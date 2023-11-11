use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};
use std::path::{Path, PathBuf};

fn cdf(latencies: &mut Vec<u64>, dots: usize, path: &Path) {
    if latencies.is_empty() {
        return;
    }
    let n = latencies.len();
    latencies.sort();
    let x0 = (*latencies.first().unwrap() as f64).log10();
    let x1 = (*latencies.last().unwrap() as f64).log10();
    let x_step = (x1 - x0) / dots as f64;
    let n_step = (n + dots - 1) / dots;
    let mut sum = 0;
    let mut last_sum = 0;
    let mut last_x = 0.0;
    let mut writer = BufWriter::new(File::create(path).unwrap());
    let last_latency = latencies.pop().unwrap();
    for latency in latencies {
        let x = (*latency as f64).log10();
        sum += 1;
        if (x - last_x) >= x_step || sum - last_sum >= n_step {
            writeln!(&mut writer, "{} {}", latency, sum as f64 / n as f64)
                .unwrap();
            last_x = x;
            last_sum = sum;
        }
    }
    sum += 1;
    assert!(sum == n);
    writeln!(&mut writer, "{} 1", last_latency).unwrap();
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

    let mut insert_latencies = Vec::new();
    let mut read_latencies = Vec::new();
    let mut update_latencies = Vec::new();
    let mut rmw_latencies = Vec::new();

    let mut i = 0;
    while let Ok(file) =
        File::open(input_directory.join(i.to_string() + "_latency_70_100"))
    {
        let latency_reader = BufReader::new(file);
        for line in latency_reader.lines() {
            let line = line?;
            let mut s = line.split(' ');
            let op = s.next().unwrap();
            let latency: u64 = s.next().unwrap().parse().unwrap();
            match op {
                "INSERT" => insert_latencies.push(latency),
                "READ" => read_latencies.push(latency),
                "UPDATE" => update_latencies.push(latency),
                "RMW" => rmw_latencies.push(latency),
                _ => panic!("Unrecognized operation {}", op),
            }
        }
        i += 1;
    }
    println!("latency-cdf: {} latency files processed", i);

    let dots = 100000;
    cdf(
        &mut insert_latencies,
        dots,
        &output_directory.join("insert-latency-cdf"),
    );
    cdf(
        &mut read_latencies,
        dots,
        &output_directory.join("read-latency-cdf"),
    );
    cdf(
        &mut update_latencies,
        dots,
        &output_directory.join("update-latency-cdf"),
    );
    cdf(
        &mut rmw_latencies,
        dots,
        &output_directory.join("rmw-latency-cdf"),
    );

    Ok(())
}
