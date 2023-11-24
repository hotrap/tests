#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

dir=sys.argv[1]

import os
import math
import json5
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter

# Paper specific settings
STANDARD_WIDTH = 17.8
SINGLE_COL_WIDTH = STANDARD_WIDTH / 2
DOUBLE_COL_WIDTH = STANDARD_WIDTH
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
    })
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(4)))

colormap = 'Set2'
patterns = ['///', '\\\\\\', '', 'XXX', '---']

workload='hotspot0.05'
ycsb_configs=['ycsba', 'read_0.5_insert_0.5', 'ycsbc', 'ycsbd', 'ycsbf']
cluster_labels = ['A', 'A\'', 'C', 'D', 'F']
versions=['flush-stably-hot', 'rocksdb-sd']
size='110GB'

gs = gridspec.GridSpec(1, 2)
bar_width = 1 / (len(versions) + 1)
cluster_width = bar_width * len(versions)

subfig = plt.subplot(gs[0, 0])
ax = plt.gca()
ax.set_axisbelow(True)
ax.grid(axis='y')
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
ax.yaxis.get_offset_text().set_fontsize(8)
for (pivot, ycsb) in enumerate(ycsb_configs):
    workload_dir = os.path.join(dir, ycsb + '_' + workload + '_' + size)
    for (version_idx, version) in enumerate(versions):
        data_dir = os.path.join(workload_dir, version)
        x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
        info = json5.load(open(os.path.join(data_dir, 'info.json')))
        run_70p_timestamp = info['run-70%-timestamp(ns)']
        run_end_timestamp = info['run-end-timestamp(ns)']
        cpu = pd.read_table(os.path.join(data_dir, 'cpu'), delim_whitespace=True, names=['Timestamp(s)', 'util'])
        cpu = cpu[(run_70p_timestamp <= cpu['Timestamp(s)'] * 1e9) & (cpu['Timestamp(s)'] * 1e9 < run_end_timestamp)]
        cputime = cpu['util'].sum() / 100
        ax.bar(x, cputime, width=bar_width, hatch=patterns[version_idx], color=plt.get_cmap(colormap)(version_idx), edgecolor='black', linewidth=0.5)
plt.xticks(range(0, len(cluster_labels)), cluster_labels, fontsize=8)
plt.yticks(fontsize=8)
plt.locator_params(axis='y', nbins=4)
plt.ylabel('CPU time (seconds)', fontsize=8)

plt.subplot(gs[0, 1])
ax = plt.gca()
ax.set_axisbelow(True)
ax.grid(axis='y')
for (pivot, ycsb) in enumerate(ycsb_configs):
    workload_dir = os.path.join(dir, ycsb + '_' + workload + '_' + size)
    for (version_idx, version) in enumerate(versions):
        data_dir = os.path.join(workload_dir, version)
        x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
        info = json5.load(open(os.path.join(data_dir, 'info.json')))
        run_70p_timestamp = info['run-70%-timestamp(ns)']
        run_end_timestamp = info['run-end-timestamp(ns)']
        def run_time_io_kB(fname):
            iostat = pd.read_table(os.path.join(data_dir, fname), delim_whitespace=True)
            iostat = iostat[(run_70p_timestamp <= iostat['Timestamp(ns)']) & (iostat['Timestamp(ns)'] < run_end_timestamp)]
            return iostat[['rkB/s', 'wkB/s']].sum().sum()
        io_TB = (run_time_io_kB('iostat-sd.txt') + run_time_io_kB('iostat-cd.txt')) / 1e9
        ax.bar(x, io_TB, width=bar_width, hatch=patterns[version_idx], color=plt.get_cmap(colormap)(version_idx), edgecolor='black', linewidth=0.5)
plt.xticks(range(0, len(cluster_labels)), cluster_labels, fontsize=8)
plt.yticks(fontsize=8)
plt.ylabel('Total read/write data (TB)', fontsize=8)

fig.legend(['HotRAP', 'RocksDB(SD)'], fontsize=8, ncol=len(versions), loc='center', bbox_to_anchor=(0.5, 0.98))
plt.tight_layout()
pdf_path = dir + '/all-in-sd.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
