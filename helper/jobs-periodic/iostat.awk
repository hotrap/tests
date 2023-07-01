{
	if ("nvme0n1" == $1)
		printf "%s %s %s ",$2,$3,$4
	if ("sda" == $1) {
		print $2,$3,$4
		fflush(stdout)
	}
}
