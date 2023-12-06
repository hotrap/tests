#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), 'common/'))
from hotspot_io import *

dir=sys.argv[1]
draw_hotspot_io(dir, '110GB', 'hotspot-io.pdf')
