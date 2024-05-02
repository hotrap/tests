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
        'path': 'rocksdb-fd',
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
                skewness_ratio_version_ops[skewness][ratio][version['path']] = common.ops_during_interval(data_dir, start_progress, end_progress)
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

def speedup_ratio_skewness(ratio, skewness):
    version_ops = skewness_ratio_version_ops[skewness][ratio]
    hotrap_ops = version_ops['promote-stably-hot']
    other_sys_max_ops = 0
    for (version, ops) in version_ops.items():
        if version == 'promote-stably-hot' or version == 'rocksdb-fd':
            continue
        other_sys_max_ops = max(other_sys_max_ops, ops)
    return hotrap_ops / other_sys_max_ops
def speedup(ratio):
    speedup_hotspot = speedup_ratio_skewness(ratio, 'hotspot0.05')
    speedup_zipfian = speedup_ratio_skewness(ratio, 'zipfian')
    assert speedup_hotspot >= speedup_zipfian
    return speedup_hotspot

tex = io.StringIO()
speedup_ro = speedup('RO')
print('% Speedup over second best under read-only workloads', file=tex)
print('\defmacro{SpeedupRO}{%.1f}' %speedup_ro, file=tex)
speedup_rw = speedup('RW')
print("% Speedup over second best under read-write workloads", file=tex)
print('\defmacro{SpeedupRW}{%.1f}' %speedup_rw, file=tex)
max_speedup_ro_rw = max(speedup_ro, speedup_rw)
print("% Max speedup over second best under RO & RW", file=tex)
print('\defmacro{MaxSpeedupRORW}{%.1f}' %max_speedup_ro_rw, file=tex)

min_ratio = 1
ratio_version_ops = skewness_ratio_version_ops['uniform']
for (ratio, version_ops) in ratio_version_ops.items():
    min_ratio = min(min_ratio, version_ops['promote-stably-hot'] / version_ops['rocksdb-fat'])
overhead = 1 - min_ratio
print('% Max overhead under uniform workloads compared to RocksDB-fat', file=tex)
print('\defmacro{OverheadUniformRocksDBFat}{%.1f\\%%}' %(overhead * 100), file=tex)

tex = tex.getvalue()
print(tex)
open(os.path.join(dir, 'ycsb-sweep.tex'), mode='w').write(tex)

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
