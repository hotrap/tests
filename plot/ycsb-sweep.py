#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

dir=sys.argv[1]

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

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

ticks = [0, 5e4, 10e4, 15e4]
subfigs = [
    {
        'title': '(a) hotspot-5%',
        'ticks': ticks
    },
    {
        'title': '(b) zipfian',
        'ticks': ticks
    },
    {
        'title': '(c) uniform',
        'ticks': ticks
    },
]

skewnesses = ['hotspot0.05', 'zipfian', 'uniform']
ycsb_configs = ['ycsbc', 'read_0.75_insert_0.25', 'read_0.5_insert_0.5', 'ycsba']
cluster_labels = ['RO', 'RW', 'WH', 'UH']
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
        'path': 'rocksdb-sd',
        'pattern': 'XXXXXXXXX',
        'color': plt.get_cmap('Set2')(2),
    },
    {
        'path': 'mutant',
        'pattern': '---',
        'color': plt.get_cmap('Set2')(4),
    },
    {
        'path': 'prismdb',
        'pattern': '---\\\\\\\\\\\\',
        'color': plt.get_cmap('Set2')(5),
    }
]
version_names = ['HotRAP', 'RocksDB-fat', 'RocksDB-secondary-cache', 'RocksDB(SD)', 'Mutant', 'PrismDB']
size='110GB'

gs = gridspec.GridSpec(1, len(skewnesses))
bar_width = 1 / (len(versions) + 1)
cluster_width = bar_width * len(versions)

workload_version_ops = {}
for i in range(len(skewnesses)):
    skewness = skewnesses[i]
    for ycsb in ycsb_configs:
        workload = ycsb + '_' + skewness + '_' + size
        workload_dir = os.path.join(dir, workload)
        data_dir = os.path.join(workload_dir, 'promote-stably-hot')
        start_progress = common.warmup_finish_progress(data_dir)
        progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
        end_progress = progress.iloc[-1]['operations-executed']
        workload_version_ops[workload] = {}
        for (version_idx, version) in enumerate(versions):
            if version_idx < 4:
                data_dir = os.path.join(workload_dir, version['path'])
                timestamp_start = common.progress_to_timestamp(data_dir, start_progress)
                timestamp_end = common.progress_to_timestamp(data_dir, end_progress)
                progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
                progress = progress[(timestamp_start <= progress['Timestamp(ns)']) & (progress['Timestamp(ns)'] < timestamp_end)]
                operations_executed = progress.iloc[-1]['operations-executed'] - progress.iloc[0]['operations-executed']
                seconds = (progress.iloc[-1]['Timestamp(ns)'] - progress.iloc[0]['Timestamp(ns)']) / 1e9
                workload_version_ops[workload][version['path']] = operations_executed / seconds

other_sys_in = open('other-sys.txt')
while True:
    line = other_sys_in.readline()
    line = line.strip()
    if len(line) == 0:
        break
    if line == 'uh':
        t = 'ycsba'
    elif line == 'wr':
        t = 'read_0.75_insert_0.25'
    elif line == 'wh':
        t = 'read_0.5_insert_0.5'
    elif line == 'rh':
        t = 'ycsbc'
    else:
        print('Unknown type ' + line)
        assert False
    for _ in range(0, 2):
        line = other_sys_in.readline().strip().split(' ')
        assert line[0][-1] == ':'
        version = line[0][:-1]
        i = 1
        while i < len(line):
            skewness = line[i]
            i += 1
            ops = float(line[i])
            i += 1
            workload = t + '_' + skewness + '_' + size
            workload_version_ops[workload][version] = ops

def get_ratios(skewnesses):
    ratios = []
    for skewness in skewnesses:
        for ycsb in ['ycsbc', 'read_0.75_insert_0.25', 'read_0.5_insert_0.5']:
            workload = ycsb + '_' + skewness + '_' + size
            version_ops = workload_version_ops[workload]
            ratios.append(version_ops['promote-stably-hot'] / version_ops['rocksdb-fat'])
            ratios.append(version_ops['promote-stably-hot'] / version_ops['secondary-cache'])
    return ratios
ratios = get_ratios(['hotspot0.05', 'zipfian'])
print("%.1f%%" %((min(ratios) - 1) * 100))
print("%.0f%%" %((max(ratios) - 1) * 100))

ratios = get_ratios(['uniform'])
print("%.1f%%" %((min(ratios) - 1) * 100))
print("%.0f%%" %((max(ratios) - 1) * 100))

for i in range(len(skewnesses)):
    subfig = plt.subplot(gs[0, i])
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.grid(axis='y')
    skewness = skewnesses[i]
    for (pivot, ycsb) in enumerate(ycsb_configs):
        workload = ycsb + '_' + skewness + '_' + size
        for (version_idx, version) in enumerate(versions):
            x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
            value = workload_version_ops[workload][version['path']]
            ax.bar(x, value, width=bar_width, hatch=version['pattern'], color=version['color'], edgecolor='black', linewidth=0.5)
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-3, 4))
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set_fontsize(8)
    plt.xticks(range(0, len(cluster_labels)), cluster_labels, fontsize=8)
    plt.yticks(subfigs[i]['ticks'], fontsize=8)
    plt.ylim((0, max(subfigs[i]['ticks']) + 1e4))
    plt.xlabel(subfigs[i]['title'], labelpad=1, fontsize=8)
    if i == 0:
        plt.ylabel('Operations per second', fontsize=8)
fig.legend(version_names, fontsize=8, ncol=len(version_names), loc='center', bbox_to_anchor=(0.5, 0.99))
plt.tight_layout()
pdf_path = dir + '/ycsb-sweep.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
