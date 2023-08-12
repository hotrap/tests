use rand::prelude::Distribution;
use rand::rngs::StdRng;
use rand::SeedableRng;
use std::collections::BTreeMap;
use std::env;
use std::error::Error;
use std::io;

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 3 {
        eprintln!("{} num-hot cold-ratio num-op", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let num_hot: usize = args.next().unwrap().parse().unwrap();
    let cold_ratio: f64 = args.next().unwrap().parse().unwrap();
    let num_op: usize = args.next().unwrap().parse().unwrap();

    let mut rng = StdRng::seed_from_u64(233);
    let dist_0_1 = rand::distributions::Uniform::new(0.0, 1.0);
    let dist_hot = rand::distributions::Uniform::new(0, num_hot);
    #[derive(Default, Clone)]
    struct HotInfo {
        tick: usize,
        stable: bool,
    }
    let mut info = vec![HotInfo::default(); num_hot];
    let mut tick_id = BTreeMap::new();
    let mut promoted = 0;
    let mut tick = 0;
    while tick < num_op {
        tick += 1;
        if dist_0_1.sample(&mut rng) < cold_ratio {
            assert!(tick_id.insert(tick, num_hot).is_none()); // ID of cold records is "num_hot"
        } else {
            let id = dist_hot.sample(&mut rng);
            if info[id].tick != 0 {
                if !info[id].stable {
                    info[id].stable = true;
                    promoted += 1;
                    println!("{} {}", tick, promoted);
                }
                tick_id.remove(&info[id].tick);
            }
            info[id].tick = tick;
            assert!(tick_id.insert(tick, id).is_none());
        }
        if tick_id.len() > num_hot {
            let (_, id) = tick_id.pop_first().unwrap();
            if id != num_hot {
                info[id].tick = 0;
                if info[id].stable {
                    info[id].stable = false;
                    promoted -= 1;
                    println!("{} {}", tick, promoted);
                }
            }
        }
    }
    Ok(())
}
