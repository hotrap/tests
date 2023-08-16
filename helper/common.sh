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
	conan build . --options ROCKSDB_INCLUDE=$HOME/hotrap/include --options ROCKSDB_LIB=$HOME/hotrap/build --options VISCNTS_INCLUDE=$HOME/viscnts-splay-rs/include --options VISCNTS_LIB=$HOME/viscnts-splay-rs/target/release
}
