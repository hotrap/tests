#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

dir=sys.argv[1]

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import io
import pandas as pd
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

figure = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(4)))

versions = {
    'promote-stably-hot': {
        'pattern': '///',
        'color': plt.get_cmap('Set2')(0),
    },
    'rocksdb-fat': {
        'pattern': '\\\\\\',
        'color': plt.get_cmap('Set2')(1),
    },
    'rocksdb-fd': {
        'pattern': 'XXXXXXXXX',
        'color': plt.get_cmap('Set2')(2),
    },
}
version_names = ['HotRAP', 'RocksDB-fat', 'RocksDB(FD)']
figs = [
    {
        'title': '(a) hotspot-5%',
        'skewness': 'hotspot0.05',
        'ticks': [0, 4e4, 8e4, 12e4],
        'versions': ['promote-stably-hot', 'rocksdb-fd']
    },
    {
        'title': '(b) uniform',
        'skewness': 'uniform',
        'ticks': [0, 1e4, 2e4, 3e4],
        'versions': ['promote-stably-hot', 'rocksdb-fat']
    },
]

rw_ratios = ['RO', 'RW', 'WH', 'UH']
ratios_ycsb = {
    'RO': 'ycsbc',
    'RW': 'read_0.75_insert_0.25',
    'WH': 'read_0.5_insert_0.5',
    'UH': 'ycsba'
}
size='110GB_220GB_200B'

gs = gridspec.GridSpec(1, len(figs))
num_clusters = 2
bar_width = 1 / (num_clusters + 1)
cluster_width = bar_width * num_clusters

skewness_ratio_version_ops = {}
for fig in figs:
    skewness = fig['skewness']
    skewness_ratio_version_ops[skewness] = {}
    for ratio in rw_ratios:
        workload = ratios_ycsb[ratio] + '_' + skewness + '_' + size
        data_dir = os.path.join(dir, workload, 'promote-stably-hot')
        start_progress = common.warmup_finish_progress(data_dir)
        progress = pd.read_table(os.path.join(data_dir, 'progress'), sep='\s+')
        end_progress = progress.iloc[-1]['operations-executed']
        skewness_ratio_version_ops[skewness][ratio] = {}
        for version in fig['versions']:
            workload = ratios_ycsb[ratio] + '_' + skewness + '_' + size
            data_dir = os.path.join(dir, workload, version)
            timestamp_start = common.progress_to_timestamp(data_dir, start_progress)
            timestamp_end = common.progress_to_timestamp(data_dir, end_progress)
            progress = pd.read_table(os.path.join(data_dir, 'progress'), sep='\s+')
            progress = progress[(timestamp_start <= progress['Timestamp(ns)']) & (progress['Timestamp(ns)'] < timestamp_end)]
            operations_executed = progress.iloc[-1]['operations-executed'] - progress.iloc[0]['operations-executed']
            seconds = (progress.iloc[-1]['Timestamp(ns)'] - progress.iloc[0]['Timestamp(ns)']) / 1e9
            skewness_ratio_version_ops[skewness][ratio][version] = operations_executed / seconds

json_output = io.StringIO()
min_ratio = 1
ratio_version_ops = skewness_ratio_version_ops['uniform']
for (ratio, version_ops) in ratio_version_ops.items():
    min_ratio = min(min_ratio, version_ops['promote-stably-hot'] / version_ops['rocksdb-fat'])
overhead = 1 - min_ratio
print('{\n\t\"OverheadUniformRocksDBFat200B\": %f\n}' %overhead, file=json_output)
json_output = json_output.getvalue()
print(json_output)
open(os.path.join(dir, 'ops-200B.json'), mode='w').write(json_output)

for (i, fig) in enumerate(figs):
    plt.subplot(gs[0, i])
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.grid(axis='y')
    skewness = fig['skewness']
    for (pivot, ratio) in enumerate(rw_ratios):
        for (version_idx, version) in enumerate(fig['versions']):
            x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
            value = skewness_ratio_version_ops[skewness][ratio][version]
            ax.bar(x, value, width=bar_width, hatch=versions[version]['pattern'], color=versions[version]['color'], edgecolor='black', linewidth=0.5)
    ax.ticklabel_format(style='sci', scilimits=(4, 4), useMathText=True)
    ax.yaxis.get_offset_text().set_fontsize(8)
    plt.xticks(range(0, len(rw_ratios)), rw_ratios, fontsize=8)
    plt.yticks(fig['ticks'], fontsize=8)
    plt.ylim((0, max(fig['ticks']) + 1e4))
    plt.xlabel(fig['title'], labelpad=1, fontsize=8)
    if i == 0:
        plt.ylabel('Operations per second', fontsize=8)
handles = []
for (version, info) in versions.items():
    handles.append(mpl.patches.Patch(facecolor=info['color'], hatch=info['pattern'], edgecolor='black', linewidth=0.5))
figure.legend(handles=handles, labels=version_names, fontsize=8, ncol=len(handles), loc='center', bbox_to_anchor=(0.5, 0.99))
plt.tight_layout()
pdf_path = dir + '/ops-200B.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
