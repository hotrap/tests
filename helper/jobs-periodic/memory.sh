pid=$(pidof rocksdb-kvexe)
while : ; do date; pmap -x $pid | grep "total kB"; sleep 1; done
