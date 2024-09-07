import common

import os
import json5
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter
from matplotlib.patches import Patch

# Return min and max ralt portion
def draw_io_breakdown(dir, size, pdf_name):
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

    figure = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(3.7)), constrained_layout=True)
    gs = gridspec.GridSpec(1, 2, figure=figure)

    workload='hotspot0.05'
    ycsb_configs=['ycsbc', 'read_0.75_insert_0.25', 'read_0.5_insert_0.5', 'ycsba']
    cluster_labels = ['RO', 'RW', 'WH', 'UH']
    colors_hotrap = [
        plt.get_cmap('Paired')(1), plt.get_cmap('Paired')(3),
        plt.get_cmap('Paired')(5), plt.get_cmap('Paired')(7),
        plt.get_cmap('Paired')(9),
        'white',
    ]
    colors_rocksdb = [
        plt.get_cmap('Paired')(0), plt.get_cmap('Paired')(2),
        plt.get_cmap('Paired')(4), plt.get_cmap('Paired')(6),
        'white',
    ]
    promote_stably_hot = {
        'path': 'promote-stably-hot',
        'colors': colors_hotrap,
        'legend-colors': colors_hotrap,
    }
    rocksdb_fd = {
        'path': 'rocksdb-fd',
        'colors': colors_rocksdb,
        'legend-colors': [colors_rocksdb[i] for i in [1, 3, 4]],
    }
    rocksdb_tiered = {
        'path': 'rocksdb-tiered',
        'colors': colors_rocksdb,
        'legend-colors': colors_rocksdb,
    }
    patterns = ['///', '\\\\\\', '......', 'XXX', '', '']

    versions=[rocksdb_fd, promote_stably_hot]
    bar_width = 1 / (len(versions) + 1)
    cluster_width = bar_width * len(versions)
    subfig_anchor_x = 0.46
    subfig_anchor_y = 1.11

    def draw_io(min_max_portion):
        ax = plt.gca()
        ax.set_axisbelow(True)
        ax.grid(axis='y')
        for (pivot, ycsb) in enumerate(ycsb_configs):
            workload_dir = os.path.join(dir, ycsb + '_' + workload + '_' + size)
            for (version_idx, version) in enumerate(versions):
                data_dir = os.path.join(workload_dir, version['path'])
                x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
                version_data = common.VersionData(data_dir)
                first_level_in_sd = int(open(os.path.join(data_dir, 'first-level-in-sd')).read())
                def run_time_io_kB(fname):
                    iostat = pd.read_table(os.path.join(data_dir, fname), sep='\s+')
                    iostat = version_data.run_phase(iostat)
                    return iostat[['rkB/s', 'wkB/s']].sum().sum()
                device_io = (run_time_io_kB('iostat-fd.txt') + run_time_io_kB('iostat-sd.txt')) / 1e9

                bottom = 0

                rand_read_bytes = common.read_rand_read_bytes_fd_sd(data_dir, first_level_in_sd)
                rand_read_bytes = version_data.run_phase(rand_read_bytes)
                rand_read_bytes = rand_read_bytes.iloc[-1] - rand_read_bytes.iloc[0]

                if version['path'] == 'rocksdb-fd':
                    assert rand_read_bytes['sd'] == 0
                else:
                    height = rand_read_bytes['sd'] / 1e12
                    ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[0], color=version['colors'][0], edgecolor='black', linewidth=0.5)
                    bottom += height

                height = rand_read_bytes['fd'] / 1e12
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[1], color=version['colors'][1], edgecolor='black', linewidth=0.5)
                bottom += height

                compaction_bytes = common.read_compaction_bytes_fd_sd(data_dir, first_level_in_sd)
                compaction_bytes = version_data.run_phase(compaction_bytes)
                compaction_bytes = compaction_bytes.iloc[-1] - compaction_bytes.iloc[0]

                if version['path'] == 'rocksdb-fd':
                    assert compaction_bytes['sd-read'] == 0
                    assert compaction_bytes['sd-write'] == 0
                else:
                    height = (compaction_bytes['sd-read'] + compaction_bytes['sd-write']) / 1e12
                    ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[2], color=version['colors'][2], edgecolor='black', linewidth=0.5)
                    bottom += height

                height = (compaction_bytes['fd-read'] + compaction_bytes['fd-write']) / 1e12
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[3], color=version['colors'][3], edgecolor='black', linewidth=0.5)
                bottom += height

                if version['path'] == 'promote-stably-hot':
                    viscnts_io = pd.read_table(os.path.join(data_dir, 'viscnts-io'), sep='\s+')
                    viscnts_io = version_data.run_phase(viscnts_io)
                    viscnts_io = viscnts_io.iloc[-1] - viscnts_io.iloc[0]
                    height = (viscnts_io['read'] + viscnts_io['write']) / 1e12
                    portion = height / device_io
                    min_max_portion[0] = min(min_max_portion[0], portion)
                    min_max_portion[1] = max(min_max_portion[1], portion)
                    ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[4], color=version['colors'][4], edgecolor='black', linewidth=0.5)
                    bottom += height

                height = device_io - bottom
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[-1], color=version['colors'][-1], edgecolor='black', linewidth=0.5)
        plt.xticks(range(0, len(cluster_labels)), cluster_labels, fontsize=8)
        plt.yticks(fontsize=8)
        plt.ylabel('I/O (TB)', fontsize=8)

    min_max_portion = [1, 0]

    subfig = plt.subplot(gs[0, 0])
    draw_io(min_max_portion)
    plt.xlabel('(a) hotspot-5%', fontsize=8)
    subfig.legend(
        [
            common.MulticolorPatch(colors=rocksdb_fd['legend-colors']),
            common.MulticolorPatch(colors=promote_stably_hot['legend-colors']),
        ],
        ['RocksDB(FD)', 'HotRAP'],
        handler_map={common.MulticolorPatch: common.MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(subfig_anchor_x, subfig_anchor_y), columnspacing=1,
    )

    workload='uniform'
    versions = [rocksdb_tiered, promote_stably_hot]
    subfig = plt.subplot(gs[0, 1])
    draw_io(min_max_portion)
    plt.xlabel('(b) uniform', fontsize=8)
    subfig.legend(
        [
            common.MulticolorPatch(colors=rocksdb_tiered['legend-colors']),
            common.MulticolorPatch(colors=promote_stably_hot['legend-colors']),
        ],
        ['RocksDB-tiered', 'HotRAP'],
        handler_map={common.MulticolorPatch: common.MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(subfig_anchor_x, subfig_anchor_y), columnspacing=1,
    )

    def get_fig_legend(i):
        return common.MulticolorPatch(colors=[colors_rocksdb[i], colors_hotrap[i]], pattern=patterns[i])
    labels = []
    handles = []
    labels.append(r'Get in SD')
    handles.append(get_fig_legend(0))
    labels.append(r'Get in FD')
    handles.append(get_fig_legend(1))
    labels.append('Compaction in SD')
    handles.append(get_fig_legend(2))
    labels.append('Compaction in FD')
    handles.append(get_fig_legend(3))
    labels.append('RALT')
    handles.append(common.MulticolorPatch(colors=[colors_hotrap[4]], pattern=patterns[4]))
    labels.append('Others')
    assert colors_hotrap[-1] == colors_rocksdb[-1]
    handles.append(common.MulticolorPatch(colors=[colors_hotrap[-1]], pattern=patterns[-1]))
    figure.legend(
        handles, labels,
        handler_map={common.MulticolorPatch: common.MulticolorPatchHandler()},
        fontsize=8, ncol=3, loc='center', bbox_to_anchor=(0.5, 1.11)
    )

    pdf_path = os.path.join(dir, pdf_name)
    plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
    print('Plot saved to ' + pdf_path)
    if 'DISPLAY' in os.environ:
        plt.show()
    return (min_max_portion[0], min_max_portion[1])
