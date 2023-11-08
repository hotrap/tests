kvexe_dir=~/kvexe-hotrap/build
rm ~/testdb/log/*
systemd-run --scope -p MemoryMax=6G bash -c "$HOME/tests/helper/exe-while.sh $HOME/testdb/log bash -c \"$kvexe_dir/rocksdb-kvexe --cleanup --format=ycsb --compaction_pri=5 --num_threads=8 --max_hot_set_size=$max_hot_set_size --switches=$switches --db_path=$HOME/testdb/db --db_paths=\\\"{{$HOME/testdb/sd,40000000000},{$HOME/testdb/cd,100000000000}}\\\" --viscnts_path=$HOME/testdb/viscnts/ --enable_fast_process --enable_fast_generator --workload_file=$workload_file --max_background_jobs=4 --level0_file_num_compaction_trigger=1 2> $HOME/testdb/log/log.txt\"" &
wait