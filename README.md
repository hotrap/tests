# Test scripts for hotrap

## Prerequisites

Place these repositories in the parent directory of this repository and compile them:

- kvexe-rocksdb: The `rocksdb` branch of [kvexe](https://github.com/hotrap/kvexe).

- kvexe: The `main` branch of [kvexe](https://github.com/hotrap/kvexe).

- [trace-generator](https://github.com/hotrap/trace-generator)

- [YCSB](https://github.com/brianfrankcooper/YCSB/)

These directories should be manually created in the parent directory of this repository:

- `testdb/db`: Store the basic database files

- `testdb/sd`: Speed disk

- `testdb/cd`: Capacity disk

- `testdb/viscnts`: Store the files of VisCnts.

## Run tests

```shell
cd helper
make -j$(nproc)
cd ..
cd plot/helper
make -j$(nproc)
cd ../..
bash test.sh
```
