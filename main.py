from flask import Flask, request, url_for, abort, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
from app.Converters.regex import RegexConverter
from app.Modules import ModuleFactory
from app.Modules.image_module import ImageModule

flaskApp = Flask(__name__)

Modules = ModuleFactory()
Modules.Register(ImageModule)
Modules.Bootstrap()
flaskApp.url_map.converters['regex'] = RegexConverter


def custom_response(msg, status_code, err=""):
    response = jsonify({'msg': msg, 'err': err})
    response.status_code = status_code
    return response


@flaskApp.route("/upload/image", methods=['POST'])
def upload():
    password = request.values.get('password')
    imageModule = Modules.GetModule(ImageModule)

    if imageModule is None:
        abort(500)

    if imageModule.CheckPassword(password):
        file = request.files.get('upload')
        if file is None:
            abort(400)
        try:
            result = imageModule.UploadImage(file, secure_filename)
            if not result:
                return custom_response("Invalid File Type", 400)
            return url_for('.show', name=result)
        except Exception as e:
            flaskApp.log_exception(e)
            abort(500)
    else:
        abort(403)


@flaskApp.route('/public/images/<regex("[A-Za-z0-9]+\.[a-z]+"):name>')
def view(name):
    image = Modules.GetModule(ImageModule)

    return image.Resources(name, send_from_directory)


# @flaskApp.route('/image')
# def image():
#    flaskApp.template_folder = Modules.GetModule(ImageModule).GetTemplateFolder()
#    return Modules.GetModule(ImageModule).List(render_template)


@flaskApp.route('/favicon')
def favicon():
    return send_from_directory(Modules.root, "public/favicon.ico")


@flaskApp.route('/public/assets/<regex("[A-Za-z0-9]+\.css"):file>')
def css(file):
    return send_from_directory(Modules.root, "public/assets/" + file)


@flaskApp.route('/public/sp_logo')
def logo():
    return send_from_directory(Modules.root, "public/sp_logo.svg")


@flaskApp.route('/image/<regex("[A-Za-z0-9]+\.[a-z]+"):name>')
def show(name):
    image = Modules.GetModule(ImageModule)
    flaskApp.template_folder = image.GetTemplateFolder()

    return image.Index(name, render_template)


if __name__ == "__main__":
    flaskApp.run()
