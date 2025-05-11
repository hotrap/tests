#!/usr/bin/env python3
import sys
if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' data-dir')
	exit()
data_dir = sys.argv[1]

import os
import json5
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Paper specific settings
STANDARD_WIDTH = 17.8
SINGLE_COL_WIDTH = STANDARD_WIDTH / 2
DOUBLE_COL_WIDTH = STANDARD_WIDTH
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
    })
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH) * 0.33, cm_to_inch(4.7)), constrained_layout=True)

info = os.path.join(data_dir, 'info.json')
info = json5.load(open(info))
num_scans = pd.read_table(os.path.join(data_dir, 'num-scans'), sep='\s+')
num_scans = num_scans[(num_scans['Timestamp(ns)'] >= info['run-start-timestamp(ns)']) & (num_scans['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]
time = (num_scans['Timestamp(ns)'] - info['run-start-timestamp(ns)']).values / 1e9
time = time[:-1]
total = num_scans['Total']
fd = num_scans['FD']
total = total[1:len(total)].values - total[:len(total) - 1].values
fd = fd[1:len(fd)].values - fd[:len(fd) - 1].values
hit_rates = fd / total

ax = plt.gca()
plt.plot(time, hit_rates)
plt.xlabel('Time (Seconds)', fontsize=8)
plt.ylabel('Range hit rate', fontsize=8)
plt.xticks(fontsize=8)
plt.yticks(np.linspace(0, 1, 6), fontsize=8)

x = time[-1]
y = hit_rates[len(hit_rates) * 99 // 100:len(hit_rates)].mean()
ax.annotate('Final: {:.2f}%'.format(y * 100), xy=(x, y), xytext=(0.5, 0.5), textcoords='axes fraction', arrowprops=dict(arrowstyle="->"), fontsize=8)


plot_dir = data_dir + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/range-hit-rate.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
