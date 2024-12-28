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
    if args.len() != 3 {
        eprintln!("Usage: {} source-dir data-dir since-timestamp(ns)", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let dir = std::path::PathBuf::from(args.next().unwrap());
    let data_dir = std::path::PathBuf::from(args.next().unwrap());
    let since_timestamp: u64 = args.next().unwrap().parse().unwrap();

    let mut first_level_in_sd = File::open(data_dir.join("first-level-in-last-tier")).unwrap();
    let mut buf = String::new();
    first_level_in_sd.read_to_string(&mut buf).unwrap();
    let first_level_in_sd: isize = buf.trim().parse().unwrap();

    let mut key_run_phase_reads = HashMap::new();
    let mut key_reads_hits = HashMap::new();
    let mut i = 0;
    while let Ok(key_hit_level) = File::open(dir.join("key-hit-level-".to_owned() + &i.to_string()))
    {
        let key_hit_level = BufReader::new(key_hit_level);
        for line in key_hit_level.lines() {
            let line = line.unwrap();
            let mut s = line.trim().split(' ');
            let timestamp: u64 = s.next().unwrap().parse().unwrap();
            let key = s.next().unwrap();
            key_run_phase_reads
                .entry(key.to_owned())
                .and_modify(|v| *v += 1)
                .or_insert(1usize);
            if timestamp < since_timestamp {
                continue;
            }
            let level: isize = s.next().unwrap().parse().expect(&line);
            let hit = (level < first_level_in_sd) as usize;
            key_reads_hits
                .entry(key.to_owned())
                .and_modify(|v: &mut (usize, usize)| {
                    v.0 += 1;
                    v.1 += hit;
                })
                .or_insert((1, hit));
        }
        i += 1;
    }
    eprintln!("{} key-hit-level files processed", i);

    let mut key_run_phase_reads: Vec<(String, usize)> = key_run_phase_reads.into_iter().collect();
    key_run_phase_reads.sort_unstable_by(|a, b| b.1.cmp(&a.1));

    #[derive(Clone)]
    struct Num {
        reads: usize,
        hits: usize,
        keys_accessed: usize,
        keys_with_hit: usize,
    }
    let mut cur = Num {
        reads: 0,
        hits: 0,
        keys_accessed: 0,
        keys_with_hit: 0,
    };
    let mut cdf = Vec::new();
    for (key, _) in &key_run_phase_reads {
        let (reads, hits) = key_reads_hits.get(key).map(|v| *v).unwrap_or((0, 0));
        cur.reads += reads;
        cur.hits += hits;
        if reads > 0 {
            cur.keys_accessed += 1;
        }
        if hits > 0 {
            cur.keys_with_hit += 1;
        }
        cdf.push(cur.clone());
    }

    let mut writer = BufWriter::new(File::create(data_dir.join("hit")).unwrap());
    writeln!(
        &mut writer,
        "key-rank reads hits keys-accessed keys-with-hit"
    )
    .unwrap();
    let max_dots = 10000;
    let n = cdf.len();
    if n == 0 {
        return Ok(());
    }
    let step = (n + max_dots - 1) / max_dots;
    let mut i = 0;
    while i < n - 1 {
        let num = &cdf[i];
        writeln!(
            &mut writer,
            "{} {} {} {} {}",
            i + 1,
            num.reads,
            num.hits,
            num.keys_accessed,
            num.keys_with_hit
        )
        .unwrap();
        i += step;
    }
    let num = &cdf[n - 1];
    writeln!(
        &mut writer,
        "{} {} {} {} {}",
        n - 1,
        num.reads,
        num.hits,
        num.keys_accessed,
        num.keys_with_hit,
    )
    .unwrap();

    Ok(())
}
