from flask import Flask, request, redirect, url_for, abort, send_from_directory, render_template
from werkzeug.utils import secure_filename
import hashlib, time, os
from app.Modules.module_loader import ModuleLoader

app = Flask(__name__)
#app.run(threaded=True)


 #   def __init__(self, input):
Modules = ModuleLoader()

@app.route("/")
def main():
    return "Yo"

@app.route("/upload/image", methods=['POST'])
def upload():
    password = request.values.get('password')
    imageModule = Modules.GetImage()

    if(imageModule.CheckPassword(password)):
        file = request.files.get('upload')
        if(file == None):
            abort(400)
        try:
            result = imageModule.UploadImage(file, secure_filename)
            return redirect(url_for('.show', name=result))
        except Exception as e:
            app.log_exception(e)
            abort(500)
    else:
        abort(403)

@app.route('/public/images/<name>')
def view(name):
    return Modules.GetImage().Resources(name, send_from_directory)

@app.route('/image/<name>')
def show(name):
    app.template_folder = Modules.GetImage().GetTemplateFolder()
    return Modules.GetImage().Index(name, render_template)


