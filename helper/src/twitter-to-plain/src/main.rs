use std::collections::{HashSet, VecDeque};
use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};

enum Operation {
    // Key, value size, is first occurrence
    Insert(String, usize, bool),
    Read(String),
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 3 {
        eprintln!("{} prefix target-db-size num-run-op", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let prefix = args.next().unwrap();
    let target_db_size: usize = args.next().unwrap().parse().unwrap();
    let target_num_run_op: usize = args.next().unwrap().parse().unwrap();
    assert!(target_num_run_op > 0);

    let read_op = HashSet::from(["get".to_owned(), "gets".to_owned()]);
    let insert_op = HashSet::from([
        "set".to_owned(),
        "add".to_owned(),
        "prepend".to_owned(),
        "cas".to_owned(),
        "incr".to_owned(),
        "decr".to_owned(),
    ]);

    let mut load_writer =
        BufWriter::new(File::create(prefix.clone() + "-load").unwrap());
    let mut db_size = 0;

    let mut run = VecDeque::new();
    let add_operation = |run: &mut VecDeque<Operation>,
                         load_writer: &mut BufWriter<File>,
                         op: Operation| {
        if run.len() == target_num_run_op {
            if let Operation::Insert(key, value_size, is_first_occurrence) =
                run.pop_front().unwrap()
            {
                if is_first_occurrence {
                    writeln!(load_writer, "INSERT {} {}", key, value_size)
                        .unwrap();
                }
            }
        }
        run.push_back(op);
    };

    let mut keys = HashSet::<String>::new();

    let mut reader = BufReader::new(io::stdin());
    let mut buf = String::new();
    let mut nr: usize = 0;
    let mut skipped: usize = 0;
    while db_size < target_db_size || run.len() < target_num_run_op {
        buf.clear();
        nr += 1;
        if reader.read_line(&mut buf).unwrap() == 0 {
            if db_size < target_db_size {
                println!("DB size {} < {}", db_size, target_db_size);
            } else {
                println!(
                    "Number of operations {} < {}",
                    run.len(),
                    target_num_run_op
                );
            }
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
        // Useful unstable: hash_set_entry
        if read_op.contains(op) {
            if !keys.contains(key) && value_size > 0 {
                keys.insert(key.to_owned());
                db_size += key.len() + value_size;
                writeln!(&mut load_writer, "INSERT {} {}", key, value_size)
                    .unwrap();
            }
            add_operation(
                &mut run,
                &mut load_writer,
                Operation::Read(key.to_owned()),
            );
        } else if insert_op.contains(op) {
            // Useful unstable: hash_set_entry
            let is_first_occurrence;
            if !keys.contains(key) {
                keys.insert(key.to_owned());
                db_size += key.len() + value_size;
                is_first_occurrence = true;
            } else {
                is_first_occurrence = false;
            }
            add_operation(
                &mut run,
                &mut load_writer,
                Operation::Insert(
                    key.to_owned(),
                    value_size,
                    is_first_occurrence,
                ),
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

    let mut run_writer = BufWriter::new(File::create(prefix + "-run").unwrap());
    for operation in &run {
        match operation {
            Operation::Insert(key, value_size, _) => {
                writeln!(&mut run_writer, "INSERT {} {}", key, value_size)
                    .unwrap();
            }
            Operation::Read(key) => {
                writeln!(&mut run_writer, "READ {}", key).unwrap();
            }
        }
    }

    println!(
        "Final DB size: {}\nSkipped: {}\nUnique keys: {}",
        db_size,
        skipped,
        keys.len()
    );

    Ok(())
}
