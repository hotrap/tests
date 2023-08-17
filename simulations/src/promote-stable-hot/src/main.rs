use rand::prelude::Distribution;
use rand::rngs::StdRng;
use rand::SeedableRng;
use std::collections::BTreeMap;
use std::env;
use std::error::Error;
use std::io;
use std::ops::Bound::{Excluded, Unbounded};

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args();
    let arg0 = args.next().unwrap();
    // args.len(): Returns the exact remaining length of the iterator.
    if args.len() != 4 {
        eprintln!("{} num-hot cold-ratio num-op probation-size", arg0);
        return Err(Box::new(io::Error::new(
            io::ErrorKind::Other,
            "Invalid arguments",
        )));
    }
    let num_hot: usize = args.next().unwrap().parse().unwrap();
    let cold_ratio: f64 = args.next().unwrap().parse().unwrap();
    let num_op: usize = args.next().unwrap().parse().unwrap();
    let probation_size: usize = args.next().unwrap().parse().unwrap();
    let max_tracked_size = num_hot + probation_size;

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
    let mut boundary_tick = 0; // The first probation tick
    let mut hot_region_size = 0;
    let mut probation_stable_hot = 0;
    println!("\"Number of operations\" \"Promoted\"");
    while tick < num_op {
        tick += 1;
        if dist_0_1.sample(&mut rng) < cold_ratio {
            assert!(tick_id.insert(tick, num_hot).is_none()); // ID of cold records is "num_hot"
            hot_region_size += 1;
        } else {
            let id = dist_hot.sample(&mut rng);
            if info[id].tick <= boundary_tick {
                hot_region_size += 1;
                if info[id].stable {
                    assert!(info[id].tick != 0);
                    probation_stable_hot -= 1;
                }
            }
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
        if hot_region_size + probation_stable_hot > num_hot {
            loop {
                let (next_tick, next_id) = tick_id
                    .range((Excluded(boundary_tick), Unbounded))
                    .next()
                    .unwrap();
                boundary_tick = *next_tick;
                hot_region_size -= 1;
                if *next_id == num_hot || !info[*next_id].stable {
                    break;
                }
                probation_stable_hot += 1;
            }
            assert!(hot_region_size + probation_stable_hot == num_hot);
        }
        if tick_id.len() > max_tracked_size {
            let (_, id) = tick_id.pop_first().unwrap();
            if id != num_hot {
                info[id].tick = 0;
                if info[id].stable {
                    info[id].stable = false;
                    assert!(probation_stable_hot > 0);
                    probation_stable_hot -= 1;
                    promoted -= 1;
                    println!("{} {}", tick, promoted);
                }
            }
            assert!(tick_id.len() == max_tracked_size);
        }
    }
    Ok(())
}
