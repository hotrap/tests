#!/usr/bin/env python3

import sys
if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' data-dir')
	exit()
data_dir = sys.argv[1]

import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

# Paper specific settings
STANDARD_WIDTH = 17.8
SINGLE_COL_WIDTH = STANDARD_WIDTH / 2
DOUBLE_COL_WIDTH = STANDARD_WIDTH
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
})
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(5)), constrained_layout=True)

report = pd.read_table(os.path.join(data_dir, 'report.csv'), sep=',')
# It seems that the ops of the first several seconds is not limited.
report = report.iloc[20:]

ax = plt.gca()
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 4))
ax.yaxis.set_major_formatter(formatter)
ax.yaxis.get_offset_text().set_fontsize(8)
plt.plot(report['secs_elapsed'], report['interval_qps'], linewidth=0.5)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
ax.set_ylim(bottom=0)
plt.xlabel('Time (Seconds)', fontsize=8)
plt.ylabel('Operation per second', fontsize=8)

plot_dir = data_dir + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/ops.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)

if 'DISPLAY' in os.environ:
	plt.show(block=False)
fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(5)), constrained_layout=True)
hit_rate = report['rocksdb.t0.hit'] / (report['rocksdb.t0.hit'] + report['rocksdb.t1.hit'])
plt.plot(report['secs_elapsed'], hit_rate, linewidth=0.5)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.ylim(0, 1)
plt.xlabel('Time (Seconds)', fontsize=8)
plt.ylabel('Hit rate', fontsize=8)
pdf_path = plot_dir + '/hit-rate.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)

if 'hotrap.scan.hit.t0' in report:
    if 'DISPLAY' in os.environ:
        plt.show(block=False)
    fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(5)), constrained_layout=True)
    hit_rate = report['hotrap.scan.hit.t0'] / (report['hotrap.scan.hit.t0'] + report['hotrap.scan.hit.t1'])
    plt.plot(report['secs_elapsed'], hit_rate, linewidth=0.5)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.ylim(0, 1)
    plt.xlabel('Time (Seconds)', fontsize=8)
    plt.ylabel('Range tit rate', fontsize=8)
    pdf_path = plot_dir + '/range-hit-rate.pdf'
    plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01, metadata={'CreationDate': None})
    print('Plot saved to ' + pdf_path)

if 'DISPLAY' in os.environ:
	plt.show()
