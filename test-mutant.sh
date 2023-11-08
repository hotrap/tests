set -e
kvexe_dir=~/kvexe-mutant/build
rm ~/testdb/log/*
systemd-run --scope -p MemoryMax=4G bash -c "$HOME/tests/helper/exe-while.sh $HOME/testdb/log bash -c \"$kvexe_dir/rocksdb-kvexe --cleanup --format=ycsb --num_threads=8 --switches=$switches --db_path=$HOME/testdb/db/ --db_paths=\\\"{{$HOME/testdb/sd,$sd_size},{$HOME/testdb/cd,$cd_size}}\\\" --costs=\\\"{0.528, 0.045}\\\" --target_cost=0.4 --enable_fast_process --enable_fast_generator --workload_file=$workload_file >/dev/null 2> $HOME/testdb/log/log.txt\"" &
wait
