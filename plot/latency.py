#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()
dir = sys.argv[1]

import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import LogLocator

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

tests = [
    {
        'title': '(a) YCSB-A\' hotspot-5% insert latency',
        'workload': 'read_0.5_insert_0.5_hotspot0.05_110GB',
        'workload-name': 'read-0.5-insert-0.5-hotspot',
        'operation': 'read',
    },
    {
        'title': '(b) YCSB-A\' hotspot-5% read latency',
        'workload': 'read_0.5_insert_0.5_hotspot0.05_110GB',
        'workload-name': 'read-0.5-insert-0.5-hotspot',
        'operation': 'insert',
    },
    {
        'title': '(c) YCSB-C hotspot-5% read latency',
        'workload': 'ycsbc_hotspot0.05_110GB',
        'workload-name': 'ycsbc-hotspot',
        'operation': 'read',
    },
]
versions=[
    {
        'path': 'flush-stably-hot',
        'color': plt.get_cmap('Set2')(0),
        'marker': 'o',
    },
    {
        'path': 'rocksdb-fat',
        'color': plt.get_cmap('Set2')(1),
        'marker':'^',
    },
    {
        'path': 'secondary-cache',
        'color': plt.get_cmap('Set2')(3),
        'marker': 's',
    },
    {
        'path': 'rocksdb-sd',
        'color': plt.get_cmap('Set2')(2),
        'marker':'x',
    },
]
version_names = ['HotRAP', 'RocksDB-fat', 'RocksDB-secondary-cache', 'RocksDB(SD)']
percentiles = [50, 60, 70, 80, 90, 95, 99, 99.9]

gs = gridspec.GridSpec(1, len(tests))
bar_width = 1 / (len(versions) + 1)
cluster_width = bar_width * len(versions)

for (i, test) in enumerate(tests):
    subfig = plt.subplot(gs[0, i])
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.grid(axis='y')

    workload = test['workload']
    operation = test['operation']
    for (version_idx, version) in enumerate(versions):
        data_dir = os.path.join(dir, workload, version['path'])
        path = os.path.join(data_dir, operation + '-latency-cdf')
        cdf = pd.read_table(path, delim_whitespace=True, names=['latency', 'cdf'])
        latencies = np.array(cdf['latency'])
        cdf = np.array(cdf['cdf'])
        x = []
        y = []
        for percentile in percentiles:
            x.append(str(percentile))
            y.append(latencies[np.searchsorted(cdf, percentile / 100)])
        x.append('max')
        y.append(latencies[-1])
        ax.plot(x, y, color=version['color'], marker=version['marker'], markerfacecolor='none', linewidth=1, markersize=4)
    plt.xticks(fontsize=8)
    plt.yscale('log')
    if i == 1:
        plt.yticks([1e5, 1e6, 1e7], fontsize=8)
        ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1, numticks=233))
    else:
        plt.yticks(fontsize=8)
    subfig.text(0.5, -0.27, 'Percentiles (%)', fontsize=6, ha='center', va='center', transform=subfig.transAxes)
    plt.xlabel(test['title'], labelpad = 8, fontsize=8)
    if i == 0:
        plt.ylabel('Latency (ns)', fontsize=8)
fig.legend(version_names, fontsize=8, ncol=len(versions), loc='center', bbox_to_anchor=(0.5, 0.99))
plt.tight_layout()
pdf_path = os.path.join(dir, 'latency.pdf')
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
