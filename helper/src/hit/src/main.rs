use std::{
    collections::HashMap,
    env,
    error::Error,
    fs::File,
    io::{self, BufRead, BufReader, Read, BufWriter, Write},
};

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 2 {
        eprintln!("Usage: {} db_dir data_dir", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let dir = std::path::PathBuf::from(args.next().unwrap());
    let data_dir = std::path::PathBuf::from(args.next().unwrap());

    let mut first_level_in_cd =
        File::open(data_dir.join("first-level-in-cd")).unwrap();
    let mut buf = String::new();
    first_level_in_cd.read_to_string(&mut buf).unwrap();
    let first_level_in_cd: usize = buf.trim().parse().unwrap();

    let mut key_hits = HashMap::new();
    let mut i = 0;
    while let Ok(key_hit_level) =
        File::open(dir.join(i.to_string() + "_key_hit_level_70_100"))
    {
        let key_hit_level = BufReader::new(key_hit_level);
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
        i += 1;
    }
    eprintln!("{} key_hit_level files processed", i);

    let occurrences = if let Ok(occurrences) =
        File::open(dir.join("occurrences_sorted_by_count"))
    {
        occurrences
    } else {
        return Ok(());
    };
    let occurrences = BufReader::new(occurrences);
    let mut occurrences_cdf = vec![0];
    let mut hits_cdf = vec![0];
    for line in occurrences.lines() {
        let line = line.unwrap();
        let line = line.trim();
        let mut s = line.split(' ');
        let key = s.next().unwrap();
        let count: usize = s.next().unwrap().parse().unwrap();
        occurrences_cdf.push(occurrences_cdf.last().unwrap() + count);

        if !key_hits.is_empty() {
            let hit_count = key_hits.get(key).map(|v| *v).unwrap_or(0);
            hits_cdf.push(hits_cdf.last().unwrap() + hit_count);
        }
    }

    let mut writer = BufWriter::new(File::create(data_dir.join("hit")).unwrap());
    write!(&mut writer, "key-rank occurrences").unwrap();
    if hits_cdf.len() != 1 {
        write!(&mut writer, " hits").unwrap();
    }
    writeln!(&mut writer).unwrap();
    let max_dots = 10000;
    let n = occurrences_cdf.len();
    if n == 0 {
        return Ok(());
    }
    let step = (n + max_dots - 1) / max_dots;
    if hits_cdf.len() != 1 {
        assert_eq!(hits_cdf.len(), n);
    }
    let mut i = 0;
    while i < n - 1 {
        write!(&mut writer, "{} {}", i + 1, occurrences_cdf[i]).unwrap();
        if hits_cdf.len() != 1 {
            write!(&mut writer, " {}", hits_cdf[i]).unwrap();
        }
        writeln!(&mut writer).unwrap();
        i += step;
    }
    write!(&mut writer, "{} {}", n, occurrences_cdf[n - 1]).unwrap();
    if hits_cdf.len() != 1 {
        write!(&mut writer, " {}", hits_cdf[n - 1]).unwrap();
    }
    writeln!(&mut writer).unwrap();

    Ok(())
}
