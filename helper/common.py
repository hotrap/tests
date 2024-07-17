import os
import json5
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# https://stackoverflow.com/a/77614517/13688160
# define an object that will be used by the legend
class MulticolorPatch(object):
    def __init__(self, colors, pattern=None):
        self.colors = colors
        self.pattern = pattern
class MulticolorPatchHandler(object):
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        width, height = handlebox.width, handlebox.height
        for i, c in enumerate(orig_handle.colors):
            patch = plt.Rectangle(
                [
                    width/len(orig_handle.colors) * i - handlebox.xdescent,
                    -handlebox.ydescent,
                ],
                width / len(orig_handle.colors),
                height, 
                facecolor=c, 
                edgecolor='black',
                hatch=orig_handle.pattern,
            )
            if i == 0:
                ret = patch
            handlebox.add_artist(patch)
        return ret

def read_hit_rates(data_dir):
    first_level_in_sd = int(open(os.path.join(data_dir, 'first-level-in-sd')).read())
    last_tier0 = 0
    last_total = 0
    hit_rates = []
    for line in open(os.path.join(data_dir, 'num-accesses')):
        res = line.split(' ')
        timestamp = int(res[0])
        tier0 = 0
        total = 0
        for (level, num_accesses) in enumerate(res[1:]):
            num_accesses = int(num_accesses)
            total += num_accesses
            if level < first_level_in_sd:
                tier0 += num_accesses
        if total - last_total != 0:
            hit_rate = (tier0 - last_tier0) / (total - last_total)
            hit_rates.append(pd.Series([timestamp, hit_rate]))
            last_tier0 = tier0
            last_total = total
    hit_rates = pd.concat(hit_rates, axis=1).T
    hit_rates.columns = ['Timestamp(ns)', 'hit-rate']
    return hit_rates

def timestamp_to_progress(progress, timestamp):
    return progress[progress['Timestamp(ns)'] >= timestamp].iloc[0]['operations-executed']

def progress_to_timestamp(data_dir, progress):
    v = pd.read_table(os.path.join(data_dir, 'progress'), sep='\s+')
    v = v[v['operations-executed'] >= progress]
    if len(v) == 0:
        info = json5.load(open(os.path.join(data_dir, 'info.json')))
        return info['run-end-timestamp(ns)']
    return v.iloc[0]['Timestamp(ns)']

def read_compaction_bytes(data_dir):
    compaction_bytes = []
    compaction_stats = open(os.path.join(data_dir, 'compaction-stats'))
    while True:
        line = compaction_stats.readline()
        if line == '':
            break
        s = line.split(' ')
        assert s[0] == 'Timestamp(ns)'
        timestamp = int(s[1])
        line = compaction_stats.readline()
        assert line == 'Level Read Write\n'
        read = 0
        write = 0
        level = 0
        while True:
            line = compaction_stats.readline()
            if line == ''  or line == '\n':
                break
            s = line.split(' ')
            assert s[0] == 'L' + str(level)
            read += int(s[1])
            write += int(s[2])
            level += 1
        compaction_bytes.append(pd.Series([timestamp, read, write]))
    compaction_bytes = pd.concat(compaction_bytes, axis=1).T
    compaction_bytes.columns = ['Timestamp(ns)', 'read', 'write']
    return compaction_bytes

def read_compaction_bytes_fd_sd(data_dir, first_level_in_sd):
    compaction_bytes = []
    compaction_stats = open(os.path.join(data_dir, 'compaction-stats'))
    while True:
        line = compaction_stats.readline()
        if line == '':
            break
        s = line.split(' ')
        assert s[0] == 'Timestamp(ns)'
        timestamp = int(s[1])
        line = compaction_stats.readline()
        assert line == 'Level Read Write\n'
        fd_read = 0
        fd_write = 0
        sd_read = 0
        sd_write = 0
        level = 0
        while True:
            line = compaction_stats.readline()
            if line == ''  or line == '\n':
                break
            s = line.split(' ')
            assert s[0] == 'L' + str(level)
            read = int(s[1])
            write = int(s[2])
            if level < first_level_in_sd:
                fd_read += read
                fd_write += write
            else:
                sd_read += read
                sd_write += write
            level += 1
        compaction_bytes.append(pd.Series([timestamp, fd_read, fd_write, sd_read, sd_write]))
    compaction_bytes = pd.concat(compaction_bytes, axis=1).T
    compaction_bytes.columns = ['Timestamp(ns)', 'fd-read', 'fd-write', 'sd-read', 'sd-write']
    return compaction_bytes

def read_rand_read_bytes_fd_sd(data_dir, first_level_in_sd):
    rand_read_bytes = []
    for line in open(os.path.join(data_dir, 'rand-read-bytes')):
        if line == '':
            break
        s = line.split(' ')
        fd = 0
        sd = 0
        timestamp_ns = int(s[0])
        for level, bytes in enumerate(s[1:]):
            bytes = int(bytes)
            if level < first_level_in_sd:
                fd += bytes
            else:
                sd += bytes
        rand_read_bytes.append(pd.Series([timestamp_ns, fd, sd]))
    rand_read_bytes = pd.concat(rand_read_bytes, axis=1).T
    rand_read_bytes.columns = ['Timestamp(ns)', 'fd', 'sd']
    return rand_read_bytes

class VersionData:
    data_dir: str
    _info = None
    _ts_progress = None
    _ts_run_90p = None
    def __init__(self, data_dir):
        self.data_dir = data_dir
    def info(self):
        if self._info is None:
            self._info = json5.load(open(os.path.join(self.data_dir, 'info.json')))
        return self._info
    def _run_phase(self, data):
        return data[(data['Timestamp(ns)'] >= self.info()['run-start-timestamp(ns)']) & (data['Timestamp(ns)'] < self.info()['run-end-timestamp(ns)'])]
    def ts_progress(self):
        if self._ts_progress is None:
            self._ts_progress = pd.read_table(self.data_dir + '/progress', sep='\s+')
            self._ts_progress = self._run_phase(self._ts_progress)
            self._ts_progress['operations-executed'] -= self._ts_progress.iloc[0]['operations-executed']
        return self._ts_progress
    def progress_90p(self):
        return self.ts_progress().iloc[-1]['operations-executed'] // 10 * 9
    def ts_run_90p(self):
        if self._ts_run_90p is None:
            i = self.ts_progress()['operations-executed'].searchsorted(self.progress_90p(), side='left')
            self._ts_run_90p = self.ts_progress().iloc[i]['Timestamp(ns)']
        return self._ts_run_90p

def last_10p_ops(version_data: VersionData):
    progress = version_data.ts_progress()
    last = progress.iloc[-1]
    seconds = (last['Timestamp(ns)'] - version_data.ts_run_90p()) / 1e9
    executed = last['operations-executed'] - version_data.progress_90p()
    return executed / seconds

class Estimater:
    _it = None
    _x0 = None
    _x1 = None
    _field: str
    def __init__(self, df, field):
        self._it = df.iterrows()
        self._x0 = next(self._it)[1]
        self._x1 = next(self._it)[1]
        self._field = field
    # Raise StopIteration if none
    def __estimate(self, timestamp):
        return self._x0[self._field] + (self._x1[self._field] - self._x0[self._field]) / (self._x1['Timestamp(ns)'] - self._x0['Timestamp(ns)']) * (timestamp - self._x0['Timestamp(ns)'])
    def estimate(self, timestamp):
        while self._x1['Timestamp(ns)'] <= timestamp:
            self._x0 = self._x1
            self._x1 = next(self._it)[1]
        return self.__estimate(timestamp)

def estimate(version_data: VersionData, data, field: str):
    estimater = Estimater(data, field)
    operations_executed = []
    estimated = []
    for _, row in version_data.ts_progress().iterrows():
        timestamp = row['Timestamp(ns)']
        try:
            estimated.append(estimater.estimate(timestamp))
        except StopIteration:
            break
        operations_executed.append(row['operations-executed'])
    assert len(estimated) == len(operations_executed)
    return (operations_executed, estimated)
