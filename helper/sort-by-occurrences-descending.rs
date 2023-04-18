use std::io::{self, Write};
use std::error::Error;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn Error>> {
	let mut m: HashMap<String, usize> = HashMap::new();
	for key in io::stdin().lines() {
		let key = key?;
		m.entry(key).and_modify(|d| *d += 1).or_insert(1);
	}
	let mut v: Vec<(String, usize)> = m.drain().collect();
	v.sort_by(|a, b| b.1.cmp(&a.1));
	for (k, v) in v.as_slice() {
		if let Err(_) = writeln!(io::stdout(), "{} {}", k, *v) {
			break;
		}
	}
	Ok(())
}
