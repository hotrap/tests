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
fonten = {'family': 'Times New Roman', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

d = sys.argv[1]
mean_step = int(sys.argv[2])

def read_table(file):
    iostat_raw = pd.read_table(file, delim_whitespace=True)
    iostat_raw['Time(Seconds)'] = (iostat_raw['Timestamp(ns)'] - iostat_raw['Timestamp(ns)'][0]) / 1e9
    iostat = iostat_raw[['rkB/s', 'wkB/s']].groupby(iostat_raw.index // mean_step).mean()
    iostat['Time(Seconds)'] = iostat_raw['Time(Seconds)'].groupby(iostat_raw.index // mean_step).first()
    return iostat
sd = read_table(d + '/iostat-sd.txt')
cd = read_table(d + '/iostat-cd.txt')

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/throughput.pdf'

plt.plot(sd['Time(Seconds)'], sd['rkB/s'] * 1024 / 1e6)
plt.plot(sd['Time(Seconds)'], sd['wkB/s'] * 1024 / 1e6)
plt.plot(cd['Time(Seconds)'], cd['rkB/s'] * 1024 / 1e6)
plt.plot(cd['Time(Seconds)'], cd['wkB/s'] * 1024 / 1e6)
plt.legend(['read (SD)', 'write (SD)', 'read (CD)', 'write (CD)'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Throughput (MB/s)', fontdict=fonten)
plt.title('Throughput of SD and CD')
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
