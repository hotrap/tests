use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};
use std::path::PathBuf;

extern crate metrics_util;

const QUANTILES: [f64; 12] = [
    0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 0.999, 0.9999,
];

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 2 {
        eprintln!("{} latency-file output-directory", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let latency_path = PathBuf::from(args.next().unwrap());
    let output_directory = PathBuf::from(args.next().unwrap());
    let latency_file =
        File::open(&latency_path).expect("Fail to open latency file");
    let latency_reader = BufReader::new(latency_file);
    let mut insert_stats = metrics_util::Summary::with_defaults();
    let mut read_stats = metrics_util::Summary::with_defaults();
    for line in latency_reader.lines() {
        let line = line?;
        let mut s = line.split(' ');
        let op = s.next().unwrap();
        let latency: f64 = s.next().unwrap().parse().unwrap();
        let latency_log10 = latency.log10();
        match op {
            "INSERT" => insert_stats.add(latency_log10),
            "READ" => read_stats.add(latency_log10),
            _ => panic!("Unrecognized operation {}", op),
        }
    }

    if !insert_stats.is_empty() {
        let mut insert_writer = BufWriter::new(
            File::create(output_directory.join("insert_latency")).unwrap(),
        );
        writeln!(insert_writer, "quantile latency(ns)").unwrap();
        for q in QUANTILES {
            let latency_log10 = insert_stats.quantile(q).unwrap();
            writeln!(insert_writer, "{} {}", q, 10.0_f64.powf(latency_log10))
                .unwrap();
        }
    }

    if !read_stats.is_empty() {
        let mut read_writer = BufWriter::new(
            File::create(output_directory.join("read_latency")).unwrap(),
        );
        writeln!(read_writer, "quantile latency(ns)").unwrap();
        for q in QUANTILES {
            let latency_log10 = read_stats.quantile(q).unwrap();
            writeln!(read_writer, "{} {}", q, 10.0_f64.powf(latency_log10))
                .unwrap();
        }
    }
    Ok(())
}