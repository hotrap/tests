function hotspot-op {
	if [ ! -s $1 ]; then
		echo 0
	fi
	n=$(tail -n1 $1 | cut -sd" " -f1)
	i=$(echo $n / 20 | bc)
	hotspot_opn=$(sed -n "${i}p" $1 | cut -sd" " -f2)
	opn=$(tail -n1 $1 | cut -sd" " -f2)
	echo $hotspot_opn / $opn | bc -l
}
