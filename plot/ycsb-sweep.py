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
rw_ratios = ['RO', 'RW', 'WH', 'UH']
ratios_ycsb = {
    'RO': 'ycsbc',
    'RW': 'read_0.75_insert_0.25',
    'WH': 'read_0.5_insert_0.5',
    'UH': 'ycsba'
}
ratios_prismdb_mutant = {
    'RO': 'ycsbc',
    'RW': 'wr',
    'WH': 'wh',
    'UH': 'ycsba'
}
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
version_names = ['HotRAP', 'RocksDB-fat', 'RocksDB-secondary-cache', 'RocksDB(FD)', 'Mutant', 'PrismDB']
size='110GB'

gs = gridspec.GridSpec(1, len(skewnesses))
bar_width = 1 / (len(versions) + 1)
cluster_width = bar_width * len(versions)

skewness_ratio_version_ops = {}
for i in range(len(skewnesses)):
    skewness = skewnesses[i]
    skewness_ratio_version_ops[skewness] = {}
    for ratio in rw_ratios:
        workload = ratios_ycsb[ratio] + '_' + skewness + '_' + size
        data_dir = os.path.join(dir, workload, 'promote-stably-hot')
        start_progress = common.warmup_finish_progress(data_dir)
        progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
        end_progress = progress.iloc[-1]['operations-executed']
        skewness_ratio_version_ops[skewness][ratio] = {}
        for (version_idx, version) in enumerate(versions):
            if version_idx < 4:
                workload = ratios_ycsb[ratio] + '_' + skewness + '_' + size
                data_dir = os.path.join(dir, workload, version['path'])
                timestamp_start = common.progress_to_timestamp(data_dir, start_progress)
                timestamp_end = common.progress_to_timestamp(data_dir, end_progress)
                progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
                progress = progress[(timestamp_start <= progress['Timestamp(ns)']) & (progress['Timestamp(ns)'] < timestamp_end)]
                operations_executed = progress.iloc[-1]['operations-executed'] - progress.iloc[0]['operations-executed']
                seconds = (progress.iloc[-1]['Timestamp(ns)'] - progress.iloc[0]['Timestamp(ns)']) / 1e9
                skewness_ratio_version_ops[skewness][ratio][version['path']] = operations_executed / seconds
            else:
                workload = 'workload_110GB_' + ratios_prismdb_mutant[ratio] + '_' + skewness
                data_dir = os.path.join(dir, workload, version['path'])
                progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
                last = progress.iloc[-1]
                progress = progress[progress['operations-executed'] != last['operations-executed']]
                last = progress.iloc[-1]
                first = progress.iloc[len(progress) - len(progress) // 10]
                seconds = (last['Timestamp(ns)'] - first['Timestamp(ns)']) / 1e9
                ops = (last['operations-executed'] - first['operations-executed']) / seconds
                skewness_ratio_version_ops[skewness][ratio][version['path']] = ops

def get_ratios(skewnesses):
    ratios = []
    for skewness in skewnesses:
        for ratio in ['RO', 'RW', 'WH']:
            version_ops = skewness_ratio_version_ops[skewness][ratio]
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
    for (pivot, ratio) in enumerate(rw_ratios):
        for (version_idx, version) in enumerate(versions):
            x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
            value = skewness_ratio_version_ops[skewness][ratio][version['path']]
            ax.bar(x, value, width=bar_width, hatch=version['pattern'], color=version['color'], edgecolor='black', linewidth=0.5)
    ax.ticklabel_format(style='sci', scilimits=(4, 4), useMathText=True)
    ax.yaxis.get_offset_text().set_fontsize(8)
    plt.xticks(range(0, len(rw_ratios)), rw_ratios, fontsize=8)
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
