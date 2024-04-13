use std::collections::{HashMap, HashSet, VecDeque};
use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};

enum Operation {
    // Key, value size
    Insert(String, usize),
    // value size > 0 iff it's the first occurrence of the key
    Read(String, usize),
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

    let mut run = VecDeque::new();
    let mut load = HashMap::<String, usize>::new();
    let mut add = |run: &mut VecDeque<Operation>, op: Operation| {
        if run.len() == max_num_run_op {
            match run.pop_front().unwrap() {
                Operation::Insert(key, value_size) => {
                    load.entry(key)
                        .and_modify(|v| *v = value_size)
                        .or_insert(value_size);
                }
                Operation::Read(key, value_size) => {
                    if value_size > 0 {
                        assert!(load.insert(key, value_size).is_none());
                    }
                }
            }
        }
        run.push_back(op);
    };

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
            if !kv.contains_key(key) && value_size > 0 {
                kv.insert(key.to_owned(), value_size);
                db_size += key.len() + value_size;
                add(&mut run, Operation::Read(key.to_owned(), value_size));
            } else {
                add(&mut run, Operation::Read(key.to_owned(), 0));
            }
        } else if insert_op.contains(op) {
            if let Some(old_value_len) = kv.get_mut(key) {
                db_size = db_size - *old_value_len + value_size;
                *old_value_len = value_size;
            } else {
                kv.insert(key.to_owned(), value_size);
                db_size += key.len() + value_size;
            }
            add(&mut run, Operation::Insert(key.to_owned(), value_size));
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
    for operation in run {
        match operation {
            Operation::Insert(key, value_size) => {
                writeln!(&mut run_writer, "INSERT {} {}", key, value_size)
                    .unwrap();
            }
            Operation::Read(key, value_size) => {
                writeln!(&mut run_writer, "READ {}", &key).unwrap();
                if value_size > 0 {
                    assert!(load.insert(key, value_size).is_none());
                }
            }
        }
    }

    let mut load_writer =
        BufWriter::new(File::create(prefix.clone() + "-load").unwrap());
    for (key, value_size) in load {
        writeln!(&mut load_writer, "INSERT {} {}", key, value_size).unwrap();
    }

    println!(
        "Final DB size: {}\nSkipped: {}\nUnique keys: {}",
        db_size,
        skipped,
        kv.len()
    );

    writeln!(
        BufWriter::new(File::create(prefix + ".json").unwrap()),
        "{{\n\t\"num-run-op\": {},\n\t\"db-size\": {}\n}}",
        num_run_op,
        db_size
    )
    .unwrap();

    Ok(())
}
