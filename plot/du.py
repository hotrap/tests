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
fonten = {'family': 'Linux Libertine O', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

d = sys.argv[1]
du = pd.read_table(d + '/du.sh.txt', sep='\s+')
time = (du['Timestamp(ns)'] - du['Timestamp(ns)'][0]) / 1e9

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/du.pdf'
plt.plot(time, du['DB'])
plt.plot(time, du['FD'])
plt.plot(time, du['SD'])
plt.plot(time, du['RALT'])
plt.legend(['DB', 'FD', 'SD', 'RALT'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Size (Bytes)', fontdict=fonten)
plt.title('Disk usage of DB, FD, and SD')
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
