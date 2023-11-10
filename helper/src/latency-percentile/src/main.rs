use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};
use std::path::{Path, PathBuf};

extern crate metrics_util;

const QUANTILES: [f64; 12] = [
    0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 0.999, 0.9999,
];

struct Stat {
    num: u64,
    sum: f64,
    max: f64,
    summary: metrics_util::Summary,
}

impl Stat {
    fn new() -> Stat {
        Stat {
            num: 0,
            sum: 0.0,
            max: 0.0,
            summary: metrics_util::Summary::with_defaults(),
        }
    }
    fn add(&mut self, latency: f64) {
        self.num += 1;
        self.sum += latency;
        if latency > self.max {
            self.max = latency;
        }
        self.summary.add(latency.log10());
    }
    fn store(&self, path: &Path) {
        if !self.summary.is_empty() {
            let mut writer = BufWriter::new(File::create(path).unwrap());
            writeln!(writer, "quantile latency(ns)").unwrap();
            for q in QUANTILES {
                let latency_log10 = self.summary.quantile(q).unwrap();
                writeln!(writer, "{} {}", q, 10.0_f64.powf(latency_log10))
                    .unwrap();
            }
            writeln!(writer, "average {}", self.sum / self.num as f64).unwrap();
            writeln!(writer, "max {}", self.max).unwrap();
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 2 {
        eprintln!("{} input-directory output-directory", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let input_directory = PathBuf::from(args.next().unwrap());
    let output_directory = PathBuf::from(args.next().unwrap());
    let mut insert_stats = Stat::new();
    let mut read_stats = Stat::new();
    let mut update_stats = Stat::new();
    let mut rmw_stats = Stat::new();
    let mut i = 0;
    while let Ok(file) =
        File::open(input_directory.join(i.to_string() + "_latency_70_100"))
    {
        let latency_reader = BufReader::new(file);
        for line in latency_reader.lines() {
            let line = line?;
            let mut s = line.split(' ');
            let op = s.next().unwrap();
            let latency: f64 = s.next().unwrap().parse().unwrap();
            match op {
                "INSERT" => insert_stats.add(latency),
                "READ" => read_stats.add(latency),
                "UPDATE" => update_stats.add(latency),
                "RMW" => rmw_stats.add(latency),
                _ => panic!("Unrecognized operation {}", op),
            }
        }
        i += 1;
    }
    println!("{} latency files processed", i);

    insert_stats.store(&output_directory.join("insert_latency"));
    read_stats.store(&output_directory.join("read_latency"));
    update_stats.store(&output_directory.join("update_latency"));
    rmw_stats.store(&output_directory.join("rmw_latency"));

    Ok(())
}
