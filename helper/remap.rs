use std::collections::HashMap;
use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

#[derive(PartialEq)]
enum Format {
    Plain,
    YCSB,
}

/// Read all bytes into buf until a whitespace byte or EOF is reached.
/// The whitespace byte will also be appended to buf.
fn read_until_whitespace<R: BufRead>(
    mut reader: R,
    buf: &mut Vec<u8>,
) -> io::Result<()> {
    'outer: loop {
        let b = reader.fill_buf()?;
        if b.is_empty() {
            break;
        }
        for (i, c) in b.iter().enumerate() {
            buf.push(*c);
            if c.is_ascii_whitespace() {
                reader.consume(i + 1);
                break 'outer;
            }
        }
        let len = b.len();
        drop(b);
        reader.consume(len);
    }
    Ok(())
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        println!("Usage: {} format remap-file", args[0]);
        return;
    }
    let format = &args[1];
    let remap_file = File::open(&args[2]).unwrap();

    let format = match format.as_str() {
        "plain" => Format::Plain,
        "ycsb" => Format::YCSB,
        _ => panic!("Unsupported format {}", format),
    };
    let mut remap_reader = BufReader::new(remap_file);
    let mut remap = HashMap::<Vec<u8>, Vec<u8>>::new();
    loop {
        let mut k1 = Vec::new();
        read_until_whitespace(&mut remap_reader, &mut k1).unwrap();
        if k1.len() == 0 {
            break;
        }
        assert_eq!(*k1.last().unwrap(), b' ');
        k1.pop();
        let mut k2 = Vec::new();
        read_until_whitespace(&mut remap_reader, &mut k2).unwrap();
        assert!(!k2.is_empty());
        if k2.last().unwrap().is_ascii_whitespace() {
            assert_eq!(k2.pop().unwrap(), b'\n');
        }
        remap.insert(k1, k2);
    }
    let mut cin = BufReader::new(io::stdin());
    loop {
        let mut line = Vec::new();
        // Operation
        read_until_whitespace(&mut cin, &mut line).unwrap();
        if line.len() == 0 {
            break;
        }
        assert_eq!(*line.last().unwrap(), b' ');
        if format == Format::YCSB {
            // usertable
            let ori_len = line.len();
            read_until_whitespace(&mut cin, &mut line).unwrap();
            assert_ne!(line.len(), ori_len);
        }
        let mut key = Vec::new();
        read_until_whitespace(&mut cin, &mut key).unwrap();
        assert_ne!(key.len(), 0);
        let line_ends = if key.last().unwrap().is_ascii_whitespace() {
            key.pop().unwrap() == b'\n'
        } else {
            false
        };
        match remap.get(&key) {
            Some(new_key) => {
                line.extend_from_slice(new_key);
            }
            None => line.append(&mut key),
        }
        if line_ends {
            line.push(b'\n');
        } else {
            line.push(b' ');
            assert_ne!(cin.read_until(b'\n', &mut line).unwrap(), 0);
        }
        print!("{}", String::from_utf8(line).unwrap());
    }
}
