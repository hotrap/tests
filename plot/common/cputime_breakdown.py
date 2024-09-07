import common

import os
import json5
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter

def draw_cputime_breakdown(dir, size, pdf_name):
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

    figure = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(4)), constrained_layout=True)
    gs = gridspec.GridSpec(1, 2, figure=figure)

    workload='hotspot0.05'
    ycsb_configs=['ycsbc', 'read_0.75_insert_0.25', 'read_0.5_insert_0.5', 'ycsba']
    cluster_labels = ['RO', 'RW', 'WH', 'UH']
    colors_rocksdb = [
        plt.get_cmap('Paired')(0),
        plt.get_cmap('Paired')(2),
        plt.get_cmap('Paired')(4),
        'white',
    ]
    colors_hotrap = [
        plt.get_cmap('Paired')(1),
        plt.get_cmap('Paired')(3),
        plt.get_cmap('Paired')(5),
        plt.get_cmap('Paired')(7),
        plt.get_cmap('Paired')(9),
        'white',
    ]

    promote_stably_hot = {
        'path': 'promote-stably-hot',
        'colors': colors_hotrap,
    }
    rocksdb_fd = {
        'path': 'rocksdb-fd',
        'colors': colors_rocksdb,
    }
    rocksdb_tiered = {
        'path': 'rocksdb-tiered',
        'colors': colors_rocksdb,
    }
    patterns = ['///', '\\\\\\', 'XXX', '......', '', '']

    versions=[rocksdb_fd, promote_stably_hot]
    bar_width = 1 / (len(versions) + 1)
    cluster_width = bar_width * len(versions)
    subfig_anchor_x = 0.46
    subfig_anchor_y = 1.28

    def draw_cputime(min_max_portion):
        ax = plt.gca()
        ax.set_axisbelow(True)
        ax.grid(axis='y')
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_powerlimits((-3, 3))
        ax.yaxis.set_major_formatter(formatter)
        ax.yaxis.get_offset_text().set_fontsize(8)
        for (pivot, ycsb) in enumerate(ycsb_configs):
            workload_dir = os.path.join(dir, ycsb + '_' + workload + '_' + size)
            for (version_idx, version) in enumerate(versions):
                data_dir = os.path.join(workload_dir, version['path'])
                x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
                version_data = common.VersionData(data_dir)
                cputimes = pd.read_table(os.path.join(data_dir, 'cputimes'), sep='\s+')
                cputimes = version_data.run_phase(cputimes)
                cputimes = cputimes['cputime(s)'].iloc[-1] - cputimes['cputime(s)'].iloc[0]
                timers = pd.read_table(os.path.join(data_dir, 'timers'), sep='\s+')
                timers = version_data.run_phase(timers)
                timers = timers.iloc[-1] - timers.iloc[0]
                bottom = 0

                height = timers['get-cpu-nanos'] / 1e9
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[0], color=version['colors'][0], edgecolor='black', linewidth=0.5)
                bottom += height

                height = timers['put-cpu-nanos'] / 1e9
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[1], color=version['colors'][1], edgecolor='black', linewidth=0.5)
                bottom += height

                height = timers['compaction-cpu-micros'] / 1e6
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[2], color=version['colors'][2], edgecolor='black', linewidth=0.5)
                bottom += height
                if version_idx == 1:
                    first_level_in_sd = int(open(os.path.join(data_dir, 'first-level-in-sd')).read())
                    checker = pd.read_table(os.path.join(data_dir, 'checker-' + str(first_level_in_sd - 1) + '-cputime'), sep='\s+')
                    checker = version_data.run_phase(checker)
                    height = (checker.iloc[-1] - checker.iloc[0])['cputime(ns)'] / 1e9
                    ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[3], color=version['colors'][3], edgecolor='black', linewidth=0.5)
                    bottom += height

                    height = (timers['viscnts.compaction.thread.cpu.nanos'] + timers['viscnts.flush.thread.cpu.nanos'] + timers['viscnts.decay.thread.cpu.nanos']) / 1e9
                    portion = height / cputimes
                    min_max_portion[0] = min(min_max_portion[0], portion)
                    min_max_portion[1] = max(min_max_portion[1], portion)
                    ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[4], color=version['colors'][4], edgecolor='black', linewidth=0.5)
                    bottom += height
                height = cputimes - bottom
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[-1], color=version['colors'][-1], edgecolor='black', linewidth=0.5)
        plt.xticks(range(0, len(cluster_labels)), cluster_labels, fontsize=8)
        plt.yticks(fontsize=8)
        plt.locator_params(axis='y', nbins=4)
        plt.ylabel('CPU time (seconds)', fontsize=8)

    min_max_portion = [1, 0]

    subfig = plt.subplot(gs[0, 0])
    draw_cputime(min_max_portion)
    plt.xlabel('(a) hotspot-5%', fontsize=8)
    subfig.legend(
        [
            common.MulticolorPatch(colors=rocksdb_fd['colors']),
            common.MulticolorPatch(colors=promote_stably_hot['colors']),
        ],
        ['RocksDB(FD)', 'HotRAP'],
        handler_map={common.MulticolorPatch: common.MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(subfig_anchor_x, subfig_anchor_y), columnspacing=1,
    )

    workload='uniform'
    versions = [rocksdb_tiered, promote_stably_hot]
    subfig = plt.subplot(gs[0, 1])
    draw_cputime(min_max_portion)
    plt.xlabel('(b) uniform', fontsize=8)
    subfig.legend(
        [
            common.MulticolorPatch(colors=rocksdb_tiered['colors']),
            common.MulticolorPatch(colors=promote_stably_hot['colors']),
        ],
        ['RocksDB-tiered', 'HotRAP'],
        handler_map={common.MulticolorPatch: common.MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(subfig_anchor_x, subfig_anchor_y), columnspacing=1,
    )

    labels = []
    handles = []
    def all_versions(i):
        handles.append(common.MulticolorPatch(
            colors=[
                colors_rocksdb[i],
                colors_hotrap[i],
            ],
            pattern=patterns[i],
        ))
    labels.append('Read')
    all_versions(0)
    labels.append('Insert')
    all_versions(1)
    labels.append('Compaction')
    all_versions(2)
    labels.append('Checker')
    handles.append(common.MulticolorPatch(colors=[promote_stably_hot['colors'][3]], pattern=patterns[3]))
    labels.append('RALT')
    handles.append(common.MulticolorPatch(colors=[promote_stably_hot['colors'][4]], pattern=patterns[4]))
    labels.append('Others')
    assert colors_hotrap[-1] == colors_rocksdb[-1]
    handles.append(common.MulticolorPatch(colors=[colors_rocksdb[-1]], pattern=patterns[-1]))
    figure.legend(
        handles, labels,
        handler_map={common.MulticolorPatch: common.MulticolorPatchHandler()},
        fontsize=8, ncol=3, loc='center', bbox_to_anchor=(0.5, 1.13), columnspacing=1
    )
    pdf_path = os.path.join(dir, pdf_name)
    plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
    print('Plot saved to ' + pdf_path)
    if 'DISPLAY' in os.environ:
        plt.show()
    return (min_max_portion[0], min_max_portion[1])
