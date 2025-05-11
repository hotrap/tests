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
SINGLE_COL_WIDTH = 8.5
STANDARD_WIDTH = 17.8
DOUBLE_COL_WIDTH = STANDARD_WIDTH
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
})
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(10)), constrained_layout=True)



version_data = common.VersionData(data_dir)

ax1 = plt.subplot(3, 1, 1)
ax1.grid(axis='y')

ralt_sizes = pd.read_table(os.path.join(data_dir, 'ralt-sizes'), sep='\s+')
(x, real_hot_size) = common.estimate(version_data, ralt_sizes, 'real-hot-size')
real_hot_size = np.array(real_hot_size)

hotspot_sizes = [[0, 0]]
def add_phase(hotspot_size):
    last = hotspot_sizes[-1][0]
    hotspot_sizes.append([last + 1, hotspot_size])
    hotspot_sizes.append([last + 22e7, hotspot_size])
add_phase(0)
add_phase(2.2e9)
add_phase(4.4e9)
add_phase(6.6e9)
add_phase(8.8e9)
add_phase(5.5e9)
add_phase(5.5e9)
add_phase(3.3e9)
add_phase(1.1e9)
hotspot_sizes = np.array(hotspot_sizes)

plt.plot(hotspot_sizes[:,0], hotspot_sizes[:,1] / 1e9, linewidth=1, marker='^', markersize=4, linestyle='dashed')
plt.plot(x, real_hot_size / 1e9, linewidth=1, marker='o', markersize=4, markevery=int(len(x) / 5))
def draw_hotspot_shifts(ax):
    plt.axvline(132e7, linewidth=1, linestyle='--', color='black')
    plt.text(0.66, 1.05, 'Hotspot shifts', transform=ax.transAxes, fontsize=9)
draw_hotspot_shifts(ax1)

plt.ylabel('Size (GB)', fontsize=9)
plt.yticks(fontsize=9)
ax1.yaxis.get_offset_text().set_fontsize(9)
plt.legend(['Hotspot size', 'Hot set size'], frameon=False, fontsize=9, loc='upper left', bbox_to_anchor=(-0.02, 1.07), handletextpad=0.3)
# Turn off ticks on xaxis
plt.tick_params('x', labelbottom=False)


ax2 = plt.subplot(3, 1, 2, sharex=ax1)
ax2.grid(axis='y')

hit_rates = common.read_hit_rates(version_data.data_dir)
(x, hit_rates) = common.estimate(version_data, hit_rates, 'hit-rate')
plt.plot(x, hit_rates, linewidth=1)
draw_hotspot_shifts(ax2)
plt.ylabel('Hit rate', fontsize=9)
plt.yticks(fontsize=9)
# Turn off ticks on xaxis
plt.tick_params('x', labelbottom=False)


ax3 = plt.subplot(3, 1, 3, sharex=ax1)
ax3.grid(axis='y')

def mean_every_n(a, n):
    split = len(a) - len(a) % n
    res = a[0:split].reshape(-1, n).mean(axis=1)
    if split != len(a):
        res = np.append(res, a[split:].mean())
    return res

progress = pd.read_table(data_dir + '/progress', sep='\s+')
info_json = os.path.join(data_dir, 'info.json')
info_json = json5.load(open(info_json))
progress = progress[(progress['Timestamp(ns)'] >= info_json['run-start-timestamp(ns)']) & (progress['Timestamp(ns)'] < info_json['run-end-timestamp(ns)'])]
progress = progress['operations-executed'].values
progress -= progress[0]
ops = progress[1:] - progress[:-1]
progress = progress[:-1]
progress = mean_every_n(progress, mean_step)
ops = mean_every_n(ops, mean_step)

plt.plot(progress, ops, linewidth=1)
draw_hotspot_shifts(ax3)

formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 4))
ax3.yaxis.set_major_formatter(formatter)
ax3.yaxis.get_offset_text().set_fontsize(9)
ax3.set_ylim(bottom=0)
plt.xticks(fontsize=9)
ax3.ticklabel_format(useMathText=True)
ax3.xaxis.get_offset_text().set_fontsize(9)
plt.yticks(fontsize=9)
plt.xlabel('Completed operation count', fontsize=9)
plt.ylabel('Operations per second', fontsize=9)

pdf_path = os.path.join(data_dir, 'plot', 'dynamic-workload.pdf')
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
