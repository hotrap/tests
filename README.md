# Test scripts for HotRAP

## Prerequisites

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

## Manual work

These directories should be created in the parent directory of this repository (i.e., in `$workspace`):

- `testdb/db`: Store the basic database files. Expected to be a symbolic link to a directory on the fast disk.

- `testdb/fd`: Store LSM-tree files on the fast disk. Expected to be a symbolic link to a directory on the fast disk.

- `testdb/sd`: Store LSM-tree files on the slow disk. Expected to be a symbolic link to a directory on the slow disk.

- `testdb/ralt`: Store the files of RALT. Expected to be a symbolic link to a directory on the fast disk.

Export environment variable `fd_dev` to be the device in iostat that is used as FD.

Export environment variable `sd_dev` to be the device in iostat that is used as SD.

Restart your shell to make changes take effect.

## Process twitter traces

1. Download twitter traces from <http://iotta.snia.org/traces/key-value/28652>

2. For each cluster: `$workspace/tests/helper/process-trace.sh <cluster-ID> $workspace/twitter/processed`. For example, if your workspace is the home directory, for cluster17: `~/tests/helper/process-trace.sh cluster17 ~/twitter/processed`

3. Processing twitter traces can consume hundreds of GBs of memory. Therefore, you may want to process them in a server with large memory and transmit the results to servers that run experiments. An example to transmit the results is shown below.

```shell
server_path=admin@IP:/home/admin/twitter/processed/
rsync -e ssh -zPrpt *.json ${server_path}
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
# Run Twitter tests
bash twitter.sh
# Run YCSB tests
bash 110GB.sh
```
