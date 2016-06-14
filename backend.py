#!/usr/bin/env python
import os
import os.path as osp
import sys
import numpy as np
import argparse
import subprocess
import time
from scipy.misc import imsave
from utils import get_dir, prepare_caffe
from post_process import post_process_image
from config import cfg

def parse_args():
    parser = argparse.ArgumentParser(description='Test the deep-layout.')
    parser.add_argument('--gpu', dest='gpu_id',
                        help='GPU device id to use [1]',
                        default=1, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        action='store_true')
    args = parser.parse_args()
    return args

if __name__ == '__main__': # Parse arguments
    args = parse_args()

    # Prepare the data folder
    data_dir =  get_dir(cfg.DATA_DIR)
    task_dir =  get_dir(cfg.TASK_DIR)

    # Define command
    caffe = cfg.CAFFE
    prototxt_example = osp.join(cfg.ROOT_DIR, 'caffe_models',
                                'test.prototxt.example')
    caffemodel = osp.join(cfg.ROOT_DIR, 'caffe_models', 'trained.caffemodel')

    # Run
    while(1):
        tasks = os.listdir(task_dir)
        if len(tasks) > 0:
            start_time = time.time()
            scene_id = tasks[0]
            scene_dir = get_dir(data_dir, scene_id)

            print('Processing {:s}...'.format(scene_id))
            prototxt, fc8_dir, view_ids = \
                prepare_caffe(scene_dir, prototxt_example)
            caffe_cmd = '{:s} test -gpu {:d} ' \
                        '-model {:s} -weights {:s} -iterations {:d}'\
                        .format(caffe, args.gpu_id, prototxt, caffemodel,
                                len(view_ids))

            print('Running Caffe command: {:s}'.format(caffe_cmd))
            subprocess.call(caffe_cmd, shell=True)

            print('Running post-processing...')
            result_dir =  get_dir(scene_dir, 'result')
            for view_id in view_ids:
                mat_filename = '{:s}_blob_0.mat'.format(view_id)
                mat_file_path = osp.join(fc8_dir, mat_filename)
                layout = post_process_image(mat_file_path)
                imsave(osp.join(result_dir, view_id + cfg.EXT), layout)

            cmd = 'rm {:s};'.format(osp.join(task_dir, scene_id))
            print('Running command: {:s}'.format(cmd))
            subprocess.call(cmd, shell=True)

            print('Done in {:.1f} sec'.format(time.time() - start_time))

        time.sleep(cfg.DELAY) 

