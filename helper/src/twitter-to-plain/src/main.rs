use std::collections::{HashMap, HashSet};
use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 2 {
        eprintln!("{} prefix target-db-size", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let prefix = args.next().unwrap();
    let target_db_size: usize = args.next().unwrap().parse().unwrap();

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

    let mut run_writer = BufWriter::new(File::create(prefix + "-run").unwrap());
    let add_read = |run_writer: &mut BufWriter<File>, key: &str| {
        writeln!(run_writer, "READ {}", key).unwrap();
    };
    let add_insert =
        |run_writer: &mut BufWriter<File>, key: &str, value_size: usize| {
            writeln!(run_writer, "INSERT {} {}", key, value_size).unwrap();
        };

    let mut kv = HashMap::<String, usize>::new();

    let mut reader = BufReader::new(io::stdin());
    let mut buf = String::new();
    let mut nr: usize = 0;
    let mut skipped: usize = 0;
    while db_size < target_db_size {
        buf.clear();
        nr += 1;
        if reader.read_line(&mut buf).unwrap() == 0 {
            if db_size < target_db_size {
                println!("DB size {} < {}", db_size, target_db_size);
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
        if read_op.contains(op) {
            if !kv.contains_key(key) && value_size > 0 {
                kv.insert(key.to_owned(), value_size);
                db_size += key.len() + value_size;
                writeln!(&mut load_writer, "INSERT {} {}", key, value_size)
                    .unwrap();
            }
            add_read(&mut run_writer, key);
        } else if insert_op.contains(op) {
            if let Some(old_value_len) = kv.get_mut(key) {
                db_size = db_size - *old_value_len + value_size;
                *old_value_len = value_size;
            } else {
                kv.insert(key.to_owned(), value_size);
                db_size += key.len() + value_size;
            }
            add_insert(&mut run_writer, key, value_size);
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

    println!(
        "Final DB size: {}\nSkipped: {}\nUnique keys: {}",
        db_size,
        skipped,
        kv.len()
    );

    Ok(())
}
