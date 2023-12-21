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

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(4)))

versions = [
	{
		'name': '(a) HotRAP',
		'path': 'promote-stably-hot',
    },
	{
        'name': '(b) promote-accessed',
		'path': 'flush-accessed',
    }
]
throughput_breakdown.draw_throughput_breakdown(dir, versions, mean_step, linewidth=0.5, num_marks=5, markersize=1, markersize_x=2)

fig.legend(['SD', 'CD', 'SD-Compaction', 'CD-Compaction', 'Get'], fontsize=8, ncol=3, loc='center', bbox_to_anchor=(0.5, 1.05))
plt.tight_layout()
pdf_path = 'promote-accessed-throughput.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
