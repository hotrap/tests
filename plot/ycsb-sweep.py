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

# Paper specific settings
SINGLE_COL_WIDTH = 8.5
DOUBLE_COL_WIDTH = 17.8
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
})
plt.rcParams['axes.unicode_minus'] = False

figure = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH), cm_to_inch(3.5)), constrained_layout=True)

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
versions=[
    {
        'path': 'rocksdb-fd',
        'pattern': 'XXXXXXXXX',
        'color': plt.get_cmap('Set2')(2),
    },
    {
        'path': 'rocksdb-fat',
        'pattern': '\\\\\\',
        'color': plt.get_cmap('Set2')(1),
    },
    {
        'path': 'mutant',
        'pattern': '---',
        'color': plt.get_cmap('tab20c')(1),
    },
    {
        'path': 'prismdb',
        'pattern': '---\\\\\\\\\\\\',
        'color': plt.get_cmap('Set2')(5),
    },
    {
        'path': 'SAS-Cache',
        'pattern': 'XXX',
        'color': plt.get_cmap('Set2')(3),
    },
    {
        'path': 'promote-stably-hot',
        'pattern': '///',
        'color': plt.get_cmap('Set2')(0),
    },
]
version_names = ['RocksDB(FD)', 'RocksDB-fat', 'Mutant', 'PrismDB', 'SAS-Cache', 'HotRAP']
size='110GB_220GB'

skewness_ratio_version_ops = {}
for i in range(len(skewnesses)):
    skewness = skewnesses[i]
    skewness_ratio_version_ops[skewness] = {}
    for ratio in rw_ratios:
        workload = ratios_ycsb[ratio] + '_' + skewness + '_' + size
        skewness_ratio_version_ops[skewness][ratio] = {}
        for (version_idx, version) in enumerate(versions):
            # We use the OPS of the last 10%
            workload = ratios_ycsb[ratio] + '_' + skewness + '_' + size
            data_dir = os.path.join(dir, workload, version['path'])
            version_data = common.VersionData(data_dir)
            skewness_ratio_version_ops[skewness][ratio][version['path']] = common.last_10p_ops(version_data)

json_output = io.StringIO()
min_ratio = 1
for (ratio, version_ops) in skewness_ratio_version_ops['uniform'].items():
    min_ratio = min(min_ratio, version_ops['promote-stably-hot'] / version_ops['rocksdb-fat'])
overhead = 1 - min_ratio
print('{\n\t\"OverheadUniformRocksDBFat1KiB\": %f\n}' %overhead, file=json_output)
json_output = json_output.getvalue()
print(json_output)
open(os.path.join(dir, 'ycsb-sweep.json'), mode='w').write(json_output)

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
tex = tex.getvalue()
print(tex)
open(os.path.join(dir, 'ycsb-sweep.tex'), mode='w').write(tex)

gs = gridspec.GridSpec(1, len(skewnesses), figure=figure)
bar_width = 1 / (len(versions) + 1)
cluster_width = bar_width * len(versions)

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
figure.legend(version_names, fontsize=8, ncol=len(version_names), loc='center', bbox_to_anchor=(0.5, 1.06))
pdf_path = dir + '/ycsb-sweep.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
