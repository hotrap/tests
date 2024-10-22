# Test scripts for HotRAP

## Install dependencies

Note: `setup.sh` currently doesn't work because we make the repositories private for anonymity.

```shell
./apt.sh
./setup.sh
```

## Manual work

These directories should be created in the parent directory of this repository:

- `testdb/db`: Store the basic database files. Expected to be a symbolic link to a directory on the fast disk.

- `testdb/fd`: Store LSM-tree files on the fast disk. Expected to be a symbolic link to a directory on the fast disk.

- `testdb/sd`: Store LSM-tree files on the slow disk. Expected to be a symbolic link to a directory on the slow disk.

- `testdb/ralt`: Store the files of RALT. Expected to be a symbolic link to a directory on the fast disk.

Export environment variable `fd_dev` to be the device in iostat that is used as FD.

Export environment variable `sd_dev` to be the device in iostat that is used as SD.

Restart your shell to make changes take effect.

## Run tests on a local machine

You may want to comment out systems or workloads that you don't want to test.

```shell
cd workloads
# Run YCSB tests
bash 110GB.sh
# Run Twitter tests
bash twitter.sh
```
