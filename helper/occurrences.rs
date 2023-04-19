use std::io::{self, Write};
use std::error::Error;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn Error>> {
	let mut m: HashMap<String, usize> = HashMap::new();
	for key in io::stdin().lines() {
		let key = key?;
		m.entry(key).and_modify(|d| *d += 1).or_insert(1);
	}
	for (k, v) in m {
		if let Err(_) = writeln!(io::stdout(), "{} {}", k, v) {
			break;
		}
	}
	Ok(())
}
