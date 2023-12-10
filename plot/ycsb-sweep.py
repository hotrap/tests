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

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH), cm_to_inch(4)))

subfigs = [
    {
        'title': '(a) hotspot 5%',
        'ticks': [0, 2e4, 4e4, 6e4],
    },
    {
        'title': '(b) zipfian',
        'ticks': [0, 2e4, 4e4, 6e4],
    },
    {
        'title': '(c) uniform',
        'ticks': [0, 2e4, 4e4, 6e4],
    },
]

workloads=['hotspot0.05', 'zipfian', 'uniform']
ycsb_configs=['ycsbc', 'read_0.75_insert_0.25', 'read_0.5_insert_0.5', 'ycsba']
cluster_labels = ['RO', 'RW', 'WH', 'UH']
versions=[
    {
        'path': 'flush-stably-hot',
        'pattern': '///',
        'color': plt.get_cmap('Set2')(0),
    },
    {
        'path': 'rocksdb-fat',
        'pattern': '\\\\\\',
        'color': plt.get_cmap('Set2')(1),
    },
    {
        'path': 'secondary-cache',
        'pattern': 'XXX',
        'color': plt.get_cmap('Set2')(3),
    },
    {
        'path': 'rocksdb-sd',
        'pattern': 'XXXXXXXXX',
        'color': plt.get_cmap('Set2')(2),
    },
]
version_names = ['HotRAP', 'RocksDB-fat', 'RocksDB-secondary-cache', 'RocksDB(SD)']
size='110GB'

gs = gridspec.GridSpec(1, len(workloads))
bar_width = 0.15
cluster_width = bar_width * len(versions)

for i in range(len(workloads)):
    subfig = plt.subplot(gs[0, i])
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.grid(axis='y')
    workload = workloads[i]
    for (pivot, ycsb) in enumerate(ycsb_configs):
        workload_dir = os.path.join(dir, ycsb + '_' + workload + '_' + size)
        for (version_idx, version) in enumerate(versions):
            data_dir = os.path.join(workload_dir, version['path'])
            x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
            info = json5.load(open(os.path.join(data_dir, 'info.json')))
            run_70p_timestamp = info['run-70%-timestamp(ns)']
            run_end_timestamp = info['run-end-timestamp(ns)']
            progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
            progress = progress[(run_70p_timestamp <= progress['Timestamp(ns)']) & (progress['Timestamp(ns)'] < run_end_timestamp)]
            operations_executed = progress.iloc[-1]['operations-executed'] - progress.iloc[0]['operations-executed']
            seconds = (progress.iloc[-1]['Timestamp(ns)'] - progress.iloc[0]['Timestamp(ns)']) / 1e9
            value = operations_executed / seconds
            ax.bar(x, value, width=bar_width, hatch=version['pattern'], color=version['color'], edgecolor='black', linewidth=0.5)
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-3, 4))
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set_fontsize(8)
    plt.xticks(range(0, len(cluster_labels)), cluster_labels, fontsize=8)
    plt.yticks(subfigs[i]['ticks'], fontsize=8)
    plt.ylim((0, 7e4))
    plt.xlabel(subfigs[i]['title'], labelpad=1, fontsize=8)
    if i == 0:
        plt.ylabel('Operations per second', fontsize=8)
fig.legend(version_names, fontsize=8, ncol=len(versions), loc='center', bbox_to_anchor=(0.5, 0.99))
plt.tight_layout()
pdf_path = dir + '/ycsb-sweep.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
