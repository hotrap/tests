#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

dir=sys.argv[1]

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter

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

figure = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(3.5)), constrained_layout=True)

ticks = [0, 5e4, 10e4, 15e4]
figs = [
    {
        'title': '(a) hotspot-5%',
        'skewness': 'hotspot0.05',
        'ticks': ticks,
        'ylim': 16e4,
    },
    {
        'title': '(b) zipfian',
        'skewness': 'zipfian',
        'ticks': ticks,
        'ylim': 16e4,
    },
    {
        'title': '(b) uniform',
        'skewness': 'uniform',
        'ticks': ticks,
        'ylim': 16e4,
    },
]

ratio_paths = ['ycsbc', 'read_0.75_insert_0.25', 'read_0.5_insert_0.5', 'ycsba']
ratio_names = ['RO', 'RW', 'WH', 'UH']

versions = [
    {
        'size': '1.1TB',
        'path': 'rocksdb-fd',
        'pattern': 'XXXXXXXXX',
        'color': plt.get_cmap('Set2')(2),
    },
    {
        'size': '1.1TB',
        'path': 'rocksdb-tiered',
        'pattern': '\\\\\\',
        'color': plt.get_cmap('Set2')(1),
    },
    {
        'size': '1.1TB_2.2TB',
        'path': 'hotrap',
        'pattern': '///',
        'color': plt.get_cmap('Set2')(0),
    }
]
labels = ['RocksDB-FD', 'RocksDB-tiering', common.sysname]

gs = gridspec.GridSpec(1, len(figs), figure=figure)
num_clusters = len(versions)
bar_width = 1 / (num_clusters + 1)
cluster_width = bar_width * num_clusters

for (i, fig) in enumerate(figs):
    plt.subplot(gs[0, i])
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.grid(axis='y')
    skewness = fig['skewness']
    for (pivot, ratio_path) in enumerate(ratio_paths):
        for (version_idx, version) in enumerate(versions):
            x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
            workload = ratio_path + '_' + skewness + '_' + version['size']
            data_dir = os.path.join(dir, workload, version['path'])
            value = common.last_10p_ops(common.VersionData(data_dir))
            ax.bar(x, value, width=bar_width, hatch=version['pattern'], color=version['color'], edgecolor='black', linewidth=0.5)
    ax.ticklabel_format(style='sci', scilimits=(4, 4), useMathText=True)
    ax.yaxis.get_offset_text().set_fontsize(9)
    plt.xticks(range(0, len(ratio_names)), ratio_names, fontsize=8)
    plt.yticks(fig['ticks'], fontsize=9)
    ax.tick_params(axis='y', which='major', pad=0.1)
    plt.ylim((0, fig['ylim']))
    plt.xlabel(fig['title'], labelpad=1, fontsize=9)
    if i == 0:
        plt.ylabel('Operations per second', fontsize=9, y=0.4)
handles = []
for version in versions:
    handles.append(mpl.patches.Patch(facecolor=version['color'], hatch=version['pattern'], edgecolor='black', linewidth=0.5))
figure.legend(handles=handles, labels=labels, fontsize=9, ncol=len(handles), loc='center', bbox_to_anchor=(0.5, 1.07), handletextpad=0.5, columnspacing=1)
pdf_path = dir + '/ops-1.1TB.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
