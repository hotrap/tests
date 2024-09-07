#!/usr/bin/env python3

workloads=[
    'cluster11-25x',
    'cluster17-80x',
    'cluster19-3x',
    'cluster16-67x',
    'cluster53-12x',
    'cluster10',
    'cluster29',
]

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' dir')
        exit()
    dir = sys.argv[1]

    import os
    sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
    import common

    import io
    import pandas as pd
    import matplotlib as mpl
    import matplotlib.pyplot as plt

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

    fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(3.5)), constrained_layout=True)

    versions=[
        {
            'path': 'rocksdb-fd',
            'pattern': 'XXXXXXXXX',
            'color': plt.get_cmap('Set2')(2),
        },
        {
            'path': 'rocksdb-tiered',
            'pattern': '\\\\\\',
            'color': plt.get_cmap('Set2')(1),
        },
        {
            'path': 'prismdb',
            'pattern': '---\\\\\\\\\\\\',
            'color': plt.get_cmap('Set2')(5),
        },
        {
            'path': 'SAS-Cache',
            'pattern': 'XXX',
            'color': plt.get_cmap('Set2')(3),
        },
        {
            'path': 'promote-stably-hot',
            'pattern': '///',
            'color': plt.get_cmap('Set2')(0),
        },
    ]
    version_names = ['RocksDB(FD)', 'RocksDB-tiered', 'PrismDB', 'SAS-Cache', 'HotRAP']

    workload_version_ops = {}
    for workload in workloads:
        workload_dir = os.path.join(dir, workload)
        workload_version_ops[workload] = {}
        for version in versions:
            data_dir = os.path.join(workload_dir, version['path'])
            workload_version_ops[workload][version['path']] = common.last_10p_ops(common.VersionData(data_dir))

    max_speedup = 0
    for workload in workloads:
        version_ops = workload_version_ops[workload]
        hotrap_ops = version_ops['promote-stably-hot']
        other_sys_max_ops = 0
        for version in versions:
            version = version['path']
            if version == 'promote-stably-hot' or version == 'rocksdb-fd':
                continue
            other_sys_max_ops = max(other_sys_max_ops, version_ops[version])
        assert other_sys_max_ops > 0
        max_speedup = max(max_speedup, hotrap_ops / other_sys_max_ops)
    tex = io.StringIO()
    print('% Max speedup over second best under twitter production workloads', file=tex)
    print('\defmacro{MaxSpeedupTwitter}{%.1f}' %max_speedup, file=tex)

    tex = tex.getvalue()
    print(tex)
    open(os.path.join(dir, 'twitter.tex'), mode='w').write(tex)

    bar_width = 1 / (len(versions) + 1)
    cluster_width = bar_width * len(versions)

    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.grid(axis='y')
    ids = []
    for (pivot, workload) in enumerate(workloads):
        ids.append(workload.split('-')[0][7:])
        for (version_idx, version) in enumerate(versions):
            x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
            value = workload_version_ops[workload][version['path']]
            ax.bar(x, value, width=bar_width, hatch=version['pattern'], color=version['color'], edgecolor='black', linewidth=0.5)
    ax.ticklabel_format(style='sci', scilimits=(4, 4), useMathText=True)
    ax.yaxis.get_offset_text().set_fontsize(8)
    plt.xticks(range(0, len(workloads)), ids, fontsize=8)
    plt.yticks([0, 5e4, 10e4, 15e4, 20e4], fontsize=8)
    plt.xlabel('Cluster ID', labelpad=1, fontsize=8)
    plt.ylabel('Operations per second', fontsize=8)
    fig.legend(version_names, fontsize=8, ncol=3, loc='center', bbox_to_anchor=(0.5, 1.12))
    pdf_path = dir + '/twitter-ops.pdf'
    plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
    print('Plot saved to ' + pdf_path)
    if 'DISPLAY' in os.environ:
        plt.show()
