use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::collections::HashMap;
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("Usage: {} remap-file", args[0]);
        return;
    }
    let remap_file = File::open(&args[1]).unwrap();
    let mut remap_reader = BufReader::new(remap_file);
    let mut remap = HashMap::<Vec<u8>, Vec<u8>>::new();
    loop {
        let mut k1 = Vec::new();
        if remap_reader.read_until(b' ', &mut k1).unwrap() == 0 {
            break;
        }
        let mut k2 = Vec::new();
        assert!(remap_reader.read_until(b'\n', &mut k2).unwrap() != 0);
        assert!(*k2.last().unwrap() == b'\n');
        k2.pop();
        remap.insert(k1, k2);
    }
    let mut cin = BufReader::new(io::stdin());
    loop {
        let mut line = Vec::new();
        // Operation
        if cin.read_until(b' ', &mut line).unwrap() == 0 {
            break;
        }
        // usertable
        assert!(cin.read_until(b' ', &mut line).unwrap() != 0);
        let mut key = Vec::new();
        assert!(cin.read_until(b' ', &mut key).unwrap() != 0);
        match remap.get(&key) {
            Some(new_key) => {
                line.extend_from_slice(new_key);
                line.push(b' ');
            },
            None => line.append(&mut key),
        }
        assert!(cin.read_until(b'\n', &mut line).unwrap() != 0);
        print!("{}", String::from_utf8(line).unwrap());
    }
}
