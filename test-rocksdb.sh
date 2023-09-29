kvexe_dir=~/kvexe-rocksdb/build
rm ~/testdb/log/*
nohup bash -c "$HOME/tests/helper/exe-while.sh $HOME/testdb/log bash -c \"$kvexe_dir/rocksdb-kvexe --cleanup --format=ycsb --num_threads=8 --switches=0 --db_path=$HOME/testdb/db --db_paths=\\\"{{$HOME/testdb/sd,40000000000},{$HOME/testdb/cd,100000000000}}\\\" --enable_fast_process --enable_fast_generator --workload_file=$workload_file --max_background_jobs=4 --level0_file_num_compaction_trigger=1 2> $HOME/testdb/log/log.txt\"" &
