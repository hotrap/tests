#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()
dir = sys.argv[1]

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH) * 0.33, cm_to_inch(4.5)))

versions = [
    {
        'path': 'EXP',
        'marker': 'o',
    },
    {
        'path': 'LRU',
        'marker': '^',
    },
    {
        'path': 'CLOCK',
        'marker': 's',
    }
]
version_names = ['Exponential smoothing', 'LRU', 'CLOCK']

ax = plt.gca()
for version in versions:
    data_dir = os.path.join(dir, version['path'])
    version_data = common.VersionData(data_dir)

    hit_rates = common.read_hit_rates(data_dir)
    (x, hit_rates) = common.estimate(version_data, hit_rates, 'hit-rate')

    plt.plot(x, hit_rates, linewidth=0.5, marker=version['marker'], markersize=3, markevery=int(len(x) / 5))

plt.xlabel('Completed operation count', fontsize=8, loc='left')
ax.xaxis.set_label_coords(0.1, -0.19)
plt.xticks(fontsize=8)
ax.ticklabel_format(useMathText=True)
ax.xaxis.get_offset_text().set_fontsize(8)
plt.ylabel('Hit rate', fontsize=8)
plt.yticks(np.linspace(0, 1, 6), fontsize=8)
plt.legend(version_names, frameon=False, fontsize=8)

pdf_path = dir + '/progress-hit-rate-scoring.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
