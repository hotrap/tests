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

dir = sys.argv[1]

tests = [
    {
        'workload': 'read_0.5_insert_0.5_hotspot0.01_110GB',
        'workload-name': 'read-0.5-insert-0.5-hotspot',
        'operations': ['read', 'insert'],
    },
    {
        'workload': 'ycsbc_hotspot0.01_110GB',
        'workload-name': 'ycsbc-hotspot',
        'operations': ['read'],
    },
]
versions=['flush-stably-hot', 'rocksdb-fat']
percentiles = ['0.1', '0.3', '0.5', '0.7', '0.9', '0.99', '0.999', 'Max']
for test in tests:
    workload = test['workload']
    operations = test['operations']
    pdf_path = os.path.join(dir, test['workload-name'] + '-latency.pdf')
    plt.figure()
    legends=[]
    for operation in operations:
        for version in versions:
            data_dir = os.path.join(dir, workload, version)
            path = os.path.join(data_dir, operation + '-latency')
            latency = pd.read_table(path, delim_whitespace=True, names=['percentile', 'ns'])
            latency = latency.set_index('percentile').to_dict()['ns']
            y = []
            for percentile in percentiles:
                y.append(latency[percentile])
            plt.plot(percentiles, y)
            plt.yscale('log')
            if len(operations) == 1:
                legends.append(version)
            else:
                legends.append(version + '-' + operation)
    plt.legend(legends, prop={'size': fontsize})
    plt.xlabel('Percentiles', fontdict=fonten)
    plt.ylabel('Latency (ns)', fontdict=fonten)
    plt.savefig(pdf_path)
    print('Plot saved to ' + pdf_path)
