use std::collections::{HashMap, HashSet};
use std::env;
use std::error::Error;
use std::fs::File;
use std::hash::{BuildHasherDefault, DefaultHasher};
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
    Delete(&'a str),
}
impl<'a> Operation<'a> {
    fn key(&'a self) -> &'a str {
        match self {
            Self::Insert(key, _) => key,
            Self::Read(key, _) => key,
            Self::Delete(key) => key,
        }
    }
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
    let mut prefix = args.next().unwrap();
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
    let mut load: HashMap<
        String,
        (usize, usize),
        BuildHasherDefault<DefaultHasher>,
    > = HashMap::with_hasher(BuildHasherDefault::default());
    let mut timestamp = 0;
    fn add_to_load(
        op: Operation,
        timestamp: &mut usize,
        load: &mut HashMap<
            String,
            (usize, usize),
            BuildHasherDefault<DefaultHasher>,
        >,
    ) {
        match op {
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
            Operation::Delete(key) => {
                load.remove(key);
            }
        }
    }
    // Useful unstable feature: closure_lifetime_binder
    fn add<'a, 'b>(
        run: &'a mut SerdeQueue,
        op: Operation<'b>,
        max_num_run_op: usize,
        timestamp: &mut usize,
        load: &mut HashMap<
            String,
            (usize, usize),
            BuildHasherDefault<DefaultHasher>,
        >,
    ) {
        if run.len() == max_num_run_op {
            add_to_load(run.pop().unwrap().unwrap(), timestamp, load);
        }
        run.push(&op).unwrap();
    }

    struct KeyInfo {
        value_size: usize,
        augment: usize,
    }
    let mut keys: HashMap<String, KeyInfo, BuildHasherDefault<DefaultHasher>> =
        HashMap::with_hasher(BuildHasherDefault::default());
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
            if !keys.contains_key(key) {
                if value_size > 0 {
                    keys.insert(
                        key.to_owned(),
                        KeyInfo {
                            value_size,
                            augment: 1,
                        },
                    );
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
            if let Some(old_info) = keys.get_mut(key) {
                db_size = db_size - old_info.value_size + value_size;
                old_info.value_size = value_size;
            } else {
                keys.insert(
                    key.to_owned(),
                    KeyInfo {
                        value_size,
                        augment: 1,
                    },
                );
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
            if let Some(info) = keys.remove(key) {
                db_size -= key.len() + info.value_size;
            }
            add(
                &mut run,
                Operation::Delete(key),
                max_num_run_op,
                &mut timestamp,
                &mut load,
            );
        } else {
            for c in op.as_bytes() {
                if !c.is_ascii_digit() {
                    panic!("Unknown operation {}", op);
                }
            }
        }
    }

    let mut stats_writer =
        BufWriter::new(File::create(prefix.clone() + ".json").unwrap());
    writeln!(
        &mut stats_writer,
        "{{\n\t\"db-size\": {},\n\t\"num-unique-keys\": {},",
        db_size,
        keys.len()
    )
    .unwrap();

    let mut augment_prefix = Vec::new();
    let mut num_prefix_digits = 0;
    let mut default_augment = 1;
    if db_size < target_db_size {
        default_augment = (target_db_size + db_size - 1) / db_size;

        let mut n = default_augment - 1;
        while n > 0 {
            num_prefix_digits += 1;
            n /= 10;
        }
        let db_size = db_size + keys.len() * num_prefix_digits;
        if db_size >= target_db_size {
            num_prefix_digits = 0;
        } else {
            let mut augmented_db_size = db_size * (default_augment - 1);
            assert!(augmented_db_size + db_size >= target_db_size);
            while augmented_db_size >= target_db_size {
                default_augment -= 1;
                augmented_db_size -= db_size;
            }
            let mut num_unique_keys = 0;
            for (key, info) in keys.iter_mut() {
                if augmented_db_size >= target_db_size {
                    info.augment = default_augment - 1;
                } else {
                    info.augment = default_augment;
                    augmented_db_size +=
                        num_prefix_digits + key.len() + info.value_size;
                }
                num_unique_keys += info.augment;
            }
            writeln!(
                &mut stats_writer,
                "\t\"augment\": {}\n}}",
                default_augment
            )
            .unwrap();
            prefix.push('-');
            prefix += &default_augment.to_string();
            prefix.push('x');
            stats_writer =
                BufWriter::new(File::create(prefix.clone() + ".json").unwrap());
            writeln!(
                &mut stats_writer,
                "{{\n\t\"db-size\": {},\n\t\"num-unique-keys\": {},",
                augmented_db_size, num_unique_keys
            )
            .unwrap();
            for i in 0..default_augment {
                augment_prefix.push(format!("{:01$}", i, num_prefix_digits));
            }

            let mut augmented_num_run_op = 0;
            for op in run.iter::<Operation>() {
                if let Some(info) = keys.get(op.key()) {
                    augmented_num_run_op += info.augment;
                } else {
                    augmented_num_run_op += default_augment;
                }
            }
            while augmented_num_run_op > max_num_run_op {
                let op: Operation = run.pop().unwrap().unwrap();
                if let Some(info) = keys.get(op.key()) {
                    augmented_num_run_op -= info.augment;
                    add_to_load(op, &mut timestamp, &mut load);
                } else {
                    augmented_num_run_op -= default_augment;
                }
            }
        }
    }
    if augment_prefix.len() == 0 {
        augment_prefix.push(String::new());
    }

    let mut run_writer =
        BufWriter::new(File::create(prefix.clone() + "-run").unwrap());
    let mut num_run_inserts: usize = 0;
    let mut num_reads: usize = 0;
    let mut num_empty_reads: usize = 0;
    let mut num_deletes: usize = 0;
    let mut num_empty_deletes: usize = 0;
    while let Some(operation) = run.pop().unwrap() {
        match operation {
            Operation::Insert(key, value_size) => {
                let augment = if let Some(info) = keys.get(key) {
                    info.augment
                } else {
                    default_augment
                };
                num_run_inserts += augment;
                for i in 0..augment {
                    writeln!(
                        &mut run_writer,
                        "INSERT {}{} {}",
                        augment_prefix[i], key, value_size
                    )
                    .unwrap();
                }
            }
            Operation::Read(key, value_size) => {
                let augment = if let Some(info) = keys.get(key) {
                    info.augment
                } else {
                    default_augment
                };
                num_reads += augment;
                for i in 0..augment {
                    writeln!(
                        &mut run_writer,
                        "READ {}{}",
                        augment_prefix[i], key
                    )
                    .unwrap();
                }
                if value_size > 0 {
                    // It seems that this is possible in the trace:
                    // read key1 123
                    // delete key1
                    // read key1 123
                    load.insert(key.to_owned(), (value_size as usize, 0));
                } else if value_size == -1 {
                    num_empty_reads += augment;
                }
            }
            Operation::Delete(key) => {
                let augment = if let Some(info) = keys.get(key) {
                    info.augment
                } else {
                    num_empty_deletes += default_augment;
                    default_augment
                };
                num_deletes += augment;
                for i in 0..augment {
                    writeln!(
                        &mut run_writer,
                        "DELETE {}{}",
                        augment_prefix[i], &key
                    )
                    .unwrap();
                }
            }
        }
    }

    let mut load_writer =
        BufWriter::new(File::create(prefix.clone() + "-load").unwrap());
    let mut load: Vec<(String, (usize, usize))> = load.drain().collect();
    load.sort_unstable_by(|a, b| a.1 .1.cmp(&b.1 .1));
    let mut num_load_op = 0;
    let mut load_key_len = 0;
    let mut load_value_len = 0;
    for (key, (value_size, _)) in load {
        let augment = if let Some(info) = keys.get(&key) {
            info.augment
        } else {
            default_augment
        };
        num_load_op += augment;
        load_key_len += (num_prefix_digits + key.len()) * augment;
        load_value_len += value_size * augment;
        for i in 0..augment {
            writeln!(
                &mut load_writer,
                "INSERT {}{} {}",
                augment_prefix[i], key, value_size
            )
            .unwrap();
        }
    }

    println!("Skipped: {}", skipped);

    writeln!(
        &mut stats_writer,
        "\t\"num-load-op\": {},
\t\"num-run-op\": {},
\t\"num-run-inserts\": {},
\t\"num-reads\": {},
\t\"num-empty-reads\": {},
\t\"num-deletes\": {},
\t\"num-empty-deletes\": {},
\t\"load-avg-key-len\": {},
\t\"load-avg-value-len\": {}
}}",
        num_load_op,
        num_run_inserts + num_reads,
        num_run_inserts,
        num_reads,
        num_empty_reads,
        num_deletes,
        num_empty_deletes,
        load_key_len / num_load_op,
        load_value_len / num_load_op,
    )
    .unwrap();

    Ok(())
}
