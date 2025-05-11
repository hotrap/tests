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
fonten = {'family': 'Linux Libertine O', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
})
plt.rcParams['axes.unicode_minus'] = False

d = sys.argv[1]
cdf = pd.read_table(d + '/hit', sep='\s+')

plt.plot(cdf['key-rank'], cdf['reads'])
legends = ['# accessed']
plt.plot(cdf['key-rank'], cdf['hits'])
legends.append('# hit')
plt.legend(legends, prop={'size': fontsize})
plt.xlabel('Keys ranked by hotness', fontdict=fonten)
plt.ylabel('CDF', fontdict=fonten)

expected_num_reads_of_hot = 110 * 0.1 / 10
last_rank = 0
last_total_reads = 0
last_hot_index = -1
for i, row in cdf.iterrows():
    rank = row['key-rank']
    num_keys = rank - last_rank
    total_reads = row['reads']
    reads = total_reads - last_total_reads
    if reads / num_keys < expected_num_reads_of_hot:
        break
    last_rank = rank
    last_total_reads = total_reads
    last_hot_index = i
plt.axvline(last_rank, linewidth=0.5, linestyle='--', color='black')

last_hot = cdf.iloc[last_hot_index]
total = cdf.iloc[-1]
reads_hot = last_hot['reads']
print('Reads of hot keys: ' + str(reads_hot))
print('Reads of cold keys: ' + str(total['reads'] - reads_hot))
hits_hot = last_hot['hits']
print('Hits of hot keys: ' + str(hits_hot))
print('Hits of cold keys: ' + str(total['hits'] - hits_hot))

print('Hot keys: ' + str(last_rank))
print('Cold keys: ' + str(total['key-rank'] - last_rank))
hot_keys_accessed = last_hot['keys-accessed']
print('Hot keys accessed: ' + str(hot_keys_accessed))
print('Cold keys accessed: ' + str(total['keys-accessed'] - hot_keys_accessed))
hot_keys_with_hit = last_hot['keys-with-hit']
print('Hot keys with hit: ' + str(hot_keys_with_hit))
print("Cold keys with hit: " + str(total['keys-with-hit'] - hot_keys_with_hit))

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
    os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/hit.pdf'
plt.savefig(pdf_path, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
    plt.show()
