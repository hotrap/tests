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
du = pd.read_table(d + '/du.sh.txt', delim_whitespace=True)

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/du.pdf'
plt.plot(du['Timestamp(ns)'] / 1e9, du['DB'])
plt.plot(du['Timestamp(ns)'] / 1e9, du['SD'])
plt.plot(du['Timestamp(ns)'] / 1e9, du['CD'])
plt.legend(['DB', 'SD', 'CD'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Size (Bytes)', fontdict=fonten)
plt.title('Disk usage of DB, SD, and CD')
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
