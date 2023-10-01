set -e
for workload in `ls formal-config/`
do
	for db in rocksdb prismdb mutant hotrap
	do
		echo $db-$workload
		workload_file=formal-config/$workload switches=1 max_hot_set_size=2000000000 pop_cache_size=22000000 ./test-$db.sh
		workload_file=formal-config/$workload DIR=~/results/formal-$db-$workload/ ./store.sh
	done
done
