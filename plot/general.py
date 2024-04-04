#!/usr/bin/env python3

import sys
import getopt
def print_help():
    print(sys.argv[0] + ' [-o <outputfile>] [--xlable=] [--ylabel=]')

try:
    opts, args = getopt.getopt(sys.argv[1:], 'ho:', ['xlabel=', 'ylabel='])
except getopt.GetoptError:
    print_help()
    exit(1)

pdf_path = None
xlabel = None
ylabel = None
for opt, arg in opts:
    if opt == '-h':
        print_help()
        exit()
    elif opt == '-o':
        pdf_path = arg
    elif opt == '--xlabel':
        xlabel = arg
    elif opt == '--ylabel':
        ylabel = arg

if xlabel is not None:
    assert ylabel is not None
 
import os
if pdf_path is None and 'DISPLAY' not in os.environ:
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

legends = None
if xlabel is None:
    header = shlex.split(sys.stdin.readline())
    xlabel = header[0]
    legends = header[1:]
    n = len(legends)
else:
    n = 1
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
if ylabel is not None:
    plt.ylabel(ylabel, fontdict=fonten)
if legends is not None:
    plt.legend(legends, prop={'size': fontsize})
if pdf_path is not None:
    plt.savefig(pdf_path)
    print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
