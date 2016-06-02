import os
from flask import Flask, request, render_template, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

# Server Configuration
SERVER_HOST        =    '0.0.0.0'
SERVER_PORT        =    5000
DEBUG_MODE         =    True

# UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
DEFAULT_SCENE_PATH = 'static/default-scene.jpg'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
    # check if the post request has the file part
        if 'scene' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['scene']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            scene_url = url_for('send_from_uploads', filename=filename)
        return render_template('main.html', scene_path=scene_url)
    return render_template('main.html', scene_path=DEFAULT_SCENE_PATH)

@app.route('/uploads/<filename>')
def send_from_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/hello/')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])

    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG_MODE)
