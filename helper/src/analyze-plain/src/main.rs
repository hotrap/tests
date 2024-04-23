use std::collections::HashMap;
use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 1 {
        eprintln!("{} output-prefix", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let output_prefix = args.next().unwrap();

    let mut stats_out = BufWriter::new(File::create(&output_prefix).unwrap());
    let mut write_size_since_last_write_out = BufWriter::new(
        File::create(output_prefix.clone() + "-write-size-since-last-write")
            .unwrap(),
    );
    let mut num_reads_since_last_read_out = BufWriter::new(
        File::create(output_prefix.clone() + "-num-reads-since-last-read")
            .unwrap(),
    );
    let mut read_size_since_last_read_out = BufWriter::new(
        File::create(output_prefix + "-read-size-since-last-read").unwrap(),
    );

    struct KeyInfo {
        value_size: usize,
        total_write_size: usize,
        num_non_empty_reads: usize,
        non_empty_read_size: usize,
    }
    let mut keys = HashMap::<String, KeyInfo>::new();

    let mut preload_size = 0;
    let mut total_increased_size: isize = 0;
    // The actual DB size = preload_size + total_increased_size

    // Does not count preload writes
    let mut total_write_size = 0;
    let mut num_non_empty_reads = 0;
    let mut non_empty_read_size = 0;

    let mut num_reads = 0;
    let mut num_empty_reads = 0;

    let mut reader = BufReader::new(io::stdin());
    let mut nr: usize = 0;
    let mut buf = String::new();
    loop {
        buf.clear();
        nr += 1;
        if reader.read_line(&mut buf).unwrap() == 0 {
            break;
        }
        let mut s = buf.trim_end().split(' ');
        let op = s.next().expect(&nr.to_string());
        let key = s.next().expect(&nr.to_string());
        let value_size = s.next();
        assert!(
            s.next().is_none(),
            "More fields than expected in line {}",
            nr
        );
        let value_size: Option<usize> =
            value_size.map(|v| v.parse().expect(&nr.to_string()));
        if op == "READ" {
            num_reads += 1;
            let write_size_since_last_write;
            if let Some(info) = keys.get_mut(key) {
                write_size_since_last_write =
                    total_write_size - info.total_write_size;

                if info.num_non_empty_reads != 0 {
                    writeln!(
                        &mut num_reads_since_last_read_out,
                        "{}",
                        num_non_empty_reads - info.num_non_empty_reads
                    )
                    .unwrap();
                }
                num_non_empty_reads += 1;
                info.num_non_empty_reads = num_non_empty_reads;

                if info.non_empty_read_size != 0 {
                    writeln!(
                        &mut read_size_since_last_read_out,
                        "{}",
                        non_empty_read_size - info.non_empty_read_size
                    )
                    .unwrap();
                }
                non_empty_read_size += key.len() + info.value_size;
                info.non_empty_read_size = non_empty_read_size;
            } else {
                let value_size = if let Some(v) = value_size {
                    if v == 0 {
                        num_empty_reads += 1;
                        continue;
                    }
                    v
                } else {
                    num_empty_reads += 1;
                    continue;
                };
                num_non_empty_reads += 1;
                non_empty_read_size += key.len() + value_size;
                keys.insert(
                    key.to_owned(),
                    KeyInfo {
                        value_size,
                        total_write_size: 0,
                        num_non_empty_reads,
                        non_empty_read_size,
                    },
                );
                preload_size += key.len() + value_size;
                write_size_since_last_write = total_write_size;
            }
            writeln!(
                &mut write_size_since_last_write_out,
                "{}",
                write_size_since_last_write
            )
            .unwrap();
        } else if op == "INSERT" {
            let value_size = value_size.unwrap();
            total_write_size += key.len() + value_size;
            if let Some(old_info) = keys.get_mut(key) {
                total_increased_size = total_increased_size
                    - old_info.value_size as isize
                    + value_size as isize;
                *old_info = KeyInfo {
                    value_size,
                    total_write_size,
                    num_non_empty_reads: 0,
                    non_empty_read_size: 0,
                };
            } else {
                total_increased_size += (key.len() + value_size) as isize;
                keys.insert(
                    key.to_owned(),
                    KeyInfo {
                        value_size,
                        total_write_size,
                        num_non_empty_reads: 0,
                        non_empty_read_size: 0,
                    },
                );
            }
        } else {
            panic!("Unknown operation {}", op);
        }
    }

    writeln!(
        &mut stats_out,
        "db_size={}\nnum_reads={}\nnum_empty_reads={}\nempty_read_ratio={}",
        preload_size as isize + total_increased_size,
        num_reads,
        num_empty_reads,
        num_empty_reads as f64 / num_reads as f64,
    )
    .unwrap();

    Ok(())
}
