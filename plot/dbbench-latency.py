#!/usr/bin/env python3

import sys
if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' data-dir mean-step')
    exit()
data_dir = sys.argv[1]
mean_step = int(sys.argv[2])

import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

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

read = pd.read_table(os.path.join(data_dir, 'read-count-time'), sep='\s+')
write = pd.read_table(os.path.join(data_dir, 'write-count-time'), sep='\s+')
seek = pd.read_table(os.path.join(data_dir, 'seek-count-time'), sep='\s+')

def calc_avg_lat_ns(data):
    micros = data['micros']
    micros = micros[1:].values - micros[:-1].values
    count = data['count']
    count = count[1:].values - count[:-1].values
    ret = pd.DataFrame({
        'secs': data['secs_elapsed'][1:],
        'avg-lat-ns': micros * 1000 / count
    })
    # It seems that the ops of the first several seconds is not limited.
    return ret[10:]

read = calc_avg_lat_ns(read)
write = calc_avg_lat_ns(write)
seek = calc_avg_lat_ns(seek)

def mean_every_n(a, n):
    return a.groupby(a.index // mean_step).mean()

read = mean_every_n(read, mean_step)
write = mean_every_n(write, mean_step)
seek = mean_every_n(seek, mean_step)

ax = plt.gca()
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 4))
ax.yaxis.set_major_formatter(formatter)
ax.yaxis.get_offset_text().set_fontsize(8)
ax.set_yscale('log')
plt.plot(read['secs'], read['avg-lat-ns'], linewidth=0.5)
plt.plot(write['secs'], write['avg-lat-ns'], linewidth=0.5)
plt.plot(seek['secs'], seek['avg-lat-ns'], linewidth=0.5)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.xlabel('Time (Seconds)', fontsize=8)
plt.ylabel('Average latency (ns)', fontsize=8)
plt.legend(['read', 'write', 'seek'], fontsize=8)

plot_dir = data_dir + '/plot'
if not os.path.exists(plot_dir):
    os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/latency.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
    plt.show(block=False)

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(5)), constrained_layout=True)
ax = plt.gca()
plt.plot(read['secs'], read['avg-lat-ns'], linewidth=0.5)
plt.ylim(0, 1e6)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.xlabel('Time (Seconds)', fontsize=8)
plt.ylabel('Average latency (ns)', fontsize=8)

pdf_path = plot_dir + '/latency-read.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
    plt.show()
