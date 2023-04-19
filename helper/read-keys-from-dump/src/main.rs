use std::io;
use std::env;
use std::error::Error;
use std::fs::File;

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 1 {
        eprintln!("{} dump-file", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let file_path = args.next().unwrap();
    let f = File::open(file_path)?;
    let val: serde_json::Value = serde_json::from_reader(f)?;
    let arr = val.as_array().unwrap();
    for d in arr {
        let bytes = d["key"].as_array().unwrap();
        let s: Vec<u8> = bytes.iter().map(|v| v.as_u64().unwrap().try_into().unwrap()).collect();
        let s = String::from_utf8(s).unwrap();
        println!("{}", s);
    }
    Ok(())
}
