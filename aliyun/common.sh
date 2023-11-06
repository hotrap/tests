for workload in "${workloads[@]}"; do
	if [ ! -f ../config/$workload ]; then
		echo $workload does not exists!
		exit 1
	fi
done

function setup {
	instance_id=$3
	echo Run $1 $2 with instance $instance_id $(./hostname.py $config_file $instance_id)
	./start.py $config_file $instance_id
	IP=$(./ip.py $config_file $instance_id)
	./setup.sh $IP
	./checkout-$2 $IP
}

suffix=1
function create_instance_if_none {
	if [ $1 ]; then
		instance_id=$1
	else
		while ! ./instance-name-unused.py $config_file "$instance_name_prefix$suffix"; do
			suffix=$(($suffix+1))
		done
		instance_id=$(./create.py $config_file "$instance_name_prefix$suffix")
		suffix=$(($suffix+1))
	fi
}

function run_rocksdb {
	# Don't Create instance inside subprocess, otherwise the instance names are likely to collide
	create_instance_if_none $3
	echo Run $1 $2 with instance $instance_id $(./hostname.py $config_file $instance_id)
	DIR=$output_dir/$1/$2
	mkdir -p $DIR
	run_rocksdb_1 $1 $2 $instance_id > $DIR/aliyun.txt 2>&1 &
}
function run_hotrap {
	# Don't Create instance inside subprocess, otherwise the instance names are likely to collide
	create_instance_if_none $3
	echo Run $1 $2 with instance $instance_id $(./hostname.py $config_file $instance_id)
	DIR=$output_dir/$1/$2
	mkdir -p $DIR
	run_hotrap_1 $1 $2 $instance_id > $DIR/aliyun.txt 2>&1 &
}

