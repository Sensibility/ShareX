from flask import Flask, request, url_for, abort, send_from_directory, render_template
from werkzeug.utils import secure_filename
from app.Modules.module_loader import ModuleLoader

flaskApp = Flask(__name__)

Modules = ModuleLoader()

@flaskApp.route("/")
def main():
    return "Yo"

@flaskApp.route("/upload/image", methods=['POST'])
def upload():
    password = request.values.get('password')
    imageModule = Modules.GetImage()

    if(imageModule.CheckPassword(password)):
        file = request.files.get('upload')
        if(file == None):
            abort(400)
        try:
            result = imageModule.UploadImage(file, secure_filename)
            if not result:
                abort(400, "Invalid File Type")
            return url_for('.show', name=result)
        except Exception as e:
            flaskApp.log_exception(e)
            abort(500)
    else:
        abort(403)

@flaskApp.route('/public/images/<name>')
def view(name):
    return Modules.GetImage().Resources(name, send_from_directory)

@flaskApp.route('/image')
def image():
    flaskApp.template_folder = Modules.GetImage().GetTemplateFolder()
    return Modules.GetImage().List(render_template)
cd
@flaskApp.route('/image/favicon')
def favicon():
    return send_from_directory(Modules.root, "favicon.ico")

@flaskApp.route('/public/sp_logo')
def logo():
    return send_from_directory(Modules.root, "public/sp_logo.svg")

@flaskApp.route('/image/<name>')
def show(name):
    flaskApp.template_folder = Modules.GetImage().GetTemplateFolder()

    return Modules.GetImage().Index(name, render_template)


