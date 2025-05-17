build_rocksdb_common() {
	mkdir -p build
	cd build
	cmake .. -DUSE_RTTI=true -DFAIL_ON_WARNINGS=OFF -DWITH_TBB=on "$@"
	make -j$(nproc) rocksdb-shared
	#make -j$(nproc) rocksdb
	cd ..
}
build_rocksdb() {
	build_rocksdb_common -DCMAKE_BUILD_TYPE=None -DCMAKE_C_FLAGS="$CFLAGS -Wall -O2 -g" -DCMAKE_CXX_FLAGS="$CXXFLAGS -Wall -O2 -g" -DCMAKE_SHARED_LINKER_FLAGS="$LDFLAGS"
}
build_rocksdb_portable() {
	build_rocksdb -DPORTABLE=ON
}
build_rocksdb_debug() {
	build_rocksdb_common -DCMAKE_BUILD_TYPE=Debug -DWITH_ASAN=ON
}

build_db_bench_rocksdb() {
	build_rocksdb
	cd build
	make -j$(nproc) db_bench
	cd ..
}
build_db_bench_ralt() {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DRALT_LIB_DIR=$workspace/RALT/build -DRALT_INCLUDE_DIR=$workspace/RALT/include
	make -j$(nproc) db_bench
	cd ..
}
build_db_bench_viscnts_splay_rs() {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DRALT_LIB_DIR=$workspace/viscnts-splay-rs/target/release-with-debug -DRALT_INCLUDE_DIR=$workspace/viscnts-splay-rs/include
	make -j$(nproc) db_bench
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
	workspace=$(realpath ..)
	make shared_lib_relwithdeb ROCKSDB_INCLUDE=$workspace/hotrap/include
}
build_ralt() {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DROCKSDB_INCLUDE=$workspace/hotrap/include -DROCKSDB_LIB=$workspace/hotrap/build/ "$@"
	make ralt
	cd ..
}
build_ralt_debug() {
	build_ralt -DCMAKE_BUILD_TYPE=Debug -DWITH_ASAN=ON
}

build_kvexe_viscnts_splay_rs() {
	mkdir -p build
	cd build
	workspace=$(realpath ../..)
	cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DROCKSDB_INCLUDE_DIR=$workspace/hotrap/include -DROCKSDB_LIB_DIR=$workspace/hotrap/build -DRALT_INCLUDE_DIR=$workspace/viscnts-splay-rs/include -DRALT_LIB_DIR=$workspace/viscnts-splay-rs/target/release-with-debug
	make
	cd ..
}

build_kvexe_ralt_common() {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DROCKSDB_INCLUDE_DIR=$workspace/hotrap/include -DROCKSDB_LIB_DIR=$workspace/hotrap/build -DRALT_INCLUDE_DIR=$workspace/RALT/include -DRALT_LIB_DIR=$workspace/RALT/build "$@"
	make
	cd ..
}
build_kvexe_ralt() {
	build_kvexe_ralt_common -DCMAKE_BUILD_TYPE=RelWithDebInfo
}
build_kvexe_ralt_debug() {
	build_kvexe_ralt_common -DCMAKE_BUILD_TYPE=Debug -DWITH_ASAN=ON
}

build_kvexe_rocksdb() {
	mkdir -p build
	cd build
	workspace=$(realpath ../..)
	cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DROCKSDB_INCLUDE_DIR=$workspace/rocksdb/include -DROCKSDB_LIB_DIR=$workspace/rocksdb/build
	make
	cd ..
}
build_kvexe_prismdb() {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DROCKSDB_INCLUDE_DIR=$workspace/prismdb/include -DROCKSDB_LIB_DIR=$workspace/prismdb/build
	make
	cd ..
}
build_kvexe_sas() {
	workspace=$(realpath ..)
	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=Release -DROCKSDB_INCLUDE_DIR=$workspace/SAS-Cache/include -DROCKSDB_LIB_DIR=$workspace/SAS-Cache/build
	make
	cd ..
}
build_kvexe_cachelib() {
	workspace=$(realpath ..)

	# Additional "FindXXX.cmake" files are here (e.g. FindSodium.cmake)
	CLCMAKE="$workspace/CacheLib/cachelib/cmake"
	CMAKE_PARAMS="-DCMAKE_MODULE_PATH='$CLCMAKE'"

	mkdir -p build
	cd build
	cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo $CMAKE_PARAMS -DROCKSDB_INCLUDE_DIR=$workspace/rocksdb/include -DROCKSDB_LIB_DIR=$workspace/rocksdb/build
	make
	cd ..
}
