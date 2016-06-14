import os 
import os.path as osp
import numpy as np
from scipy.io import loadmat

def post_process_image(mat_file_path):
    p = loadmat(mat_file_path)['data'][:, :, :, 0]
    p = p.transpose(1, 0, 2)
    p -= np.min(p, axis=2, keepdims=True)
    p /= np.sum(p, axis=2, keepdims=True)
    layout = np.argmax(p, axis=2)
    return layout
