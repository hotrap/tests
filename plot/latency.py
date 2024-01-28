#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()
dir = sys.argv[1]

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter

# Paper specific settings
SINGLE_COL_WIDTH = 8.5
DOUBLE_COL_WIDTH = 17.8
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
    })
plt.rcParams['axes.unicode_minus'] = False

figure = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(3)), constrained_layout=True)

xticks = ['RO', 'RW', 'WH']
workloads = [
    {
        'path': 'ycsbc_hotspot0.05_110GB',
    },
    {
        'path': 'read_0.75_insert_0.25_hotspot0.05_110GB',
    },
    {
        'path': 'read_0.5_insert_0.5_hotspot0.05_110GB',
    },
]
versions=[
    {
        'path': 'promote-stably-hot',
        'pattern': '///',
        'color': plt.get_cmap('Set2')(0),
        'workloads': workloads,
    },
    {
        'path': 'rocksdb-fat',
        'pattern': '\\\\\\',
        'color': plt.get_cmap('Set2')(1),
        'workloads': workloads,
    },
    {
        'path': 'secondary-cache',
        'pattern': 'XXX',
        'color': plt.get_cmap('Set2')(3),
        'workloads': workloads,
    },
    {
        'path': 'rocksdb-sd',
        'pattern': 'XXXXXXXXX',
        'color': plt.get_cmap('Set2')(2),
        'workloads': workloads,
    },
]
version_names = ['HotRAP', 'RocksDB-fat', 'RocksDB-secondary-cache', 'RocksDB(SD)', 'Mutant', 'PrismDB']

gs = gridspec.GridSpec(1, 3, figure=figure)
bar_width = 1 / (len(versions) + 1)
cluster_width = bar_width * len(versions)

figs = [
    {
        'title': '(a) 50%',
        'subfig': plt.subplot(gs[0, 0]),
        'ax': plt.gca(),
        'percentile': '50%',
    },
    {
        'title': '(b) 99%',
        'subfig': plt.subplot(gs[0, 1]),
        'ax': plt.gca(),
        'percentile': '99%',
    },
    {
        'title': '(c) 99.9% (log scale)',
        'subfig': plt.subplot(gs[0, 2]),
        'ax': plt.gca(),
        'percentile': '99.9%',
        'yscale': 'log',
    },
]

warmup_finish_progress = {}
for workload in workloads:
    workload_dir = os.path.join(dir, workload['path'])
    data_dir = os.path.join(workload_dir, 'promote-stably-hot')
    warmup_finish_progress[workload['path']] = common.warmup_finish_progress(data_dir)

for (version_idx, version) in enumerate(versions):
    for (pivot, workload) in enumerate(version['workloads']):
        data_dir = os.path.join(dir, workload['path'], version['path'])
        if version_idx < 4:
            warmup_finish_ts = common.progress_to_timestamp(data_dir, warmup_finish_progress[workload['path']])
            for fig in figs:
                x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
                path = os.path.join(data_dir, 'read-latency')
                latency = pd.read_table(path, delim_whitespace=True)
                latency = latency[latency['Timestamp(ns)'] >= warmup_finish_ts].iloc[-1]
                value = latency[fig['percentile']]
                fig['ax'].bar(x, value, width=bar_width, hatch=version['pattern'], color=version['color'], edgecolor='black', linewidth=0.5)
                # print(workload['name'], version['path'], fig['percentile'], value)

for (i, fig) in enumerate(figs):
    subfig = fig['subfig']
    ax = fig['ax']
    ax.set_axisbelow(True)
    ax.grid(axis='y')

    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-3, 4))
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set_fontsize(8)
    ax.tick_params(axis='y', which='major', labelsize=8)

    ax.set_xticks(list(range(0, len(xticks))), xticks, fontsize=8)
    if i == 2:
        ax.set_xlabel(fig['title'], labelpad=2, fontsize=8, loc='right')
    else:
        ax.set_xlabel(fig['title'], labelpad=2, fontsize=8)
    if 'yscale' in fig:
        ax.set_yscale(fig['yscale'])
    if i == 0:
        ax.set_ylabel('Latency (ns)', fontsize=8)
handles = []
for version in versions:
    handles.append(mpl.patches.Patch(facecolor=version['color'], hatch=version['pattern'], edgecolor='black', linewidth=0.5))
figure.legend(handles=handles, labels=version_names, fontsize=8, ncol=2, loc='center', bbox_to_anchor=(0.5, 1.13))
# gs.tight_layout(figure=figure)
pdf_path = os.path.join(dir, 'latency.pdf')
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
