use std::{
    collections::HashMap,
    env,
    error::Error,
    fs::File,
    io::{self, BufRead, BufReader, Read},
};

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 1 {
        eprintln!("Usage: {} dir", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let dir = std::path::PathBuf::from(args.next().unwrap());

    let mut first_level_in_cd =
        File::open(dir.join("first-level-in-cd")).unwrap();
    let mut buf = String::new();
    first_level_in_cd.read_to_string(&mut buf).unwrap();
    let first_level_in_cd: usize = buf.trim().parse().unwrap();

    let key_hit_level =
        BufReader::new(File::open(dir.join("key_hit_level")).unwrap());
    let mut key_hits = HashMap::new();
    for line in key_hit_level.lines() {
        let line = line.unwrap();
        let line = line.trim();
        let mut s = line.split(' ');
        let key = s.next().unwrap();
        let level: usize = s.next().unwrap().parse().unwrap();
        if level < first_level_in_cd {
            key_hits
                .entry(key.to_owned())
                .and_modify(|v| *v += 1)
                .or_insert(1usize);
        }
    }

    let occurrences = BufReader::new(
        File::open(dir.join("occurrences_sorted_by_count")).unwrap(),
    );
    let mut occurrences_cdf = vec![0];
    let mut hits_cdf = vec![0];
    for line in occurrences.lines() {
        let line = line.unwrap();
        let line = line.trim();
        let mut s = line.split(' ');
        let key = s.next().unwrap();
        let count: usize = s.next().unwrap().parse().unwrap();
        occurrences_cdf.push(occurrences_cdf.last().unwrap() + count);

        let hit_count = key_hits.get(key).map(|v| *v).unwrap_or(0);
        hits_cdf.push(hits_cdf.last().unwrap() + hit_count);
    }

    println!("key-rank occurrences hits");
    let max_dots = 10000;
    let n = hits_cdf.len();
    if n == 0 {
        return Ok(());
    }
    assert_eq!(occurrences_cdf.len(), n);
    let step = (n + max_dots - 1) / max_dots;
    let mut i = 0;
    while i < n - 1 {
        println!("{} {} {}", i + 1, occurrences_cdf[i], hits_cdf[i]);
        i += step;
    }
    println!("{} {} {}", n, occurrences_cdf[n - 1], hits_cdf[n - 1]);

    Ok(())
}
