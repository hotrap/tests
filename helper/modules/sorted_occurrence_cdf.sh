sorted_occurrence_cdf() {
	frawk '
		{
			if (NR == 1) {
				last = $1
			} else if ($1 != last) {
				print last, NR - 1;
				last = $1
			}
		}
		END {
			print last, NR
		}
	'
}
