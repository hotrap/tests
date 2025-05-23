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
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

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
ylim = 17e4
subfigs = [
    {
        'title': '(b) hotspot-5%',
    },
    {
        'title': '(c) zipfian',
    },
    {
        'title': '(d) uniform',
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
        'path': 'rocksdb-tiered',
        'pattern': '\\\\\\',
        'color': plt.get_cmap('Set2')(1),
    },
    {
        'path': 'cachelib',
        'pattern': '---',
        'color': plt.get_cmap('tab20c')(1),
    },
    {
        'path': 'SAS-Cache',
        'pattern': 'XXX',
        'color': plt.get_cmap('Set2')(3),
    },
    {
        'path': 'prismdb',
        'pattern': '---\\\\\\\\\\\\',
        'color': plt.get_cmap('Set2')(5),
    },
    {
        'path': 'hotrap',
        'pattern': '///',
        'color': plt.get_cmap('Set2')(0),
    },
]
version_names = ['RocksDB-FD', 'RocksDB-tiering', 'RocksDB-CL', 'SAS-Cache', 'PrismDB', common.sysname]
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
    min_ratio = min(min_ratio, version_ops['hotrap'] / version_ops['rocksdb-tiered'])
overhead = 1 - min_ratio
print('{\n\t\"OverheadUniformRocksdbTiered1KiB\": %f\n}' %overhead, file=json_output)
json_output = json_output.getvalue()
print(json_output)
open(os.path.join(dir, 'ycsb-sweep.json'), mode='w').write(json_output)

def speedup(ratio, version):
    ret = None
    for skewness in skewnesses:
        version_ops = skewness_ratio_version_ops[skewness][ratio]
        cur = version_ops['hotrap'] / version_ops[version]
        if ret is None:
            ret = cur
        else:
            ret = max(ret, cur)
    return ret

tex = io.StringIO()
print('% Speedup over the second best tiering baseline under read-only workloads', file=tex)
print('\defmacro{SpeedupROTiering}{%.1f}' %min(speedup('RO', 'rocksdb-tiered'), speedup('RO', 'prismdb')), file=tex)

print('% Speedup over the second best caching baseline under write-heavy workloads', file=tex)
print('\defmacro{SpeedupWHCaching}{%.1f}' %min(speedup('WH', 'cachelib'), speedup('WH', 'SAS-Cache')), file=tex)

speedup_rw = None
for version in versions:
    if version['path'] == 'hotrap' or version['path'] == 'rocksdb-fd':
        continue
    cur = speedup('RW', version['path'])
    if speedup_rw is None:
        speedup_rw = cur
    else:
        speedup_rw = min(speedup_rw, cur)
print("% Speedup over the second best baseline under read-write workloads", file=tex)
print('\defmacro{SpeedupRW}{%.1f}' %speedup_rw, file=tex)

tex = tex.getvalue()
print(tex)
open(os.path.join(dir, 'ycsb-sweep.tex'), mode='w').write(tex)

len_load_phase = 1
len_other = 4
grid = (1, len_load_phase + len_other * 3)
bar_width = 1 / (len(versions) + 1)
cluster_width = bar_width * len(versions)

plt.subplot2grid(grid, (0, 0), colspan=len_load_phase)
ax = plt.gca()
for (version_idx, version) in enumerate(versions):
    x = -cluster_width / 2 + bar_width / 2 + version_idx * bar_width
    data_dir = os.path.join(dir, 'ycsbc_hotspot0.05_110GB_220GB', version['path'])
    info = common.VersionData(data_dir).info()
    value = info['num-load-op'] / info['load-time(secs)']
    ax.bar(x, value, width=bar_width, hatch=version['pattern'], color=version['color'], edgecolor='black', linewidth=0.5)
ax.set_axisbelow(True)
ax.grid(axis='y')
ax.ticklabel_format(style='sci', scilimits=(4, 4), useMathText=True)
ax.yaxis.get_offset_text().set_fontsize(9)
plt.xlim((-cluster_width / 2 - bar_width / 2, cluster_width / 2 + bar_width / 2))
plt.xticks([], [])
plt.yticks(ticks, fontsize=9)
plt.ylim((0, ylim))
plt.xlabel('(a) Load-\nphase', labelpad=5, fontsize=9, loc='right')
plt.ylabel('Operations per second', fontsize=9)

for i in range(len(skewnesses)):
    plt.subplot2grid(grid, (0, len_load_phase + i * len_other), colspan=len_other)
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
    ax.yaxis.get_offset_text().set_fontsize(9)
    plt.xticks(range(0, len(rw_ratios)), rw_ratios, fontsize=9)
    plt.yticks(ticks, fontsize=9)
    plt.ylim((0, ylim))
    plt.xlabel(subfigs[i]['title'], labelpad=1, fontsize=9)
figure.legend(version_names, fontsize=9, ncol=len(version_names), loc='center', bbox_to_anchor=(0.51, 1.07), handletextpad=0.5, columnspacing=1.2)
pdf_path = os.path.join(dir, 'fig5-ycsb-sweep.pdf')
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
