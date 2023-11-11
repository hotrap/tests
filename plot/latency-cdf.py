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

abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)

d = sys.argv[1]
plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)

types = ['read', 'insert', 'update', 'rmw']
for t in types:
    path = os.path.join(d, t + '-latency-cdf')
    if not os.path.exists(path):
        continue
    cdf = pd.read_table(path, delim_whitespace=True, names=['latency', 'cdf'])
    pdf_path = os.path.join(plot_dir, t + '-latency-cdf.pdf')
    ax = plt.gca()
    plt.plot(cdf['latency'], (1 - cdf['cdf']))
    plt.xscale('log')
    plt.yscale('log')
    #plt.ylim(1e-4, 1)
    ax.invert_yaxis()
    ax.yaxis.set_major_formatter(lambda y, pos: 1 - y)
    plt.xlabel('Latency(ns)', fontdict=fonten)
    plt.ylabel('CDF', fontdict=fonten)
    plt.savefig(pdf_path)
    print('Plot saved to ' + pdf_path)
