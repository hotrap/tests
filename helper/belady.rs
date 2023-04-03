use std::collections::{BTreeMap, HashMap, HashSet};
use std::env;
use std::error::Error;
use std::io;

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} cache-size", args[0]);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let cache_size: usize = args[1].parse().unwrap();
    if cache_size == 0 {
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "The cache size shouldn't be zero!",
        )));
    }
    let mut keys = Vec::<String>::new();
    let mut index = HashMap::new();
    let mut next = Vec::new();
    loop {
        let mut key = String::new();
        if io::stdin().read_line(&mut key)? == 0 {
            break;
        }
        key.pop();
        keys.push(key);
    }
    for i in 0..keys.len() {
        let key = keys[i].as_str();
        index
            .entry(key)
            .and_modify(|j| {
                next[*j] = i;
                *j = i;
            })
            .or_insert(i);
        next.push(i);
    }
    let mut cached = HashSet::new();
    let mut cached_next: BTreeMap<usize, &str> = BTreeMap::new();
    let mut hit = 0;
    for i in 0..keys.len() {
        let key = keys[i].as_str();
        let cache_miss = cached.insert(key);
        if !cache_miss {
            hit += 1;
        }
        if cached.len() > cache_size {
            // Evict an item that will not be accessed for the longest time
            let evicted = cached_next.last_entry().unwrap().remove();
            assert!(evicted != key);
            cached.remove(evicted);
            assert!(cached.len() == cache_size);
        }
        cached_next.remove(&i);
        if next[i] != i {
            assert!(cached_next.insert(next[i], key) == None);
        } else {
            cached.remove(key);
        }
    }
    println!("Total: {}", keys.len());
    println!("Hit: {}", hit);
    Ok(())
}
