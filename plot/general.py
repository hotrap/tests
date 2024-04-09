#!/usr/bin/env python3

import sys
import getopt
def print_help():
    print(sys.argv[0] + ' [-o <outputfile>] [-t line|scatter] [--xlable=] [--ylabel=]')

try:
    opts, args = getopt.getopt(sys.argv[1:], 'ho:t:i', ['xlabel=', 'ylabel='])
except getopt.GetoptError:
    print_help()
    exit(1)

pdf_path = None
chart_type = 'line'
interactive = False
xlabel = None
ylabel = None
for opt, arg in opts:
    if opt == '-h':
        print_help()
        exit()
    elif opt == '-o':
        pdf_path = arg
    elif opt == '-t':
        chart_type = arg
    elif opt == '-i':
        interactive = True
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
    n = len(header)
    xlabel = header[0]
    legends = header[1:]
    c = [[] for _ in range(0, n)]
else:
    line = sys.stdin.readline().rstrip().split(' ')
    n = len(line)
    c = [[v] for v in line]
for line in sys.stdin:
    line = line.rstrip().split(' ')
    assert len(line) == n
    for i in range(0, n):
        c[i].append(line[i])

fig, ax = plt.subplots()
if chart_type == 'line':
    x = [float(v) for v in c[0]]
    for y in c[1:]:
        y = [float(v) for v in y]
        ax.plot(x, y)
else:
    assert chart_type == 'scatter'
    assert len(c) == 3
    x = [float(v) for v in c[0]]
    y = [float(v) for v in c[1]]
    labels = c[2]
    scatter = ax.scatter(x, y)
ax.set_xlabel(xlabel, fontdict=fonten)
if ylabel is not None:
    ax.set_ylabel(ylabel, fontdict=fonten)
if legends is not None:
    plt.legend(legends, prop={'size': fontsize})
if pdf_path is not None:
    plt.savefig(pdf_path)
    print('Plot saved to ' + pdf_path)
if interactive:
    assert chart_type == 'scatter'
    import mpld3
    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
    mpld3.plugins.connect(fig, tooltip)
    mpld3.show()
elif 'DISPLAY' in os.environ:
	plt.show()
