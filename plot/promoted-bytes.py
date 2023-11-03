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
promoted_bytes = pd.read_table(d + '/promoted-bytes', delim_whitespace=True)
timestamp = (promoted_bytes['Timestamp(ns)'] - promoted_bytes['Timestamp(ns)'][0]) / 1e9

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/promoted-bytes.pdf'
plt.plot(timestamp, promoted_bytes['by-flush'])
plt.plot(timestamp, promoted_bytes['2sdlast'])
plt.plot(timestamp, promoted_bytes['2cdfront'])
plt.legend(['By flush to L0', 'To the last level in SD', 'To shallower levels in CD'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Promoted bytes', fontdict=fonten)
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
