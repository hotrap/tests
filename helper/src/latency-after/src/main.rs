use core::panic;
use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufWriter, Write};
use std::path::PathBuf;

use rev_lines;
use serde_json_lenient;
use splay_safe_rs::RankTree;

fn read_json_u64<'a, 'b>(
    json: &'a serde_json_lenient::Map<String, serde_json_lenient::Value>,
    field: &'b str,
) -> u64 {
    match &json[field] {
        serde_json_lenient::Value::Number(ts) => ts.as_u64().unwrap(),
        _ => panic!(),
    }
}

struct Stat {
    path: PathBuf,
    file: Option<BufWriter<File>>,
    latencies: RankTree<u64>,
    sum: u64,
}
impl Stat {
    fn new(path: PathBuf) -> Stat {
        Stat {
            path,
            file: None,
            latencies: RankTree::new(),
            sum: 0,
        }
    }
    fn insert(&mut self, latency: u64) {
        self.latencies.insert(latency);
        self.sum += latency;
    }
    fn print(&mut self, ts: u64) {
        const PERCENTILES: &[f64] = &[0.5, 0.99, 0.999, 0.9999];
        let n = self.latencies.size();
        if n < 2 {
            return;
        }
        let file = match &mut self.file {
            Some(file) => file,
            None => {
                let mut file =
                    BufWriter::new(File::create(&self.path).unwrap());
                writeln!(
                    &mut file,
                    "Timestamp(ns) Average 50% 99% 99.9% 99.99%"
                )
                .unwrap();
                self.file = Some(file);
                self.file.as_mut().unwrap()
            }
        };
        let n = n as f64;
        write!(file, "{} {}", ts, self.sum as f64 / n).unwrap();
        for percentile in PERCENTILES {
            write!(
                file,
                " {}",
                self.latencies.query_kth((n * percentile) as u32).unwrap()
            )
            .unwrap();
        }
        writeln!(file).unwrap();
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 1 {
        eprintln!("{} directory", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let dir = PathBuf::from(args.next().unwrap());

    let json = File::open(dir.join("info.json")).unwrap();
    let json: serde_json_lenient::Value =
        serde_json_lenient::from_reader(json).unwrap();
    let json = match json {
        serde_json_lenient::Value::Object(json) => json,
        _ => panic!(),
    };
    let run_start_timestamp_ns: u64 =
        read_json_u64(&json, "run-start-timestamp(ns)");
    let run_end_timestamp_ns: u64 =
        read_json_u64(&json, "run-end-timestamp(ns)");

    let mut iters = Vec::new();
    let mut i = 0;
    while let Ok(file) =
        File::open(dir.join("latency-".to_owned() + &i.to_string()))
    {
        iters.push(
            rev_lines::RevLines::with_capacity(16 * 1024 * 1024, file)
                .peekable(),
        );
        i += 1;
    }

    let mut read = Stat::new(dir.join("read-latency"));
    let mut insert = Stat::new(dir.join("insert-latency"));
    let mut update = Stat::new(dir.join("update-latency"));
    let mut rmw = Stat::new(dir.join("rmw-latency"));

    let mut target_ts = run_end_timestamp_ns - 1000000000;
    while target_ts > run_start_timestamp_ns {
        for iter in &mut iters {
            while let Some(line) = iter.peek() {
                let line = line.as_deref().unwrap();
                let mut s = line.split(' ');
                let ts: u64 = s.next().unwrap().parse().unwrap();
                if ts < target_ts {
                    break;
                }
                let op = s.next().unwrap();
                let latency: u64 = s.next().unwrap().parse().unwrap();
                match op {
                    "READ" => read.insert(latency),
                    "INSERT" => insert.insert(latency),
                    "UPDATE" => update.insert(latency),
                    "RMW" => rmw.insert(latency),
                    _ => panic!("Unrecognized operation: {}", op),
                }
                iter.next();
            }
        }
        read.print(target_ts);
        insert.print(target_ts);
        update.print(target_ts);
        rmw.print(target_ts);
        target_ts = match target_ts.checked_sub(1000000000) {
            Some(x) => x,
            None => break,
        };
    }
    println!("{} latency files processed", i);

    Ok(())
}
