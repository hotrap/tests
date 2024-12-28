use std::{
    collections::HashMap,
    env,
    error::Error,
    fs::File,
    io::{self, BufRead, BufReader, BufWriter, Read, Write},
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

    let mut buf = String::new();
    File::open(data_dir.join("timestamp-90p"))
        .unwrap()
        .read_to_string(&mut buf)
        .unwrap();
    let timestamp_90p: u64 = buf.trim().parse().unwrap();

    let mut first_level_in_sd = File::open(data_dir.join("first-level-in-last-tier")).unwrap();
    let mut buf = String::new();
    first_level_in_sd.read_to_string(&mut buf).unwrap();
    let first_level_in_sd: isize = buf.trim().parse().unwrap();

    let mut key_reads = HashMap::new();
    let mut key_hits = HashMap::new();
    let mut i = 0;
    while let Ok(key_hit_level) = File::open(dir.join("key-hit-level-".to_owned() + &i.to_string()))
    {
        let key_hit_level = BufReader::new(key_hit_level);
        for line in key_hit_level.lines() {
            let line = line.unwrap();
            let mut s = line.trim().split(' ');
            let timestamp: u64 = s.next().unwrap().parse().unwrap();
            if timestamp < timestamp_90p {
                continue;
            }
            let key = s.next().unwrap();
            let level: isize = s.next().unwrap().parse().expect(&line);
            key_reads
                .entry(key.to_owned())
                .and_modify(|v| *v += 1)
                .or_insert(1usize);
            if level < first_level_in_sd {
                key_hits
                    .entry(key.to_owned())
                    .and_modify(|v| *v += 1)
                    .or_insert(1usize);
            }
        }
        i += 1;
    }
    eprintln!("{} key-hit-level files processed", i);

    let mut key_reads: Vec<(String, usize)> = key_reads.into_iter().collect();
    key_reads.sort_unstable_by(|a, b| b.1.cmp(&a.1));

    let mut reads_cdf = vec![0];
    let mut hits_cdf = vec![0];
    for (key, reads) in &key_reads {
        reads_cdf.push(reads_cdf.last().unwrap() + reads);
        let hit_count = key_hits.get(key).map(|v| *v).unwrap_or(0);
        hits_cdf.push(hits_cdf.last().unwrap() + hit_count);
    }

    let mut writer = BufWriter::new(File::create(data_dir.join("hit")).unwrap());
    writeln!(&mut writer, "key-rank reads hits").unwrap();
    let max_dots = 10000;
    let n = reads_cdf.len();
    if n == 0 {
        return Ok(());
    }
    let step = (n + max_dots - 1) / max_dots;
    if hits_cdf.len() != 1 {
        assert_eq!(hits_cdf.len(), n);
    }
    let mut i = 0;
    while i < n - 1 {
        write!(&mut writer, "{} {}", i + 1, reads_cdf[i]).unwrap();
        if hits_cdf.len() != 1 {
            write!(&mut writer, " {}", hits_cdf[i]).unwrap();
        }
        writeln!(&mut writer).unwrap();
        i += step;
    }
    write!(&mut writer, "{} {}", n, reads_cdf[n - 1]).unwrap();
    if hits_cdf.len() != 1 {
        write!(&mut writer, " {}", hits_cdf[n - 1]).unwrap();
    }
    writeln!(&mut writer).unwrap();

    Ok(())
}
