for workload in "${workloads[@]}"; do
	if [ ! -f ../config/$workload ]; then
		echo $workload does not exists!
		exit 1
	fi
done

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

function aliyun-run-bg {
	instance_id=$4
	echo $1 $2 $3 with instance $instance_id $(./hostname.py $config_file $instance_id)
	./start.py $config_file $instance_id
	IP=$(./ip.py $config_file $instance_id)
	./setup.sh $IP

	$1 $2 $3 $IP

	./delete.py $config_file $instance_id
}

function aliyun-run {
	if [[ $# < 3 || $# > 4 ]]; then
		echo Usage: $0 command-to-run workload version [instance-id]. workload, version, and instance-ip \(a instance will be created if not provided\) will be passed to \"command-to-run\" as arguments.
		return 1
	fi
	# Don't Create instance inside subprocess, otherwise the instance names are likely to collide
	create_instance_if_none $4
	echo $1 $2 $3 with instance $instance_id $(./hostname.py $config_file $instance_id)
	DIR=$output_dir/$2/$3
	mkdir -p $DIR
	aliyun-run-bg $1 $2 $3 $instance_id > $DIR/aliyun.txt 2>&1 &
}
