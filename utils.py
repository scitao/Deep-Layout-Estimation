import os
import os.path as osp
import cv2
from config import cfg

def get_dir(root_dir, name=''):
    """
    Create and return directory.
    """
    this_dir = osp.join(root_dir, name)
    if not osp.exists(this_dir):
        print('Creating the folder {:s}.'.format(this_dir))
        os.mkdir(this_dir)
    return this_dir

def prepare_image(scene_dir):
    """
    Load the uploaded images. Resize them and save to the corresponding
    folders. 
    """
    upload_dir = get_dir(scene_dir, 'upload')
    input_dir = get_dir(scene_dir, 'input')
    view_ids = []
    for filename in os.listdir(upload_dir):
        uploaded_image = cv2.imread(osp.join(upload_dir, filename))
        view_id, _ = osp.splitext(filename)
        # Get the input image for NN
        input_shape = cfg.INPUT_SHAPE
        input_image = cv2.resize(uploaded_image,
                                (input_shape[0], input_shape[1]),
                                interpolation=cv2.INTER_LINEAR)
        input_path = osp.join(input_dir, view_id + cfg.EXT)
        cv2.imwrite(input_path, input_image)
        view_ids.append(view_id)
    return input_dir, view_ids

def prepare_list(scene_dir, view_ids):
    """
    Prepare the list files for 
    """
    input_dir = get_dir(scene_dir, 'input')
    list_dir = get_dir(scene_dir, 'list')
    with open(osp.join(list_dir, 'ids.txt'), 'w') as f:
        for view_id in view_ids:
            f.write(view_id + '\n')
    with open(osp.join(list_dir, 'images.txt'), 'w') as f:
        for view_id in view_ids:
            input_path = osp.join(input_dir,'{:s}{:s}'.format(view_id,cfg.EXT))
            f.write(osp.abspath(input_path) + '\n')
    return list_dir

def prepare_caffe(scene_dir, prototxt_example):
    """
    Generate a prototxt file.
    """

    # Prepare the input images for Caffe.
    input_dir, view_ids = prepare_image(scene_dir)

    # Choose a subset of view ids.
    view_ids_subset = view_ids # TODO: For Kevin to replace.

    # Prepare the list files for caffe.
    list_dir = prepare_list(scene_dir, view_ids_subset)

    prototxt = osp.abspath(osp.join(scene_dir, 'test.prototxt'))
    with open(prototxt_example, 'r') as fin:
        txt = fin.read()
    with open(prototxt, 'w') as fout:
        image_list = osp.abspath(osp.join(list_dir, 'images.txt'))
        fc8_dir = osp.abspath(get_dir(scene_dir, 'fc8'))
        id_list = osp.abspath(osp.join(list_dir, 'ids.txt'))
        fout.write(txt % (image_list, fc8_dir + '/', id_list))
    return prototxt, fc8_dir, view_ids_subset

