function check-workload-files {
	for workload in "$@"; do
		if [ ! -f ../config/$workload ]; then
			echo $workload does not exists!
			exit 1
		fi
	done
}

vendor=$(cat $config_file | jq -er ".vendor")
if [ "$vendor" == 'aliyun' ]; then
	suffix=1
fi

function cloud-run-bg {
	instance_id=$1
	echo ${@:2} with instance $instance_id

	if [ "$vendor" == "aliyun" ]; then
		command="./aliyun/delete.py $config_file $instance_id"
	else
		command="./aws/delete.py $instance_id"
	fi
	(
		trap "pkill -P $BASHPID; echo $command; $command" EXIT
		(
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

			# https://unix.stackexchange.com/questions/33271/how-to-avoid-ssh-asking-permission
			while ! flock ~/.ssh/known_hosts ssh $user@$IP -o StrictHostKeyChecking=accept-new "true"; do
				# https://stackoverflow.com/questions/21383806/how-can-i-force-ssh-to-accept-a-new-host-fingerprint-from-the-command-line
				flock ~/.ssh/known_hosts ssh-keygen -R $IP
				sleep 1
			done
			ssh $user@$IP "sudo apt update"
			ssh $user@$IP "sh -s" -- < ../setup/apt.sh
			rsync -zrpL --partial -e ssh .. $user@$IP:~/tests --exclude='target'
			ssh $user@$IP "./tests/cloud/helper/$vendor.sh"
			ssh $user@$IP "./tests/cloud/helper/cloud.sh"

			ssh $user@$IP -o ServerAliveInterval=60 "rm -rf data/$3/$4"

			$2 $3 $4 $IP ${@:5}
	 	) &
		wait
	)
}

function run-with-instance {
	instance_id=$1
	echo -n "${@:2} with instance $instance_id "
	if [ "$vendor" == 'aliyun' ]; then
		./aliyun/hostname.py $config_file $instance_id
	else
		echo
	fi
	DIR=$output_dir/$3/$4
	mkdir -p $DIR
	cloud-run-bg $* > $DIR/$vendor.txt 2>&1 &
}

function cloud-run {
	if [ ! "$max_running_instances" ]; then
		echo "max_running_instances not set!"
		return 1
	fi
	if [[ $# < 3 ]]; then
		echo Usage: $0 command-to-run workload version other-arguments. workload, version, instance-ip, and other arguments will be passed to \"command-to-run\" as arguments.
		return 1
	fi

	if [ ! "$num_running_instances" ]; then
		num_running_instances=1
	elif [ "$num_running_instances" -lt "$max_running_instances" ]; then
		num_running_instances=$(("$num_running_instances" + 1))
	else
		wait -n
	fi

	# Don't Create instance inside subprocess, otherwise the instance names are likely to collide
	if [ "$vendor" == 'aliyun' ]; then
		instance_name_prefix=$(cat $config_file | jq -er ".instance_name_prefix")
		while ! ./aliyun/instance-name-unused.py $config_file "$instance_name_prefix$suffix"; do
			suffix=$(($suffix+1))
		done
		instance_id=$(./aliyun/create.py $config_file "$instance_name_prefix$suffix")
		suffix=$(($suffix+1))
	else
		instance_id=$(./aws/create.py $config_file)
	fi

	if [ ! "$instance_id" ]; then
		echo Fail to create instance
		return 1
	fi
	run-with-instance $instance_id $*
}
