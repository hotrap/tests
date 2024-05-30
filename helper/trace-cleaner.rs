use std::collections::HashSet;
use std::io;

fn main() {
    let supported = HashSet::from([
        "READ".to_owned(),
        "INSERT".to_owned(),
        "UPDATE".to_owned(),
        "RMW".to_owned(),
        "DELETE".to_owned(),
        "SCAN".to_owned(),
    ]);
	for line in io::stdin().lines() {
		let line = line.unwrap();
		let mut s = line.split(' ');
		let op = s.next().unwrap();
		if supported.contains(op) {
			println!("{}", line);
		} else {
			eprintln!("Ignore line: {}", line);
		}
	}
}
