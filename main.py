from flask import Flask, request, redirect, url_for, abort, send_from_directory, render_template
from werkzeug.utils import secure_filename
import hashlib, time

app = Flask(__name__)
#app.run(threaded=True)

import os, json
class Module():
    password = ""
    index = ""
    root = ""

    def CheckPassword(self, password):
        return self.password == password

class ModuleLoader(Module):
    modules = []

    def __init__(self):
        dir = os.getcwd() + "/private/config/"
        try:
            f = open(dir + "conf.json", 'r')
        #For the build agent
        except:
            f = open(dir + "conf.orig.json", 'r')

        config = json.loads(str.join("", f.readlines()))
        mods = config.get('Modules')
        if(mods.get('Images')):
            self.modules.append(ImageModule(mods.get('Images')))

        if(mods.get('Root')):
            self.root = mods.get('Root')

        f.close()

    def __Get(self, Module):
        for mod in self.modules:
            if(type(mod) is Module):
                return mod

    def GetImage(self):
        return self.__Get(ImageModule)

class ImageModule(Module):
    def __init__(self, module):
        self.password = module.get("Password")
        self.root = module.get("Root")
        self.index = module.get("Index")

 #   def __init__(self, input):
a = ModuleLoader()

@app.route("/")
def main():
    return "Yo"

@app.route("/upload/image", methods=['POST'])
def upload():
    password = request.headers.get('password')
    if(a.GetImage().CheckPassword(password)):
        file = request.files['upload']
        hashResult = hash(file)
        #try
        file.save(a.root + a.GetImage().root + secure_filename(hashResult) + os.path.splitext(file.name)[1])

        return redirect(url_for('.show', name=hashResult))
    else:
        abort(403)

@app.route('/public/images/<name>')
def view(name):
    return send_from_directory('./public/images', name)

@app.route('/image/<name>')
def show(name):
    return '<img src="/public/images/' + name + '"></img>'


def hash(file):
    m = None
    while m == None or os.path.isfile(m):
        m = str(hashlib.md5(str(file.name).encode('utf-8') + str(time.time()).encode('utf-8')).hexdigest())
    return m
