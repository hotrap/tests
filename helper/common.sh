function build_rocksdb {
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=None -DCMAKE_C_FLAGS="-Wall -O3" -DCMAKE_CXX_FLAGS="-Wall -O3" -DUSE_RTTI=true -DFAIL_ON_WARNINGS=OFF
	make -j$(nproc) rocksdb-shared
	cd ..
}
function build_viscnts_splay_rs {
	make ROCKSDB_INCLUDE=~/hotrap/include
}
function build_viscnts_lsm {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DROCKSDB_INCLUDE=$workspace/hotrap/include -DROCKSDB_LIB=$workspace/hotrap/build/librocksdb.so
	make viscnts
	cd ..
}
function build_kvexe_viscnts_splay_rs {
	mkdir -p build
	cd build
	workspace=$(realpath ../..)
	cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DROCKSDB_INCLUDE=$workspace/hotrap/include -DROCKSDB_LIB=$workspace/hotrap/build -DVISCNTS_INCLUDE=$workspace/viscnts-splay-rs/include -DVISCNTS_LIB=$workspace/viscnts-splay-rs/target/release
	make
	cd ..
}
function build_kvexe_viscnts_lsm {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DROCKSDB_INCLUDE=$workspace/hotrap/include -DROCKSDB_LIB=$workspace/hotrap/build -DVISCNTS_INCLUDE=$workspace/viscnts-lsm/include -DVISCNTS_LIB=$workspace/viscnts-lsm/build
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
