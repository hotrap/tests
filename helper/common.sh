function build_rocksdb {
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_RTTI=true
	make -j$(nproc) rocksdb-shared
	cd ..
}
function build_viscnts_splay_rs {
	make ROCKSDB_INCLUDE=~/hotrap/include
}
function build_kvexe {
	mkdir -p build
	cd build
	workspace=$(realpath ../..)
	cmake .. -DCMAKE_BUILD_TYPE=Release -DROCKSDB_INCLUDE=$workspace/hotrap/include -DROCKSDB_LIB=$workspace/hotrap/build -DVISCNTS_INCLUDE=$workspace/viscnts-splay-rs/include -DVISCNTS_LIB=$workspace/viscnts-splay-rs/target/release
	make
	cd ..
}
function build_kvexe_rocksdb {
	mkdir -p build
	cd build
	workspace=$(realpath ../..)
	cmake .. -DCMAKE_BUILD_TYPE=Release -DROCKSDB_INCLUDE=$workspace/rocksdb/include -DROCKSDB_LIB=$workspace/rocksdb/build
	make
	cd ..
}
