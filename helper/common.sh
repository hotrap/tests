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
	cmake .. -DCMAKE_BUILD_TYPE=Release -DROCKSDB_INCLUDE=../../hotrap/include -DROCKSDB_LIB=../../hotrap/build -DVISCNTS_INCLUDE=../../viscnts-splay-rs/include -DVISCNTS_LIB=../../viscnts-splay-rs/target/release
	make
	cd ..
}
function build_kvexe_rocksdb {
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=Release -DROCKSDB_INCLUDE=../../rocksdb/include -DROCKSDB_LIB=../../rocksdb/build
	make
	cd ..
}
