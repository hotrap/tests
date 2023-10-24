# Test scripts for hotrap

## Prerequisites

Place these repositories in the parent directory of this repository and compile them:

- kvexe-rocksdb: The `rocksdb` branch of [kvexe](https://github.com/hotrap/kvexe).

- kvexe: The `main` branch of [kvexe](https://github.com/hotrap/kvexe).

These directories should be manually created in the parent directory of this repository:

- `testdb/db`: Store the basic database files

- `testdb/sd`: Speed disk

- `testdb/cd`: Capacity disk

- `testdb/viscnts`: Store the files of VisCnts.

## Run tests

```shell
cd workloads
bash 200GB.sh
```
