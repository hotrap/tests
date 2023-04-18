use std::io;

fn main() {
	for line in io::stdin().lines() {
		let line = line.unwrap();
		let mut s = line.split(' ');
		let op = s.next().unwrap();
		if op == "READ" || op == "INSERT" || op == "UPDATE" {
			println!("{}", line);
		} else {
			eprintln!("Ignore line: {}", line);
		}
	}
}
