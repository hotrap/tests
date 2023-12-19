#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

hit_rates = common.read_hit_rates('.')
print(hit_rates['hit-rate'].max())
