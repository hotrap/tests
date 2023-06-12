use std::{
    collections::HashMap,
    env,
    error::Error,
    fs::{self, File},
    io::{self, BufRead, BufReader, BufWriter, Read, Write},
};
use tempfile::tempdir;

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

    let occurrences =
        BufReader::new(File::open(dir.join("occurrences")).unwrap());
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

    let temp = tempdir().unwrap();
    let mut writer =
        BufWriter::new(File::create(temp.path().join("hits_cdf")).unwrap());
    for cdf in hits_cdf {
        writeln!(&mut writer, "{}", cdf).unwrap();
    }
    let mut writer = BufWriter::new(
        File::create(temp.path().join("occurrences_cdf")).unwrap(),
    );
    for cdf in occurrences_cdf {
        writeln!(&mut writer, "{}", cdf).unwrap();
    }
    fs::rename(temp.into_path(), dir.join("1")).unwrap();

    Ok(())
}
