#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' data-dir')
	exit()

data_dir = sys.argv[1]
mean_step = 10

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import json5
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Paper specific settings
STANDARD_WIDTH = 17.8
SINGLE_COL_WIDTH = STANDARD_WIDTH / 2
DOUBLE_COL_WIDTH = STANDARD_WIDTH
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
})
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(10)))



version_data = common.VersionData(data_dir)

ax1 = plt.subplot(3, 1, 1)

viscnts_sizes = pd.read_table(os.path.join(data_dir, 'viscnts-sizes'), sep='\s+')
(x, real_hot_size) = common.estimate(version_data, viscnts_sizes, 'real-hot-size')
real_hot_size = np.array(real_hot_size)

hotspot_sizes = np.array([
    [0, 0],
    [22e7, 0],
    [22e7 + 1, 1.1e9],
    [44e7, 1.1e9],
    [44e7 + 1, 3.3e9],
    [66e7, 3.3e9],
    [66e7 + 1, 5.5e9],
    [110e7, 5.5e9],
    [110e7 + 1, 4.4e9],
    [132e7, 4.4e9],
    [132e7 + 1, 2.2e9],
    [154e7, 2.2e9],
])

plt.plot(hotspot_sizes[:,0], hotspot_sizes[:,1] / 1e9, linewidth=0.5, marker='^', markersize=4)
plt.plot(x, real_hot_size / 1e9, linewidth=0.5, marker='o', markersize=4, markevery=int(len(x) / 5))
plt.axvline(88e7, linewidth=0.5, linestyle='--', color='black')
plt.text(0.46, 1.05, 'Hotspot shifts', transform=ax1.transAxes, fontsize=8)

plt.ylabel('Size (GB)', fontsize=8)
plt.yticks(fontsize=8)
ax1.yaxis.get_offset_text().set_fontsize(8)
plt.legend(['Hotspot size', 'Hot set size'], frameon=False, fontsize=8, loc='upper left', bbox_to_anchor=(0.05, 1.05))
# Turn off ticks on xaxis
plt.tick_params('x', labelbottom=False)


ax2 = plt.subplot(3, 1, 2, sharex=ax1)

hit_rates = common.read_hit_rates(version_data.data_dir)
(x, hit_rates) = common.estimate(version_data, hit_rates, 'hit-rate')
plt.plot(x, hit_rates, linewidth=0.5)
plt.axvline(88e7, linewidth=0.5, linestyle='--', color='black')
plt.text(0.46, 1.05, 'Hotspot shifts', transform=ax2.transAxes, fontsize=8)
plt.ylabel('Hit rate', fontsize=8)
plt.yticks(fontsize=8)
# Turn off ticks on xaxis
plt.tick_params('x', labelbottom=False)


ax3 = plt.subplot(3, 1, 3, sharex=ax1)

def mean_every_n(a, n):
    split = len(a) - len(a) % n
    res = a[0:split].reshape(-1, n).mean(axis=1)
    if split != len(a):
        res = np.append(res, a[split:].mean())
    return res

progress = pd.read_table(data_dir + '/progress', delim_whitespace=True)
info_json = os.path.join(data_dir, 'info.json')
info_json = json5.load(open(info_json))
progress = progress[(progress['Timestamp(ns)'] >= info_json['run-start-timestamp(ns)']) & (progress['Timestamp(ns)'] < info_json['run-end-timestamp(ns)'])]
progress = progress['operations-executed'].values
progress -= progress[0]
ops = progress[1:] - progress[:-1]
progress = progress[:-1]
progress = mean_every_n(progress, mean_step)
ops = mean_every_n(ops, mean_step)

plt.plot(progress, ops, linewidth=0.5)
plt.axvline(88e7, linewidth=0.5, linestyle='--', color='black')
plt.text(0.46, 1.05, 'Hotspot shifts', transform=ax3.transAxes, fontsize=8)

formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 4))
ax3.yaxis.set_major_formatter(formatter)
ax3.yaxis.get_offset_text().set_fontsize(8)
ax3.set_ylim(bottom=0)
plt.xticks(fontsize=8)
ax3.ticklabel_format(useMathText=True)
ax3.xaxis.get_offset_text().set_fontsize(8)
plt.yticks(fontsize=8)
plt.xlabel('Completed operation count', fontsize=8)
plt.ylabel('Operations per second', fontsize=8)

pdf_path = os.path.join(data_dir, 'plot', 'dynamic-workload.pdf')
plt.tight_layout(pad=0.8)
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
