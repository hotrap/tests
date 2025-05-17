# Test scripts for HotRAP

## Prerequisites

### Find a workspace

For example, if you want to place all the stuff of this project in the home directory:

```shell
workspace=~
```

If you prefer to put everything in a subdirectory:

```shell
mkdir ~/hotrap
workspace=~/hotrap
```

### Clone this repo

```shell
cd $workspace
git clone https://github.com/hotrap/tests.git
cd tests
cd setup
```

### `./apt.sh`

### `./pip.sh`

For some Linux distros, a virtual environment for python3 is mandatory for pip3 to work, and you may encounter this error message:

```txt
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.11/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

If you don't have a virtual environment yet, we provide a simple way to install one:

```shell
python3 -m venv ~/.venvs/base
echo ". ~/.venvs/base/bin/activate" >> ~/.profile
. ~/.profile
```

Then `pip.sh` should work fine.

### Rust

```shell
./rustup.sh
. ~/.cargo/env
```

Chinese users may prefer installing Rust with `rsproxy.cn`:

```shell
./rustup-cn.sh
. ~/.profile
```

### `./setup.sh`

This script downloads the source code and compiles CacheLib. It may take up to an hour to complete.

### Specify the fast disk and the slow disk

This part is hardware-specific. In general, you need to perform the following steps:

Create the following directories in `$workspace`:

- `testdb/db`: Stores the basic database files. Expected to be a symbolic link to a directory on the fast disk.

- `testdb/fd`: Stores LSM-tree files on the fast disk. Expected to be a symbolic link to a directory on the fast disk.

- `testdb/sd`: Stores LSM-tree files on the slow disk. Expected to be a symbolic link to a directory on the slow disk.

- `testdb/ralt`: Stores the files of RALT. Expected to be a symbolic link to a directory on the fast disk.

Export environment variable `fd_dev` to be the device in iostat that is used as FD.

Export environment variable `sd_dev` to be the device in iostat that is used as SD.

Restart your shell to make changes take effect.

#### AWS i4i.2xlarge instances

Our experiments are conducted using AWS i4i.2xlarge instances. For i4i.2xlarge instances, the fast disk is `nvme1n1` and the slow disk is `nvme0n1`. You may specify them using the following commands. Before doing so, please make sure that there is no data in the fast disk.

```shell
# !!!! Please make sure there is no data in /dev/nvme1n1 !!!!

# The slow disk has been used by the root file system, so you only need to format and mount the fast disk
sudo mkfs.ext4 /dev/nvme1n1
sudo mkdir -p /mnt/fd
sudo mount /dev/nvme1n1 /mnt/fd
sudo chown $USER:$USER /mnt/fd
mkdir /mnt/fd/{db,fd,ralt}

# Link the directories to testdb
mkdir ~/testdb
ln -s /mnt/fd/{db,fd,ralt} ~/testdb/

# The root file system is already on the slow disk
mkdir ~/testdb/sd

# Set the environment variables
cat >> ~/.profile <<EOF
export fd_dev=nvme1n1
export sd_dev=nvme0n1
EOF
. ~/.profile
```

## Obtain Twitter traces

You may skip this step if you don't need to run `twitter.sh`.

### Download processed Twitter traces

The downloaded files should be placed under `$workspace/twitter/processed`.

Some zst files exceeds the 4GB file size limit of TeraBox / Baidu Netdisk, so we split them into 1GB files with digital suffixes like `file.zstXX`. You can combine them into the original zst file with `cat file.zst* > file.zst`.

We only uploaded traces necessary to reproduce our results in paper. Please contact us or file an issue if you need processed traces of other Twitter traces.

#### TeraBox

<https://1024terabox.com/s/1cwU2x_Ux8tDUKG3CII-lQQ>

#### Baidu Netdisk

<https://pan.baidu.com/s/1y9se6aUlgQw26L5gg4sjGw?pwd=fika>

access code: `fika`

Note: the interface is only available in Chinese.

### Process Twitter traces by yourself

1. Download Twitter traces from <http://iotta.snia.org/traces/key-value/28652>

2. For each cluster: `$workspace/tests/helper/process-trace.sh <cluster-ID> $workspace/twitter/processed`. To process all traces:

```shell
# cd to the directory where original twitter traces are in
for i in $(seq 1 54); do
	$workspace/tests/helper/process-trace.sh cluster$(printf "%02d" $i) $workspace/twitter/processed
done
```

4. Processing twitter traces can consume hundreds of GBs of memory. Therefore, you may want to process them in a server with large memory and transmit the results to servers that run experiments. An example to transmit the results is shown below.

```shell
server_path=admin@IP:/home/admin/twitter/processed/
rsync -e ssh -zPrpt *.json ${server_path}
rsync -e ssh -zPrpt stats/*.json ${server_path}/stats/
rsync -e ssh -zPrpt stats/*-read-hot-5p-read ${server_path}/stats/
rsync -e ssh -zPrpt stats/*-read-with-more-than-5p-write-size ${server_path}/stats/
workloads=(
	"cluster02-283x"
	"cluster10"
	"cluster11-25x"
	"cluster15"
	"cluster16-67x"
	"cluster17-80x"
	"cluster18-186x"
	"cluster19-3x"
	"cluster22-9x"
	"cluster23"
	"cluster29"
	"cluster46"
	"cluster48-5x"
	"cluster51-175x"
	"cluster53-12x"
)
for workload in "${workloads[@]}"; do
	rsync -e ssh -zPrpt $workload-*.zst ${server_path}
done
```

## Run tests on a local machine

You may want to comment out systems or workloads that you don't want to test.

```shell
cd workloads
# Figure 8
$workspace/tests/plot/twitter-scatter.py $workspace/data $workspace/twitter/processed
# Figure 9, Figure 10. About a week.
bash twitter.sh
$workspace/tests/tools/draw.sh $workspace/data
# Figure 6, Figure 11, Figure 12. About 9 days.
bash 200B.sh
$workspace/tests/tools/draw.sh $workspace/data
# Figure 5, Figure 7, Figure 13, Figure 14, Table 4, Table 5. About 11 days.
bash 110GB.sh
$workspace/tests/tools/draw.sh $workspace/data
# Figure 15. About a month.
bash 1.1TB.sh
$workspace/tests/tools/draw.sh $workspace/data
```

## Run tests in parallel with an AWS access key

Running all tests on a single machine costs more than a month. Reproducing all results in a shorter time requires an AWS access key to create instances automatically and run tests on these instances simultaneously. An automatically created instance will be automatically terminated after the test running on it is finished.

### Setup a central node

The central node is responsible for creating and terminating instances automatically. Experiment results will be transmitted and stored in the central node before a worker instance is terminated. The central node should also be configured following the instructions in [Prerequisites](#prerequisites), so that source code can be directly copied to worker instances in the future.

### Obtain an AWS access key

In the AWS EC2 console, click the drop-down menu in the upper right corner, click `Security credentials` in it, click `Create access key`, and then you obtain the access key and secret key.

In the central node:

```shell
mkdir ~/.aws
```

Create a file `~/.aws/credentials`, put your access key and secret key there:

```text
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region = YOUR_REGION
```

### Create a config file

`$workspace/config.json`:

```json
{
	"vendor": "aws",
	"ImageId": "ami-xxxxxx",
	"KeyName": "your-ssh-key-name",
	"SecurityGroupId": "sg-xxxxx",
	"user": "admin",
	"InstanceName": "atc25-hotrap-ae"
}
```

### Run tests

Note that running all tests may cost one to two thousand dollars.

We recommend running these scripts in `tmux`. You can simultaneously run these scripts in different tmux sessions, and we recommend running each script in a different session.

Create a tmux session:

```shell
# If you want to run 110GB.sh in this session, you can name the session as "110GB"
tmux new -s "session-name"
```

`ctrl+b` then `d` to detach from the session.

`tmux ls` to list all sessions.

`tmux a -t "session-name"` to reconnect to the session.

Each script requires an argument `max-running-instances`, which restricts the maximum number of live worker instances for that script. For example, if you set it to 16, the script will first create 16 worker instances. A new worker instance will not be created until a previously running worker instance terminates. We set the argument to 16 in the examples below.

```shell
cd $workspace/tests/cloud
# Figure 9, Figure 10
bash twitter.sh $workspace/config.json $workspace/data 16
# Figure 6, Figure 11, Figure 12
bash 200B.sh $workspace/config.json $workspace/data 16
# Figure 5, Figure 7, Figure 13, Figure 14, Table 4, Table 5
bash 110GB.sh $workspace/config.json $workspace/data 16
# Figure 15
bash 1.1TB.sh $workspace/config.json $workspace/data 16
```

## Process results

```shell
# Figure 8
$workspace/tests/plot/twitter-scatter.py $workspace/data $workspace/twitter/processed
# Other figures and tables:
$workspace/tests/tools/draw.sh $workspace/data
```

Some figures can be partially generated based on available results, i.e., corresponding data points will be absent if some results are not available.

```shell
cd $workspace/data
# Figure 9
$workspace/tests/tools/draw-twitter-speedup.sh
# Figure 10
$workspace/tests/tools/draw-twitter-ops.sh
# Figure 6, Figure 11, Figure 12
$workspace/tests/tools/draw-200B.sh
```

## Notes

- The `du` warnings like `du: cannot access 'fd/003409.sst': No such file or directory` are expected and can be safely ignored.
