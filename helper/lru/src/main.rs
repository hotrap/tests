use index_list::{Index, IndexList};
use std::{collections::HashMap, env, error::Error, io, rc::Rc};

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
    let mut lru: IndexList<Rc<String>> = IndexList::new();
    let mut cached: HashMap<Rc<String>, Index> = HashMap::new();
    let mut total: usize = 0;
    let mut hit: usize = 0;
    loop {
        let mut key = String::new();
        if io::stdin().read_line(&mut key)? == 0 {
            break;
        }
        key.pop();
        total += 1;
        let key = Rc::new(key);
        let entry = cached.entry(key);
        entry
            .and_modify(|index| {
                hit += 1;
                let key = lru.remove(*index).unwrap();
                *index = lru.insert_first(key);
            })
            .or_insert_with_key(|key| lru.insert_first(key.clone()));
        if cached.len() > cache_size {
            let evicted = lru.remove_last().unwrap();
            cached.remove(&evicted);
            assert!(cached.len() == cache_size);
        }
    }
    println!("Total: {}", total);
    println!("Hit: {}", hit);
    Ok(())
}
