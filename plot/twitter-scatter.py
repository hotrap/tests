#!/usr/bin/env python3
import sys
if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' dir stat-dir')
    exit()
dir = sys.argv[1]
stat_dir = sys.argv[2]

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Paper specific settings
SINGLE_COL_WIDTH = 8.5
DOUBLE_COL_WIDTH = 17.8
def cm_to_inch(value):
    return value/2.54

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(6)))

workloads=[
    'cluster02-283x',
    'cluster05',
    'cluster08-95x',
    'cluster10',
    'cluster11-25x',
    'cluster16-67x',
    'cluster17-80x',
    'cluster18-185x',
    'cluster19-3x',
    'cluster22-9x',
    'cluster23',
    'cluster24-11x',
    'cluster29',
    'cluster30-10x',
    'cluster46',
    'cluster48-5x',
    'cluster52-3x',
]

read_heavy = set([2, 11, 16, 17, 18, 24, 29, 30, 52])
read_write = set([19, 22, 46, 48])
write_heavy = set([5, 8, 10, 23])

ids = []
xs = []
ys = []
speedup = []
for workload in workloads:
    id = int(workload.split('-')[0][7:])
    ids.append(id)
    x = float(open(os.path.join(stat_dir, workload + '-read-hot-5p-read')).read())
    xs.append(x)
    y = float(open(os.path.join(stat_dir, workload + '-read-with-more-than-5p-write-size')).read())
    ys.append(y)
    if id in read_heavy:
        marker = 'o'
    elif id in read_write:
        marker = '^'
    elif id in write_heavy:
        marker ='s'
    else:
        print('The type of cluster ' + str(id) + ' is unknown')
        exit(1)

    workload_dir = os.path.join(dir, workload)
    data_dir = os.path.join(workload_dir, 'promote-stably-hot')
    start_progress = common.warmup_finish_progress(data_dir)
    progress = pd.read_table(os.path.join(data_dir, 'progress'), sep='\s+')
    end_progress = progress.iloc[-1]['operations-executed']

    hotrap = common.ops_during_interval(data_dir, start_progress, end_progress)
    data_dir = os.path.join(workload_dir, "rocksdb-fat")
    rocksdb_fat = common.ops_during_interval(data_dir, start_progress, end_progress)
    speedup.append(hotrap / rocksdb_fat)
    plt.scatter(x, y, c='C0', marker=marker)

for i in range(0, len(xs)):
    plt.text(xs[i] - 0.08, ys[i] - 0.03, '{:02}'.format(ids[i]), fontsize=8, c='gray')
    plt.text(xs[i] + 0.02, ys[i] - 0.03, '{:.2f}x'.format(speedup[i]), fontsize=8)

red_square = mlines.Line2D([], [], color='red', marker='s', linestyle='None',
                          markersize=10, label='Red squares')
purple_triangle = mlines.Line2D([], [], color='purple', marker='^', linestyle='None',
                          markersize=10, label='Purple triangles')

markersize=5
handles=[
    mlines.Line2D([], [], color='C0', marker='o', linestyle='None', markersize=markersize, label='read-heavy'),
    mlines.Line2D([], [], color='C0', marker='^', linestyle='None', markersize=markersize, label='read-write'),
    mlines.Line2D([], [], color='C0', marker='s', linestyle='None', markersize=markersize, label='write-heavy'),
]
plt.legend(handles=handles, handlelength=0.5, fontsize=8, ncol=len(handles), loc='center', bbox_to_anchor=(0.45, 1.14))

plt.xlim(-0.03, 1.03)
plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize=8)
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize=8)
plt.xlabel('Skewness of reads', fontsize=8)
plt.ylabel('Age of reads', fontsize=8)
plt.tight_layout()
pdf_path = dir + '/twitter-scatter.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
