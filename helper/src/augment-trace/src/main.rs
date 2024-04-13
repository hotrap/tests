use serde::{self, Deserialize};
use serde_json;

use std::collections::HashMap;
use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};

#[derive(Deserialize)]
struct Info {
    #[serde(rename = "num-run-op")]
    num_run_op: usize,
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 3 {
        eprintln!("{} prefix target-num-run-op multiple", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let trace_prefix = args.next().unwrap();
    let target_num_run_op: usize = args.next().unwrap().parse().unwrap();
    let multiple: usize = args.next().unwrap().parse().unwrap();
    assert!(multiple > 0);

    let out_prefix = trace_prefix.clone() + "-" + &multiple.to_string() + "x";

    let info: Info = serde_json::from_reader(BufReader::new(
        File::open(trace_prefix.clone() + ".json").unwrap(),
    ))
    .unwrap();

    let mut num_prefix_digits = 0;
    let mut n = multiple;
    while n > 1 {
        num_prefix_digits += 1;
        n /= 10;
    }
    let mut prefix = Vec::new();
    if num_prefix_digits > 0 {
        for i in 0..multiple {
            prefix.push(format!("{:01$}", i, num_prefix_digits));
        }
    } else {
        prefix.push(String::new());
    }

    let mut kv = HashMap::new();
    let mut buf = String::new();

    let mut load_reader =
        BufReader::new(File::open(trace_prefix.clone() + "-load").unwrap());
    loop {
        buf.clear();
        if (load_reader.read_line(&mut buf)).unwrap() == 0 {
            break;
        }
        let mut s = buf.trim_end().split(' ');
        let op = s.next().unwrap();
        let key = s.next().unwrap();
        assert_eq!(op, "INSERT");
        let value_size: usize = s.next().unwrap().parse().unwrap();
        assert!(kv.insert(key.to_owned(), value_size).is_none());
    }

    let mut run_reader =
        BufReader::new(File::open(trace_prefix + "-run").unwrap());
    let mut run_writer =
        BufWriter::new(File::create(out_prefix.clone() + "-run").unwrap());

    let needed = (target_num_run_op + multiple - 1) / multiple;
    let mut to_drop = if info.num_run_op <= needed {
        0
    } else {
        info.num_run_op - needed
    };
    while to_drop > 0 {
        buf.clear();
        to_drop -= 1;
        assert_ne!(run_reader.read_line(&mut buf).unwrap(), 0);
        let mut s = buf.trim_end().split(' ');
        let op = s.next().unwrap();
        let key = s.next().unwrap();
        if op == "INSERT" {
            let value_size = s.next().unwrap().parse().unwrap();
            if let Some(v) = kv.get_mut(key) {
                *v = value_size;
            } else {
                kv.insert(key.to_owned(), value_size);
            }
        }
    }

    loop {
        buf.clear();
        if run_reader.read_line(&mut buf).unwrap() == 0 {
            break;
        }
        let mut s = buf.trim_end().split(' ');
        let op = s.next().unwrap();
        let key = s.next().unwrap();
        let part1 = op.to_owned() + " ";
        let mut part2 = key.to_owned();
        if op == "INSERT" {
            let value_size = s.next().unwrap();
            part2.push(' ');
            part2.push_str(value_size);
        }
        for i in 0..multiple {
            writeln!(&mut run_writer, "{}{}{}", part1, prefix[i], part2)
                .unwrap();
        }
    }

    let mut load_writer =
        BufWriter::new(File::create(out_prefix.clone() + "-load").unwrap());
    for (key, value_size) in kv {
        for i in 0..multiple {
            writeln!(
                &mut load_writer,
                "INSERT {}{} {}",
                prefix[i], key, value_size
            )
            .unwrap();
        }
    }

    Ok(())
}
