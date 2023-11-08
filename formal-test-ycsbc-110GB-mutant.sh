set -e
for workload in `cd formal-config && ls *110GB*ycsbc*`
do
	for db in prismdb mutant
	do
		echo $db-$workload
		sd_dev=nvme0c0n1 cd_dev=vda workload_file=formal-config/$workload switches=1 max_hot_set_size=2000000000 sd_size=17179869184 cd_size=1073741824000 pop_cache_size=22000000 stop_upsert_trigger=70000000 ./test-$db.sh
		workload_file=formal-config/$workload DIR=~/results/formal-$db-$workload/ ./store.sh
	done
done
