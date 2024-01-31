#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()
dir = sys.argv[1]

import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Paper specific settings
DOUBLE_COL_WIDTH = 17.8
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
    })
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH) * 0.33, cm_to_inch(4.7)))

versions = [
    {
        'path': 'exp',
        'marker': 'o',
    },
    {
        'path': 'lru',
        'marker': '^',
    },
    {
        'path': 'clock',
        'marker': 's',
    }
]
version_names = ['Exponential smoothing', 'LRU', 'CLOCK']

ax = plt.gca()
for version in versions:
    data = pd.read_table(os.path.join(dir, version['path']), names=['progress', 'hit-rate'], delim_whitespace=True)
    plt.plot(data['progress'], data['hit-rate'], linewidth=0.5, marker=version['marker'], markersize=3, markevery=int(len(data['progress']) / 5))
plt.xlabel('Completed operation count', fontsize=8, loc='left')
plt.ylabel('Hit rate', fontsize=8)
plt.xticks(fontsize=8)
ax.ticklabel_format(useMathText=True)
ax.xaxis.get_offset_text().set_fontsize(8)
plt.yticks(np.linspace(0, 1, 6), fontsize=8)
plt.legend(version_names, frameon=False, fontsize=8)

pdf_path = dir + '/progress-hit-rate-scoring.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
