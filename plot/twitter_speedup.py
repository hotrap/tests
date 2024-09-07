#!/usr/bin/env python3

workloads=[
    'cluster02-283x',
    'cluster05',
    'cluster10',
    'cluster11-25x',
    'cluster16-67x',
    'cluster17-80x',
    'cluster18-186x',
    'cluster19-3x',
    'cluster22-9x',
    'cluster23',
    'cluster29',
    'cluster46',
    'cluster48-5x',
    'cluster52-3x',
    'cluster53-12x',
]

read_heavy = set([2, 11, 16, 17, 18, 24, 29, 30, 52, 53])
read_write = set([19, 22, 46, 48])
write_heavy = set([5, 8, 10, 23])

def workload_id(workload):
    return int(workload.split('-')[0][7:])

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: ' + sys.argv[0] + ' dir stat-dir')
        exit()
    dir = sys.argv[1]
    stat_dir = sys.argv[2]

    import os
    sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
    import common
    import twitter_ops

    import io
    import math
    import pandas as pd
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from matplotlib import cm, colors
    import matplotlib.lines as mlines

    # Paper specific settings
    SINGLE_COL_WIDTH = 8.5
    DOUBLE_COL_WIDTH = 17.8
    def cm_to_inch(value):
        return value/2.54

    mpl.rcParams.update({
        'hatch.linewidth': 0.5,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Linux Libertine O'],
        })
    plt.rcParams['axes.unicode_minus'] = False

    fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(5)), constrained_layout=True)
    ax = plt.gca()
    cmap = plt.get_cmap('coolwarm')

    ids = []
    xs = []
    ys = []
    markers = []
    speedups = []
    for workload in workloads:
        id = workload_id(workload)
        ids.append(id)
        x = float(open(os.path.join(stat_dir, workload + '-read-hot-5p-read')).read())
        xs.append(x)
        y = float(open(os.path.join(stat_dir, workload + '-read-with-more-than-5p-write-size')).read())
        ys.append(y)
        if id in read_heavy:
            marker = 'o'
        elif id in read_write:
            marker = '^'
        elif id in write_heavy:
            marker ='s'
        else:
            print('The type of cluster ' + str(id) + ' is unknown')
            exit(1)
        markers.append(marker)

        workload_dir = os.path.join(dir, workload)
        data_dir = os.path.join(workload_dir, 'promote-stably-hot')
        hotrap = common.last_10p_ops(common.VersionData(data_dir))

        data_dir = os.path.join(workload_dir, "rocksdb-tiered")
        rocksdb_tiered = common.last_10p_ops(common.VersionData(data_dir))

        speedup = hotrap / rocksdb_tiered
        speedups.append(speedup)

    max_speedup = max(speedups)
    tex = io.StringIO()
    print('% Max speedup over RocksDB-tiered under twitter production workloads', file=tex)
    print('\defmacro{MaxSpeedupTwitterRocksdbTiered}{%.2f}' %max_speedup, file=tex)

    tex = tex.getvalue()
    print(tex)
    open(os.path.join(dir, 'twitter-speedup.tex'), mode='w').write(tex)

    ceil_max_speedup = math.ceil(max_speedup)
    norm = colors.TwoSlopeNorm(1, vmin=0.9, vmax=ceil_max_speedup)
    norm_cmap = cm.ScalarMappable(norm=norm, cmap=cmap)
    for i in range(0, len(xs)):
        plt.scatter(xs[i], ys[i], marker=markers[i], color=norm_cmap.to_rgba(speedups[i]))

    ticks=[0.9]
    for i in range(1, ceil_max_speedup + 1):
        ticks.append(i)
    cb = plt.colorbar(norm_cmap, ax=ax, ticks=ticks)
    cb.ax.tick_params(labelsize=7)
    for i in range(0, len(xs)):
        if workloads[i] in twitter_ops.workloads:
            plt.text(xs[i] - 0.075, ys[i] - 0.027, '{:02}'.format(ids[i]), fontsize=8, c='black', weight='bold')
        else:
            plt.text(xs[i] - 0.075, ys[i] - 0.027, '{:02}'.format(ids[i]), fontsize=8, c='gray')
        plt.text(xs[i] + 0.025, ys[i] - 0.025, '{:.2f}x'.format(speedups[i]), fontsize=8)

    markersize=5
    handles=[
        mlines.Line2D([], [], color='black', marker='o', linestyle='None', markersize=markersize, label='read-heavy'),
        mlines.Line2D([], [], color='black', marker='^', linestyle='None', markersize=markersize, label='read-write'),
        mlines.Line2D([], [], color='black', marker='s', linestyle='None', markersize=markersize, label='write-heavy'),
    ]
    plt.legend(handles=handles, handlelength=0.5, fontsize=8, ncol=len(handles), loc='center', bbox_to_anchor=(0.5, 1.12))

    plt.xlim(-0.03, 1.03)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize=8)
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize=8)
    plt.xlabel('Proportion of reads on hot records', fontsize=8)
    plt.ylabel('Proportion of reads on sunk records', fontsize=8)
    pdf_path = dir + '/twitter-speedup.pdf'
    plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
    print('Plot saved to ' + pdf_path)
    if 'DISPLAY' in os.environ:
        plt.show()
