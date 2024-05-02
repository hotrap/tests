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

# Paper specific settings
SINGLE_COL_WIDTH = 8.5
DOUBLE_COL_WIDTH = 17.8
def cm_to_inch(value):
    return value/2.54

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(5)))

ids=[
    1,
    5,
    6,
    7,
    8,
    9,
    14,
    15,
    16,
    17,
    19,
    22,
    23,
    24,
    46,
    48,
]
workloads={
    1: 'cluster01-4247x',
    5: 'cluster05',
    6: 'cluster06-7x',
    7: 'cluster07-12x',
    8: 'cluster08-95x',
    9: 'cluster09-118x',
    11: 'cluster11-26x',
    14: 'cluster14-3x',
    15: 'cluster15',
    16: 'cluster16-68x',
    17: 'cluster17-80x',
    18: 'cluster18-197x',
    19: 'cluster19-3x',
    22: 'cluster22-9x',
    23: 'cluster23',
    24: 'cluster24-11x',
    29: 'cluster29',
    36: 'cluster36-18x',
    46: 'cluster46',
    48: 'cluster48-5x',
}

x = []
y = []
speedup = []
for id in ids:
    workload=workloads[id]
    x.append(float(open(os.path.join(stat_dir, 'cluster' + '{:02}'.format(id) + '.000-read-hot-5p-read')).read()))
    y.append(float(open(os.path.join(stat_dir, workload + '-read-with-more-than-5p-write-size')).read()))

    workload_dir = os.path.join(dir, workload)
    data_dir = os.path.join(workload_dir, 'promote-stably-hot')
    start_progress = common.warmup_finish_progress(data_dir)
    progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
    end_progress = progress.iloc[-1]['operations-executed']

    hotrap = common.ops_during_interval(data_dir, start_progress, end_progress)
    data_dir = os.path.join(workload_dir, "rocksdb-fat")
    rocksdb_fat = common.ops_during_interval(data_dir, start_progress, end_progress)
    speedup.append(hotrap / rocksdb_fat)

plt.scatter(x, y)
for i in range(0, len(x)):
    plt.text(x[i] + 0.02, y[i] - 0.02, '{:.2f}x'.format(speedup[i]), fontsize=8)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.xlabel('Skewness of reads', fontsize=8)
plt.ylabel('Age of reads', fontsize=8)
plt.tight_layout()
pdf_path = dir + '/twitter-scatter.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
