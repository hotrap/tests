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
cpu = pd.read_table(d + '/cpu', delim_whitespace=True, names=['Timestamp(s)', 'cpu'])
time = cpu['Timestamp(s)'] - cpu['Timestamp(s)'][0]
cpu = cpu['cpu']

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/cpu.pdf'
plt.plot(time, cpu)
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('CPU (%)', fontdict=fonten)
plt.title('CPU usage')
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
