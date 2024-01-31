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
import matplotlib.gridspec as gridspec

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

figure = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH) * 0.66, cm_to_inch(4.7)), constrained_layout=True)

figs = [
    {
        'versions': [
            {
                'path': 'uniform',
                'marker': 'o',
            },
            {
                'path': 'hotspot0.01',
                'marker': '^',
            },
            {
                'path': 'hotspot0.02',
                'marker': 's',
            },
            {
                'path': 'hotspot0.05',
                'marker': 'D',
            },
        ],
        'names': ['uniform', 'hotspot-1%', 'hotspot-2%', 'hotspot-5%'],
        'yticks': [0, 1, 2, 3, 4, 5],
        'loc': [0.5, 0.4],
    },
    # {
    #     'versions': [
    #         {
    #             'path': 'zipfian',
    #             'marker': None,
    #         }
    #     ],
    #     'names': ['zipfian'],
    #     'yticks': [0, 1, 2, 3],
    # },
    {
        'versions': [
            {
                'path': 'hotspotshifting0.5-0.5',
                'marker': 'o',
            },
            {
                'path': 'hotspotshifting0.5-0.2',
                'marker': 's',
            },
        ],
        'names': ['from 5% to another 5%', 'from 5% to another 2%'],
        'yticks': [0, 1, 2, 3, 4, 5, 6, 7],
    }
]

gs = gridspec.GridSpec(1, len(figs), figure=figure)

for (i, fig) in enumerate(figs):
    plt.subplot(gs[0, i])
    ax = plt.gca()
    for version in fig['versions']:
        data = pd.read_table(os.path.join(dir, version['path']), names=['progress', 'hot-set-size'], delim_whitespace=True)
        plt.plot(data['progress'], data['hot-set-size'] / 1e9, linewidth=0.5, marker=version['marker'], markersize=3, markevery=int(len(data['progress']) / 5))
    plt.xlabel('Completed operation count', fontsize=8)
    plt.xticks(fontsize=8)
    ax.ticklabel_format(useMathText=True)
    ax.xaxis.get_offset_text().set_fontsize(8)
    plt.yticks(fig['yticks'])
    if i == 0:
        plt.ylabel('Hot set size (GB)', fontsize=8)
    if 'loc' in fig:
        plt.legend(fig['names'], frameon=False, fontsize=8, loc=fig['loc'])
    else:
        plt.legend(fig['names'], frameon=False, fontsize=8)

pdf_path = dir + '/progress-hot-set-size.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
