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

mpl.rcParams.update({
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
})
plt.rcParams['axes.unicode_minus'] = False

SINGLE_COL_WIDTH = 8.5
def cm_to_inch(value):
    return value/2.54
fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(3.5)), constrained_layout=True)

tests = [
    {
        'workload': 'ycsbc',
        'version': 'hotrap',
        'linewidth': 1.0,
        'marker': 'o',
    },
    {
        'workload': 'read_0.5_insert_0.5',
        'version': 'no-promote-by-flush',
        'linewidth': 1.0,
        'marker': 'v',
    },
    {
        'workload': 'read_0.75_insert_0.25',
        'version': 'no-promote-by-flush',
        'linewidth': 1.0,
        'marker': '^',
    },
    {
        'workload': 'read_0.85_insert_0.15',
        'version': 'no-promote-by-flush',
        'linewidth': 0.7,
        'marker': 's',
    },
    {
        'workload': 'read_0.95_insert_0.05',
        'version': 'no-promote-by-flush',
        'linewidth': 0.5,
        'marker': 'X',
    },
    {
        'workload': 'ycsbc',
        'version': 'no-promote-by-flush',
        'linewidth': 1.0,
        'marker': 'D',
    },
]
skewness = 'hotspot0.05'
size = '110GB_220GB'

ax = plt.gca()
for test in tests:
    workload = test['workload'] + '_' + skewness + '_' + size
    data_dir = os.path.join(dir, workload, test['version'])
    version_data = common.VersionData(data_dir)
    hit_rates = common.read_hit_rates(data_dir)
    (x, hit_rates) = common.estimate(version_data, hit_rates, 'hit-rate')
    plt.plot(x, hit_rates, linewidth=test['linewidth'], marker=test['marker'], markersize=4, markevery=int(len(x) / 5))

plt.xlabel('Completed operation count', fontsize=9, loc='center', labelpad=1.5)
plt.xticks(fontsize=9)
ax.ticklabel_format(useMathText=True)
ax.xaxis.get_offset_text().set_fontsize(9)
plt.ylabel('Hit rate', fontsize=9)
plt.yticks(np.linspace(0, 1, 6), fontsize=9)
legend = fig.legend([common.sysname + ' 0% W', 'no-flush 50% W', 'no-flush 25% W', 'no-flush 15% W', 'no-flush 5% W', 'no-flush 0% W'], frameon=False, fontsize=9, ncol=3, loc='center', bbox_to_anchor=(0.5, 1.1), handlelength=1.3, handletextpad=0.3, columnspacing=0.7)

pdf_path = dir + '/progress-hit-rate-' + skewness + '.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
