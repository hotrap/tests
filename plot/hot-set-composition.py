#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

fontsize=9
fonten = {'family': 'Times New Roman', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

d = sys.argv[1]
plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/hot-set-composition.pdf'

tracked_size = pd.read_table(d + '/tracked-size', names=["time(s)", "bytes"], delim_whitespace=True)
stably_hot_size = pd.read_table(d + '/stably-hot-size', names=["time(s)", "bytes"], delim_whitespace=True)
plt.plot(tracked_size['time(s)'], tracked_size['bytes'])
plt.plot(stably_hot_size['time(s)'], stably_hot_size['bytes'])
legends = ['Tracked', 'Stably hot']
if os.path.exists(d + '/new-stably-hot-kvsize'):
    new_stably_hot = pd.read_table(d + '/new-stably-hot-kvsize', names=["time(s)", "bytes"], delim_whitespace=True)
    plt.plot(new_stably_hot['time(s)'], new_stably_hot['bytes'])
    legends.append('New stably hot')
if os.path.exists(d + '/kvsize-untracked'):
    kvsize_untrakced = pd.read_table(d + '/kvsize-untracked', names=["time(s)", "bytes"], delim_whitespace=True)
    plt.plot(kvsize_untrakced['time(s)'], kvsize_untrakced['bytes'])
    legends.append('Untracked')
plt.legend(legends, prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Size (bytes)', fontdict=fonten)
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
