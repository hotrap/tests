#!/usr/bin/env python3
import sys
if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' dir twitter-trace-dir')
    exit()
dir = sys.argv[1]
twitter_dir = sys.argv[2]

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common
import twitter_speedup
from twitter_speedup import workload_id, workload_marker

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

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

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(7.5), cm_to_inch(5.2)), constrained_layout=True)

workloads = [
	"cluster01-4168x",
	"cluster02-283x",
	"cluster03-135x",
	"cluster04-3x",
	"cluster05",
	"cluster06-7x",
	"cluster07-12x",
	"cluster08-95x",
	"cluster09-113x",
	"cluster10",
	"cluster11-25x",
	"cluster12",
	"cluster13",
	"cluster14-3x",
	"cluster15",
	"cluster16-67x",
	"cluster17-80x",
	"cluster18-186x",
	"cluster19-3x",
	"cluster20-16x",
	"cluster21-3x",
	"cluster22-9x",
	"cluster23",
	"cluster24-11x",
	"cluster25-215x",
	"cluster26-8x",
	"cluster27-7x",
	"cluster28-18x",
	"cluster29",
	"cluster30-10x",
	"cluster31-2x",
	"cluster32",
	"cluster33-5x",
	"cluster34-9x",
	"cluster35",
	"cluster36-18x",
	"cluster37",
	"cluster38",
	"cluster39",
	"cluster40-5x",
	"cluster41-6x",
	"cluster42-15x",
	"cluster43-4x",
	"cluster44-40x",
	"cluster45-18x",
	"cluster46",
	"cluster47-74x",
	"cluster48-5x",
	"cluster49-17x",
	"cluster50",
	"cluster51-175x",
	"cluster52-3x",
	"cluster53-12x",
	"cluster54-11x"
]


ids = []
xs = []
ys = []
markers = []
sampled = []
not_sampled = []
speedup = []
for (index, workload) in enumerate(workloads):
    id = workload_id(workload)
    ids.append(id)
    x = float(open(os.path.join(twitter_dir, 'stats', workload + '-read-hot-5p-read')).read())
    xs.append(x)
    y = float(open(os.path.join(twitter_dir, 'stats', workload + '-read-with-more-than-5p-write-size')).read())
    ys.append(y)
    markers.append(workload_marker(workload, twitter_dir))
    if workload in twitter_speedup.workloads:
        sampled.append(index)
    else:
        not_sampled.append(index)
for index in not_sampled:
    plt.scatter(xs[index], ys[index], c='gray', alpha=0.5, marker=markers[index])
for index in sampled:
    plt.scatter(xs[index], ys[index], c='black', marker=markers[index])

markersize=5
handles=[
    mlines.Line2D([], [], color='black', marker='o', linestyle='None', markersize=markersize, label='read-heavy'),
    mlines.Line2D([], [], color='black', marker='^', linestyle='None', markersize=markersize, label='read-write'),
    mlines.Line2D([], [], color='black', marker='s', linestyle='None', markersize=markersize, label='write-heavy'),
]
plt.legend(handles=handles, handlelength=0.5, fontsize=9, ncol=len(handles), loc='center', bbox_to_anchor=(0.5, 1.12), handletextpad=0.4, columnspacing=1)

plt.xlim(-0.03, 1.03)
plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize=9)
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize=9)
plt.xlabel('# of reads on hot records / # of reads', fontsize=9)
plt.ylabel('# of reads on sunk records / # of reads', fontsize=9, y=0.45)
pdf_path = os.path.join(dir, 'fig8-twitter-scatter.pdf')
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
