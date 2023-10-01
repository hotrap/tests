kvexe_dir=~/kvexe-prismdb/build
rm ~/testdb/log/*
systemd-run --scope -p MemoryMax=6G bash -c "$HOME/tests/helper/exe-while.sh $HOME/testdb/log bash -c \"$kvexe_dir/rocksdb-kvexe --num_threads=8 --cleanup --format=ycsb --db_path=$HOME/testdb/db --db_paths=\\\"{{$HOME/testdb/sd,4000000000},{$HOME/testdb/cd,100000000000}}\\\" --switches=$switches --migrations_logging=1 --read_logging=0 --migration_policy=2 --migration_metric=1 --migration_rand_range_num=8 --migration_rand_range_size=1 --num_load_ops=200000000 --num_keys=200000000 --optane_threshold=0.2 --slab_dir=$HOME/testdb/sd/slab-%d-%lu-%lu --pop_cache_size=$pop_cache_size --enable_fast_generator --workload_file=$workload_file --read_dominated_threshold=0.95 2> $HOME/testdb/log/log.txt\"" &
wait
