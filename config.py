import os
import os.path as osp
import sys
import numpy as np
# `pip install easydict` if you don't have it
from easydict import EasyDict as edict

__C = edict()
cfg = __C

#
# Misc
#

# Root directory
__C.ROOT_DIR = osp.dirname(__file__)

# Shared data folder
__C.DATA_DIR = 'data'

# Task queue
__C.TASK_DIR = osp.join(cfg.DATA_DIR, 'tasks')

# Time to wait
__C.DELAY = 0.1

__C.EXT = '.jpg' 

#
# Frontend Configuration
#

__C.SERVER_HOST = '0.0.0.0'

__C.SERVER_PORT = 5000

__C.DEBUG_MODE = True

__C.ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']) 

#
# Backend Configuration
#

# Choose command line caffe
__C.CAFFE = osp.join('deeplab-public', 'build/tools/caffe')

__C.MAX_SHAPE = (1920, 1080)

__C.INPUT_SHAPE = (321, 321)


