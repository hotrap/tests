import os
import json5
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import common

def draw_throughput_breakdown(dir, versions, mean_step, linewidth, num_marks, markersize, markersize_x):
	gs = gridspec.GridSpec(1, len(versions))
	for (i, version) in enumerate(versions):
		subfig = plt.subplot(gs[0, i])
		ax = plt.gca()
		ax.set_axisbelow(True)
		ax.grid(axis='y')
		data_dir = os.path.join(dir, version['path'])

		first_level_in_cd = int(open(data_dir + '/first-level-in-cd').read())
		info = os.path.join(data_dir, 'info.json')
		info = json5.load(open(info))
		def read_table(file):
			iostat_raw = pd.read_table(file, delim_whitespace=True)
			iostat_raw = iostat_raw[(iostat_raw['Timestamp(ns)'] >= info['run-start-timestamp(ns)']) & (iostat_raw['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]
			iostat_raw['Time(Seconds)'] = (iostat_raw['Timestamp(ns)'] - iostat_raw['Timestamp(ns)'].iloc[0]) / 1e9
			iostat = iostat_raw[['rkB/s', 'wkB/s']].groupby(iostat_raw.index // mean_step).mean()
			iostat['Time(Seconds)'] = iostat_raw['Time(Seconds)'].groupby(iostat_raw.index // mean_step).first()
			return iostat
		sd = read_table(data_dir + '/iostat-sd.txt')
		cd = read_table(data_dir + '/iostat-cd.txt')

		compaction_bytes = common.read_compaction_bytes_sd_cd(data_dir, first_level_in_cd)
		timestamps = np.array(compaction_bytes['Timestamp(ns)'])
		run_phase = (timestamps >= info['run-start-timestamp(ns)']) & (timestamps < info['run-end-timestamp(ns)'])
		timestamps = timestamps[run_phase]
		compaction_bytes = compaction_bytes[run_phase]
		time = (timestamps[1:] - info['run-start-timestamp(ns)']) / 1e9

		throughput = compaction_bytes[1:].values - compaction_bytes[:-1].values
		throughput = throughput[:,1:] / (throughput[:,0][:, np.newaxis] / 1e9)
		throughput = pd.DataFrame(throughput, columns=['sd-read', 'sd-write', 'cd-read', 'cd-write'])
		throughput['Time(Seconds)'] = time
		throughput = throughput.groupby(throughput.index // mean_step).mean()

		markevery = int(len(sd['Time(Seconds)']) / num_marks)
		ax.plot(sd['Time(Seconds)'], (sd['rkB/s'] + sd['wkB/s']) / 1e3, marker='o', linewidth=linewidth, markersize=markersize, markevery=markevery)
		ax.plot(sd['Time(Seconds)'], (cd['rkB/s'] + cd['wkB/s']) / 1e3, marker='D', linewidth=linewidth, markersize=markersize, markevery=markevery)
		markevery = int(len(throughput['Time(Seconds)']) / num_marks)
		ax.plot(throughput['Time(Seconds)'], (throughput['sd-read'] + throughput['sd-write']) / 1e6, marker='s', linewidth=linewidth, markersize=markersize, markevery=markevery)
		ax.plot(throughput['Time(Seconds)'], (throughput['cd-read'] + throughput['cd-write']) / 1e6, marker='x', linewidth=linewidth, markersize=markersize_x, markevery=markevery)

		rand_read_bytes = common.read_rand_read_bytes_sd_cd(data_dir, first_level_in_cd)
		rand_read_bytes = rand_read_bytes[(info['run-start-timestamp(ns)'] <= rand_read_bytes['Timestamp(ns)']) & (rand_read_bytes['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]
		time = (rand_read_bytes['Timestamp(ns)'][1:] - info['run-start-timestamp(ns)']) / 1e9
		rand_read_bytes = rand_read_bytes['sd'] + rand_read_bytes['cd']
		throughput = rand_read_bytes[1:].values - rand_read_bytes[:-1].values
		get_throughput = pd.DataFrame({
			'Time(s)': time,
			'Throughput(B/s)': throughput,
		})
		get_throughput = get_throughput.groupby(get_throughput.index // mean_step).mean()
		ax.plot(get_throughput['Time(s)'], get_throughput['Throughput(B/s)'] / 1e6, color='black', linestyle='dashed', marker='^', linewidth=linewidth, markersize=markersize, markevery=markevery)
		subfig.text(0.5, -0.29, 'Time (Seconds)', fontsize=6, ha='center', va='center', transform=subfig.transAxes)
		plt.xticks(fontsize=8)
		plt.yticks(fontsize=8)
		plt.xlabel(version['name'], labelpad=8, fontsize=8)
		if i == 0:
			plt.ylabel('Throughput (MB/s)', fontsize=8)
