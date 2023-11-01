if [[ $# < 2 || $# > 3 ]]; then
	echo Usage: $0 config-file output-dir [instance-name-base]
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
if [ $3 ]; then
	instance_name_base=$3
else
	instance_name_base=hotrap-auto-
fi
cd $(dirname $0)

workloads=(
	"ycsbc_hotspot0.01_144GB"
	"ycsbc_hotspotshifting0.01_144GB"
	"ycsbc_uniform_144GB"
	"ycsbc_zipfian_144GB"
	"hotspot0.01_144GB_read_0.5_insert_0.5"
	"latest_144GB_read_0.5_insert_0.5"
	"uniform_144GB_read_0.5_insert_0.5"
	"zipfian_144GB_read_0.5_insert_0.5"
)
function setup {
	instance_id=$3
	echo Run $1 $2 with instance $instance_id $(./hostname.py $config_file $instance_id)
	./start.py $config_file $instance_id
	IP=$(./ip.py $config_file $instance_id)
	./setup.sh $IP
	./checkout-$2 $IP
}
function run_rocksdb_1 {
	setup $1 $2 $3
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-144GB.sh ../config/$1 ../../data/$1/$2 16GB"
	rsync -zPrt -e ssh root@$IP:~/data/$1 $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$1/$2
	./delete.py $config_file $instance_id
}
function run_hotrap_1 {
	setup $1 $2 $3
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap-144GB.sh ../config/$1 ../../data/$1/$2 16GB 1.44GB"
	rsync -zPrt -e ssh root@$IP:~/data/$1 $output_dir/
	../helper/hotrap-plot.sh $output_dir/$1/$2
	./delete.py $config_file $instance_id
}
suffix=1
function create_instance_if_none {
	if [ $1 ]; then
		instance_id=$1
	else
		while ! ./instance-name-unused.py $config_file "$instance_name_base$suffix"; do
			suffix=$(($suffix+1))
		done
		instance_id=$(./create.py $config_file "$instance_name_base$suffix")
		suffix=$(($suffix+1))
	fi
}
function run_rocksdb {
	# Don't Create instance inside subprocess, otherwise the instance names are likely to collide
	create_instance_if_none $3
	DIR=$output_dir/$1/$2
	mkdir -p $DIR
	run_rocksdb_1 $1 $2 $instance_id > $DIR/aliyun.txt 2>&1 &
}
function run_hotrap {
	# Don't Create instance inside subprocess, otherwise the instance names are likely to collide
	create_instance_if_none $3
	DIR=$output_dir/$1/$2
	mkdir -p $DIR
	run_hotrap_1 $1 $2 $instance_id > $DIR/aliyun.txt 2>&1 &
}

for workload in "${workloads[@]}"; do
	run_rocksdb $workload rocksdb
	run_rocksdb $workload rocksdb-fat
	run_hotrap $workload flush-accessed
	run_hotrap $workload flush-stably-hot
done
wait
