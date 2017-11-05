from flask import Blueprint, request, abort, url_for, render_template
from werkzeug.utils import secure_filename
from os.path import dirname, realpath, join
from app.Modules.Images.image_module import ImageModule

cwd = dirname(realpath(__file__))
image_bp = Blueprint("/image", __name__)

image = ImageModule()


@image_bp.route("/upload", methods=['POST'])
def upload():
    password = request.values.get("password")

    if image.authenticate(password):
        file = request.files.get("upload")
        if file is None:
            abort(400)

        try:
            url = image.upload(file, secure_filename)
            if url is None:
                abort(400)
            return url_for('/image.view', name=url)
        except Exception as e:
            print(e)

            abort(500)
    else:
        abort(403)


@image_bp.route('/<regex("[A-Za-z0-9]+\.[a-z]+"):name>')
def view(name):
    return render_template(image.index(name), image=join('image', name))


@image_bp.route('/image/<regex("[A-Za-z0-9]+\.[a-z]+"):name>')
def index(name):
    return image.resources(name)
