mkdir $DIR
cp $workload_file $DIR/workload
cp ~/testdb/db/{LOG,log.txt,cpu,first-level-in-cd,progress,promoted-*,rocksdb-stats.txt,period_stats,latency*} $DIR/
cp ~/testdb/log/* $DIR/



mkdir -p $DIR/plot/
~/tests/plot/du.py $DIR &
~/tests/plot/ops.py $DIR 10 &
~/tests/plot/tps.py $DIR 1 &
~/tests/plot/throughput.py $DIR 10 &
~/tests/plot/hit.py $DIR &
~/tests/plot/promoted-bytes.py $DIR &
~/tests/helper/calc-latency.sh $DIR &
#~/tests/plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
cd $DIR/plot
rm all.pdf
pdfunite *.pdf all.pdf
