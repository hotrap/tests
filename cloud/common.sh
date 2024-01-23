function check-workload-files {
	for workload in "$@"; do
		if [ ! -f ../config/$workload ]; then
			echo $workload does not exists!
			exit 1
		fi
	done
}
check-workload-files "${workloads[@]}"

vendor=$(cat $config_file | jq -er ".vendor")
if [ "$vendor" == 'aliyun' ]; then
	suffix=1
	instance_name_prefix=$(cat $config_file | jq -er ".instance_name_prefix")
	function create_instance_if_none {
		if [ $1 ]; then
			instance_id=$1
		else
			while ! ./aliyun/instance-name-unused.py $config_file "$instance_name_prefix$suffix"; do
				suffix=$(($suffix+1))
			done
			instance_id=$(./aliyun/create.py $config_file "$instance_name_prefix$suffix")
			suffix=$(($suffix+1))
		fi
	}
else
	function create_instance_if_none {
		if [ $1 ]; then
			instance_id=$1
		else
			instance_id=$(./aws/create.py $config_file)
		fi
	}
fi

function cloud-run-bg {
	instance_id=$4
	echo $1 $2 $3 with instance $instance_id
	if [ "$vendor" == "aliyun" ]; then
		./aliyun/start.py $config_file $instance_id
	else
		./aws/start.py $instance_id
	fi
	if [ "$vendor" == "aliyun" ]; then
		IP=$(./aliyun/ip.py $config_file $instance_id)
	else
		IP=$(./aws/ip.py $instance_id)
	fi

	# https://stackoverflow.com/questions/21383806/how-can-i-force-ssh-to-accept-a-new-host-fingerprint-from-the-command-line
	ssh-keygen -R $IP
	# https://unix.stackexchange.com/questions/33271/how-to-avoid-ssh-asking-permission
	while ! ssh $user@$IP -o StrictHostKeyChecking=no "true"; do
		sleep 1
	done
	ssh $user@$IP "sudo apt update"
	ssh $user@$IP "bash -s" -- < ../apt.sh
	ssh $user@$IP "bash -s" -- < helper/cloud.sh
	ssh $user@$IP "bash -s" -- < helper/$vendor.sh
	rsync -zPrL -e ssh .. $user@$IP:~/tests --exclude='target'

	ssh $user@$IP -o ServerAliveInterval=60 "rm -rf data/$2/$3"

	$1 $2 $3 $IP

	if [ "$vendor" == "aliyun" ]; then
		./aliyun/delete.py $config_file $instance_id
	else
		./aws/delete.py $instance_id
	fi
}

function cloud-run {
	if [[ $# < 3 || $# > 4 ]]; then
		echo Usage: $0 command-to-run workload version [instance-id]. workload, version, and instance-ip \(a instance will be created if not provided\) will be passed to \"command-to-run\" as arguments.
		return 1
	fi
	# Don't Create instance inside subprocess, otherwise the instance names are likely to collide
	create_instance_if_none $4
	echo -n "$1 $2 $3 with instance $instance_id "
	if [ "$vendor" == 'aliyun' ]; then
		./aliyun/hostname.py $config_file $instance_id
	else
		./aws/ip.py $instance_id
	fi
	DIR=$output_dir/$2/$3
	mkdir -p $DIR
	cloud-run-bg $1 $2 $3 $instance_id > $DIR/$vendor.txt 2>&1 &
}
