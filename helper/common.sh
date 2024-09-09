build_rocksdb() {
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=None -DCMAKE_C_FLAGS="$CFLAGS -Wall -O2 -g" -DCMAKE_CXX_FLAGS="$CXXFLAGS -Wall -O2 -g" -DUSE_RTTI=true -DFAIL_ON_WARNINGS=OFF -DWITH_TBB=on
	make -j$(nproc) rocksdb-shared
	cd ..
}
build_sas() {
	workspace=$(realpath ..)

	# Additional "FindXXX.cmake" files are here (e.g. FindSodium.cmake)
	CLCMAKE="$workspace/CacheLib/cachelib/cmake"
	CMAKE_PARAMS="-DCMAKE_MODULE_PATH='$CLCMAKE'"

	mkdir -p build
	cd build
	cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DFAIL_ON_WARNINGS=OFF -DUSE_RTTI=true $CMAKE_PARAMS .. -DWITH_TESTS=OFF -DWITH_BENCHMARK_TOOLS=OFF
	make -j$(nproc) rocksdb-shared
	cd ..
}

build_viscnts_splay_rs() {
	make ROCKSDB_INCLUDE=~/hotrap/include
}
build_ralt() {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DROCKSDB_INCLUDE=$workspace/hotrap/include -DROCKSDB_LIB=$workspace/hotrap/build/librocksdb.so $1
	make viscnts
	cd ..
}
build_kvexe_viscnts_splay_rs() {
	mkdir -p build
	cd build
	workspace=$(realpath ../..)
	cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DROCKSDB_INCLUDE=$workspace/hotrap/include -DROCKSDB_LIB=$workspace/hotrap/build -DVISCNTS_INCLUDE=$workspace/viscnts-splay-rs/include -DVISCNTS_LIB=$workspace/viscnts-splay-rs/target/release
	make
	cd ..
}
build_kvexe_ralt() {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DROCKSDB_INCLUDE=$workspace/hotrap/include -DROCKSDB_LIB=$workspace/hotrap/build -DVISCNTS_INCLUDE=$workspace/RALT/include -DVISCNTS_LIB=$workspace/RALT/build
	make
	cd ..
}
build_kvexe_rocksdb() {
	mkdir -p build
	cd build
	workspace=$(realpath ../..)
	cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DROCKSDB_INCLUDE=$workspace/rocksdb/include -DROCKSDB_LIB=$workspace/rocksdb/build
	make
	cd ..
}
build_kvexe_prismdb() {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DROCKSDB_INCLUDE=$workspace/prismdb/include -DROCKSDB_LIB=$workspace/prismdb/build
	make
	cd ..
}
build_kvexe_mutant() {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=Release -DROCKSDB_INCLUDE=$workspace/mutant/include -DROCKSDB_LIB=$workspace/mutant
	make
	cd ..
}
build_kvexe_sas() {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=Release -DROCKSDB_INCLUDE=$workspace/SAS-Cache/include -DROCKSDB_LIB=$workspace/SAS-Cache/build
	make
	cd ..
}
