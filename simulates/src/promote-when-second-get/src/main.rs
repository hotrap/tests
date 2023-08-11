use rand::prelude::Distribution;
use rand::rngs::StdRng;
use rand::SeedableRng;
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
    let mut i = 0;
    let mut cnt = vec![0; num_hot];
    let mut promoted = 0;
    println!("\"Number of operations\" \"Promoted\"");
    while i < num_op {
        i += 1;
        if dist_0_1.sample(&mut rng) >= cold_ratio {
            let hot = dist_hot.sample(&mut rng);
            cnt[hot] += 1;
            if cnt[hot] == 2 {
                promoted += 1;
                println!("{} {}", i, promoted);
                if promoted == num_hot {
                    break;
                }
            }
        }
    }
    Ok(())
}
