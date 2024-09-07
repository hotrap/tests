#!/usr/bin/env python3

import sys

if len(sys.argv) != 3:
	print('Usage: ' + sys.argv[0] + ' dir mean-step')
	exit()
dir = sys.argv[1]
mean_step = int(sys.argv[2])

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), 'common/'))

import matplotlib as mpl
import matplotlib.pyplot as plt

import throughput_breakdown

# Paper specific settings
DOUBLE_COL_WIDTH = 17.8
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
})
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH), cm_to_inch(3.5)), constrained_layout=True)

versions=[
    {
        'name': '(a) RocksDB(FD)',
        'path': 'rocksdb-fd',
    },
    {
        'name': '(b) RocksDB-tiered',
        'path': 'rocksdb-tiered',
    },
    {
        'name': '(c) HotRAP',
        'path': 'promote-stably-hot',
    },
]
throughput_breakdown.draw_throughput_breakdown(fig, dir, versions, mean_step, linewidth=0.5, num_marks=5, markersize=1, markersize_x=2)

fig.legend(['FD', 'SD', 'FD-Compaction', 'SD-Compaction', 'Get'], fontsize=8, ncol=5, loc='center', bbox_to_anchor=(0.5, 1.08))
pdf_path = 'throughput-breakdown.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
    plt.show()
