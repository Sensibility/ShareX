from os.path import join

from flask import Blueprint, url_for, request, abort, render_template
from werkzeug.utils import secure_filename

from app.Modules.Images.image_module import ImageModule

image_bp = Blueprint("/image", __name__)

flaskApp = None
image = None

def init(app):
    global flaskApp, image
    flaskApp = app
    image = ImageModule(flaskApp.config['CWD'])

@image_bp.route("/upload", methods=['POST'])
def upload():
    password = request.values.get("password")

    if image.authenticate(password):
        file = request.files.get("upload")
        if file is None:
            abort(400)

        url = image.upload(file, secure_filename)
        if url is None:
            abort(400)
        return url_for('/image.view', name=url)

    else:
        abort(403)

@image_bp.route('/<regex("[A-Za-z0-9]+\.[a-z]+"):name>')
def view(name):
    return render_template(image.index(name), image=join('image', name))

@image_bp.route('/image/<regex("[A-Za-z0-9]+\.[a-z]+"):name>')
def index(name):
    return image.resources(name)