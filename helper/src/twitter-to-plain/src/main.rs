use std::collections::{HashMap, HashSet};
use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};

use serde::{Deserialize, Serialize};
use serde_queue::SerdeQueue;

#[derive(Serialize, Deserialize)]
enum Operation<'a> {
    // Key, value size
    Insert(&'a str, usize),
    // value size > 0 if it's the first occurrence of the key
    // value size == 0 if it's not the first occurrence of the key
    // value size == -1 if it's getting a non-existing key
    Read(&'a str, isize),
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 3 {
        eprintln!("{} prefix target-db-size max-num-run-op", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let prefix = args.next().unwrap();
    let target_db_size: usize = args.next().unwrap().parse().unwrap();
    let max_num_run_op: usize = args.next().unwrap().parse().unwrap();
    assert!(max_num_run_op > 0);

    let read_op = HashSet::from(["get".to_owned(), "gets".to_owned()]);
    let insert_op = HashSet::from([
        "set".to_owned(),
        "add".to_owned(),
        "prepend".to_owned(),
        "cas".to_owned(),
        "incr".to_owned(),
        "decr".to_owned(),
    ]);

    let mut run = SerdeQueue::new();
    let mut load = HashMap::<String, (usize, usize)>::new();
    let mut timestamp = 0;
    // Useful unstable feature: closure_lifetime_binder
    fn add<'a, 'b>(
        run: &'a mut SerdeQueue,
        op: Operation<'b>,
        max_num_run_op: usize,
        timestamp: &mut usize,
        load: &mut HashMap<String, (usize, usize)>,
    ) {
        if run.len() == max_num_run_op {
            match run.pop().unwrap().unwrap() {
                Operation::Insert(key, value_size) => {
                    *timestamp += 1;
                    load.entry(key.to_owned())
                        .and_modify(|v| *v = (value_size, *timestamp))
                        .or_insert((value_size, *timestamp));
                }
                Operation::Read(key, value_size) => {
                    if value_size > 0 {
                        assert!(load
                            .insert(key.to_owned(), (value_size as usize, 0))
                            .is_none());
                    }
                }
            }
        }
        run.push(&op).unwrap();
    }

    let mut kv = HashMap::<String, usize>::new();
    let mut db_size = 0;

    let mut reader = BufReader::new(io::stdin());
    let mut buf = String::new();
    let mut nr: usize = 0;
    let mut skipped: usize = 0;
    while db_size < target_db_size {
        buf.clear();
        nr += 1;
        if reader.read_line(&mut buf).unwrap() == 0 {
            println!("DB size {} < {}", db_size, target_db_size);
            break;
        }
        let mut s = buf.trim_end().split(',');
        s.next(); // timestamp
        let key = s.next().expect(&nr.to_string());
        s.next(); // key size
        let value_size = s.next().expect(&nr.to_string());
        s.next(); // client id
        let op = s.next().expect(&nr.to_string());
        s.next().expect(&nr.to_string()); // TTL
        if s.next().is_some() {
            // More fields than expected. Skip it.
            skipped += 1;
            continue;
        }
        let value_size = value_size.parse().expect(&nr.to_string());
        if read_op.contains(op) {
            if !kv.contains_key(key) {
                if value_size > 0 {
                    kv.insert(key.to_owned(), value_size);
                    db_size += key.len() + value_size;
                    add(
                        &mut run,
                        Operation::Read(key, value_size as isize),
                        max_num_run_op,
                        &mut timestamp,
                        &mut load,
                    );
                } else {
                    add(
                        &mut run,
                        Operation::Read(key, -1),
                        max_num_run_op,
                        &mut timestamp,
                        &mut load,
                    );
                }
            } else {
                add(
                    &mut run,
                    Operation::Read(key, 0),
                    max_num_run_op,
                    &mut timestamp,
                    &mut load,
                );
            }
        } else if insert_op.contains(op) {
            if let Some(old_value_len) = kv.get_mut(key) {
                db_size = db_size - *old_value_len + value_size;
                *old_value_len = value_size;
            } else {
                kv.insert(key.to_owned(), value_size);
                db_size += key.len() + value_size;
            }
            add(
                &mut run,
                Operation::Insert(key, value_size),
                max_num_run_op,
                &mut timestamp,
                &mut load,
            );
        } else if op == "delete" {
            // Temporarily ignore it.
        } else {
            for c in op.as_bytes() {
                if !c.is_ascii_digit() {
                    panic!("Unknown operation {}", op);
                }
            }
        }
    }

    let mut run_writer =
        BufWriter::new(File::create(prefix.clone() + "-run").unwrap());
    let num_run_op = run.len();
    let mut num_run_inserts: usize = 0;
    let mut num_reads: usize = 0;
    let mut num_empty_reads: usize = 0;
    while let Some(operation) = run.pop().unwrap() {
        match operation {
            Operation::Insert(key, value_size) => {
                num_run_inserts += 1;
                writeln!(&mut run_writer, "INSERT {} {}", key, value_size)
                    .unwrap();
            }
            Operation::Read(key, value_size) => {
                num_reads += 1;
                writeln!(&mut run_writer, "READ {}", &key).unwrap();
                if value_size > 0 {
                    assert!(load
                        .insert(key.to_owned(), (value_size as usize, 0))
                        .is_none());
                } else if value_size == -1 {
                    num_empty_reads += 1;
                }
            }
        }
    }

    let mut load_writer =
        BufWriter::new(File::create(prefix.clone() + "-load").unwrap());
    let mut load: Vec<(String, (usize, usize))> = load.drain().collect();
    load.sort_unstable_by(|a, b| a.1 .1.cmp(&b.1 .1));
    let num_load_op = load.len();
    let mut load_key_len = 0;
    let mut load_value_len = 0;
    for (key, (value_size, _)) in load {
        writeln!(&mut load_writer, "INSERT {} {}", key, value_size).unwrap();
        load_key_len += key.len();
        load_value_len += value_size;
    }

    println!(
        "Final DB size: {}\nSkipped: {}\nUnique keys: {}",
        db_size,
        skipped,
        kv.len()
    );

    writeln!(
        BufWriter::new(File::create(prefix + ".json").unwrap()),
        "{{
\t\"db-size\": {},
\t\"num-load-op\": {},
\t\"num-run-op\": {},
\t\"num-run-inserts\": {},
\t\"num-reads\": {},
\t\"num-empty-reads\": {},
\t\"load-avg-key-len\": {},
\t\"load-avg-value-len\": {}
}}",
        db_size,
        num_load_op,
        num_run_op,
        num_run_inserts,
        num_reads,
        num_empty_reads,
        load_key_len / num_load_op,
        load_value_len / num_load_op,
    )
    .unwrap();

    Ok(())
}
