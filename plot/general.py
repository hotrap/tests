#!/usr/bin/env python3

import sys
import os

if len(sys.argv) < 2 and 'DISPLAY' not in os.environ:
    print('Error: No display and no output file.')
    exit(1)

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import shlex

fontsize=9
fonten = {'family': 'Times New Roman', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

header = shlex.split(sys.stdin.readline())
xlabel = header[0]
legends = header[1:]
n = len(legends)
x = []
ys = []
for _ in range(0, n):
    ys.append([])
for line in sys.stdin:
    line = line.split(' ')
    x.append(float(line[0]))
    for i in range(0, n):
        ys[i].append(int(line[i+1]))
for y in ys:
    plt.plot(x, y)
plt.xlabel(xlabel, fontdict=fonten)
plt.legend(legends, prop={'size': fontsize})
if len(sys.argv) == 2:
    pdf_path = sys.argv[1]
    plt.savefig(pdf_path)
    print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
