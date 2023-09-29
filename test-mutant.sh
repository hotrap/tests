kvexe_dir=~/kvexe-mutant/build
rm ~/testdb/log/*
systemd-run --scope -p MemoryMax=6G nohup bash -c "$HOME/tests/helper/exe-while.sh $HOME/testdb/log bash -c \"$kvexe_dir/rocksdb-kvexe --cleanup --format=ycsb --num_threads=8 --switches=0 --db_path=$HOME/testdb/db/ --db_paths=\\\"{{$HOME/testdb/sd,60000000000},{$HOME/testdb/cd,100000000000}}\\\" --costs=\\\"{0.528, 0.045}\\\" --target_cost=0.4 --enable_fast_process --enable_fast_generator --workload_file=$workload_file 2> $HOME/testdb/log/log.txt\"" &
