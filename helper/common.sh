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
	cmake .. -DCMAKE_BUILD_TYPE=Release -DROCKSDB_INCLUDE=$HOME/hotrap/include -DROCKSDB_LIB=$HOME/hotrap/build -DVISCNTS_INCLUDE=$HOME/viscnts-splay-rs/include -DVISCNTS_LIB=$HOME/viscnts-splay-rs/target/release
	make
	cd ..
}
function build_kvexe_rocksdb {
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=Release -DROCKSDB_INCLUDE=$HOME/rocksdb/include -DROCKSDB_LIB=$HOME/rocksdb/build
	make
	cd ..
}
