#!/usr/bin/env python
import os
import os.path as osp
import time
import uuid
import cv2
from utils import get_dir
from flask import Flask, request, render_template, redirect, url_for, flash
from flask import send_from_directory
from config import cfg

app = Flask(__name__)
DATA_DIR = get_dir(cfg.DATA_DIR)
TASK_DIR = get_dir(cfg.TASK_DIR)

def allowed_file(filename):
    """Check allowed file extesions."""
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in cfg.ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # Get the name of the uploaded images
        uploaded_files = request.files.getlist('image[]')
        scene_id = str(uuid.uuid4())
        scene_dir = get_dir(DATA_DIR, scene_id)
        upload_dir = get_dir(scene_dir, 'upload')
        result_dir = get_dir(scene_dir, 'result')
        for fi, file in enumerate(uploaded_files):
            # Save the file
            if file and allowed_file(file.filename):
                _, file_extension = osp.splitext(file.filename)
                view_id = str(fi)
                file.save(osp.join(upload_dir, view_id + cfg.EXT))

        # Schedule a task to backend
        task = osp.join(TASK_DIR, scene_id)
        open(task, 'wb').write('')
        while osp.exists(task):
            time.sleep(cfg.DELAY) 

        filenames = os.listdir(result_dir)
        return render_template('result.html', scene_id=scene_id,
                                filenames=filenames)

    return render_template('main.html')

@app.route('/<scene_id>/upload/<filename>')
def upload_image(scene_id, filename):
    return send_from_directory(osp.join(DATA_DIR, scene_id, 'upload'), filename)

@app.route('/<scene_id>/result/<filename>')
def result_image(scene_id, filename):
    return send_from_directory(osp.join(DATA_DIR, scene_id, 'result'), filename)

if __name__ == "__main__":
    app.run(host=cfg.SERVER_HOST, port=cfg.SERVER_PORT, debug=cfg.DEBUG_MODE)
