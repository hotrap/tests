#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

data_dir = '.'
first_level_in_sd = int(open(data_dir + '/first-level-in-sd').read())
print(sum(common.read_rand_read_bytes_fd_sd(data_dir, first_level_in_sd).iloc[-1][1:3]) / 1e9, 'GB')
