#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

fontsize=9
fonten = {'family': 'Times New Roman', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

d = sys.argv[1]

first_level_in_cd = int(open(d + '/first-level-in-cd').read())

timestamps = []
hit_rates = []
last_tier0 = 0
last_total = 0
for line in open(d + '/num-accesses'):
	res = line.split(' ')
	timestamp = int(res[0])
	tier0 = 0
	total = 0
	for (level, num_accesses) in enumerate(res[1:]):
		num_accesses = int(num_accesses)
		total += num_accesses
		if level < first_level_in_cd:
			tier0 += num_accesses
	if total - last_total != 0:
		timestamps.append(timestamp)
		hit_rates.append((tier0 - last_tier0) / (total - last_total))
		last_tier0 = tier0
		last_total = total

time = (np.array(timestamps) - timestamps[0]) / 1e9

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/hit-rate.pdf'
plt.plot(time, hit_rates)
plt.xlabel('Time')
plt.ylabel('Hit rate')
plt.title('Hit rate')
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
