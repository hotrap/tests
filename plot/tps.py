#!/usr/bin/env python3

import sys

if len(sys.argv) != 3:
	print('Usage: ' + sys.argv[0] + ' dir mean_step')
	exit()

import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

fontsize=9
fonten = {'family': 'Linux Libertine O', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

d = sys.argv[1]
mean_step = int(sys.argv[2])

def read_table(file):
    iostat_raw = pd.read_table(file, sep='\s+')
    iostat_raw['Time(Seconds)'] = (iostat_raw['Timestamp(ns)'] - iostat_raw['Timestamp(ns)'][0]) / 1e9
    iostat = iostat_raw[['r/s', 'w/s']].groupby(iostat_raw.index // mean_step).mean()
    iostat['Time(Seconds)'] = iostat_raw['Time(Seconds)'].groupby(iostat_raw.index // mean_step).first()
    return iostat
fd = read_table(d + '/iostat-fd.txt')
sd = read_table(d + '/iostat-sd.txt')

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/tps.pdf'

plt.plot(fd['Time(Seconds)'], fd['r/s'])
plt.plot(fd['Time(Seconds)'], fd['w/s'])
plt.plot(sd['Time(Seconds)'], sd['r/s'])
plt.plot(sd['Time(Seconds)'], sd['w/s'])
plt.legend(['r/s (FD)', 'w/s (FD)', 'r/s (SD)', 'w/s (SD)'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.title('Read/Write per second of FD and SD')
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
