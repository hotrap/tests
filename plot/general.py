#!/usr/bin/env python3

import sys
import os
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
ylabel = header[1]
x = []
y = []
for line in sys.stdin:
    line = line.split(' ')
    x.append(int(line[0]))
    y.append(int(line[1]))
plt.plot(x, y)
plt.xlabel(xlabel, fontdict=fonten)
plt.ylabel(ylabel, fontdict=fonten)
plt.show()
