#!/usr/bin/env python3

import sys
import getopt
def print_help():
    print(sys.argv[0] + ' [-o <outputfile>] [-t line|scatter] [--xlable=] [--ylabel=] [--title] [--xscale] [--scatter-label] [--scatter-color] [--scatter-tooltip]')

try:
    opts, args = getopt.getopt(sys.argv[1:], 'ho:t:', ['xlabel=', 'ylabel=', 'title=', 'xscale=', 'scatter-label', 'scatter-color', 'scatter-tooltip'])
except getopt.GetoptError:
    print_help()
    exit(1)

pdf_path = None
chart_type = 'line'
xlabel = None
ylabel = None
title = None
xscale = None
scatter_label = False
scatter_color = False
scatter_tooltip = False
for opt, arg in opts:
    if opt == '-h':
        print_help()
        exit()
    elif opt == '-o':
        pdf_path = arg
    elif opt == '-t':
        chart_type = arg
    elif opt == '--xlabel':
        xlabel = arg
    elif opt == '--ylabel':
        ylabel = arg
    elif opt == '--title':
        title = arg
    elif opt == '--xscale':
        xscale = arg
    elif opt == '--scatter-label':
        scatter_label = True
    elif opt == '--scatter-color':
        scatter_color = True
    elif opt == '--scatter-tooltip':
        scatter_tooltip = True

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
    line = shlex.split(sys.stdin.readline())
    n = len(line)
    c = [[v] for v in line]
for line in sys.stdin:
    line = shlex.split(line)
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
    args = {
        'x': [float(v) for v in c[0]],
        'y': [float(v) for v in c[1]],
    }
    i = 2
    if scatter_label:
        labels = c[i]
        i += 1
    if scatter_color:
        args['c'] = c[i]
        i += 1
    if scatter_tooltip:
        tooltips = c[i]
        i += 1
    assert i == len(c)
    scatter = ax.scatter(**args)
ax.set_xlabel(xlabel, fontdict=fonten)
if ylabel is not None:
    ax.set_ylabel(ylabel, fontdict=fonten)
if title is not None:
    ax.set_title(title, fontdict=fonten)
if xscale is not None:
    ax.set_xscale(xscale)
if legends is not None:
    plt.legend(legends, prop={'size': fontsize})
if scatter_label:
    for i in range(0, len(labels)):
        plt.text(args['x'][i] + 0.01, args['y'][i], labels[i], fontsize=6)
if pdf_path is not None:
    plt.savefig(pdf_path)
    print('Plot saved to ' + pdf_path)
if scatter_tooltip:
    assert chart_type == 'scatter'
    import mpld3
    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=tooltips)
    mpld3.plugins.connect(fig, tooltip)
    mpld3.show()
elif 'DISPLAY' in os.environ:
	plt.show()
