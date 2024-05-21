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
import matplotlib as mpl
import matplotlib.pyplot as plt

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

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(4.5)))

workloads=[
    'cluster17-80x',
    'cluster18-185x',
    'cluster16-67x',
    'cluster19-3x',
    'cluster10',
    'cluster29',
]
versions=[
    {
        'path': 'promote-stably-hot',
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
        'path': 'rocksdb-fd',
        'pattern': 'XXXXXXXXX',
        'color': plt.get_cmap('Set2')(2),
    },
]
version_names = ['HotRAP', 'RocksDB-fat', 'RocksDB-secondary-cache', 'RocksDB(FD)']

workload_version_ops = {}
for workload in workloads:
    workload_dir = os.path.join(dir, workload)
    data_dir = os.path.join(workload_dir, 'promote-stably-hot')
    start_progress = common.warmup_finish_progress(data_dir)
    progress = pd.read_table(os.path.join(data_dir, 'progress'), sep='\s+')
    end_progress = progress.iloc[-1]['operations-executed']

    version_ops = {}
    for version in versions:
        data_dir = os.path.join(workload_dir, version['path'])
        version_ops[version['path']] = common.ops_during_interval(data_dir, start_progress, end_progress)
    workload_version_ops[workload] = version_ops

bar_width = 1 / (len(versions) + 1)
cluster_width = bar_width * len(versions)

ax = plt.gca()
ax.set_axisbelow(True)
ax.grid(axis='y')
ids = []
for (pivot, workload) in enumerate(workloads):
    ids.append(workload.split('-')[0][7:])
    for (version_idx, version) in enumerate(versions):
        x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
        value = workload_version_ops[workload][version['path']]
        ax.bar(x, value, width=bar_width, hatch=version['pattern'], color=version['color'], edgecolor='black', linewidth=0.5)
ax.ticklabel_format(style='sci', scilimits=(4, 4), useMathText=True)
ax.yaxis.get_offset_text().set_fontsize(8)
plt.xticks(range(0, len(workloads)), ids, fontsize=8)
plt.yticks([0, 5e4, 10e4, 15e4], fontsize=8)
plt.xlabel('Cluster ID', labelpad=1, fontsize=8)
plt.ylabel('Operations per second', fontsize=8)
fig.legend(version_names, fontsize=8, ncol=2, loc='center', bbox_to_anchor=(0.5, 1.04))
plt.tight_layout()
pdf_path = dir + '/twitter-ops.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
