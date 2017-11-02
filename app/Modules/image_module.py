from .base_module import Module
import os, hashlib, time, imghdr, io
from os.path import isfile, join, splitext
from ..Utilities import make_dir_recursive


class ImageModule(Module):
    name = "Images"

    def __init__(self, pModule, cwd):
        self.password = pModule.get("Password")
        self.root = pModule.get("Root")
        self.index = pModule.get("Index")
        self.templates = pModule.get("Template")
        self.list = pModule.get("List")

        self.extension = pModule.get("Extension")
        self.MaxSize = pModule.get("MaxSize")

        make_dir_recursive(self.root)

        self.cwd = cwd

    def IsAllowedFile(self, filename, contents: io.BytesIO):
        result = '.' in filename and \
                 (filename.rsplit('.', 1)[1].lower() in self.extension) \
                 or \
                 (imghdr.what(contents) in self.extension)
        return result

    def UploadImage(self, image, secure_filename):
        result = False

        contents = io.BytesIO(image.read())

        if self.IsAllowedFile(image.name, contents):
            hashResult = self._hash(image)
            fileName = secure_filename(hashResult) + splitext(image.filename)[1]
            with open(os.path.join(self.cwd, self.root, fileName), 'wb') as f:
                f.writelines(contents)
            result = fileName

        return result

    def GetTemplateFolder(self):
        return self.cwd + self.templates

    def GetImageFolder(self):
        return self.cwd + self.root

    def Resources(self, name, send_from_directory):
        return send_from_directory(self.cwd + self.root, name)

    def Index(self, name, render_template):
        return render_template(self.index, image="/" + self.root + name)

    def List(self, render_template):
        list = []
        for f in [f for f in os.listdir(self.GetImageFolder())]:
            if isfile(join(self.GetImageFolder(), f)) and self.IsAllowedFile(f):
                list.append(f)

        return render_template(self.list, images=list)

    def _hash(self, file):
        m = None
        while m == None or os.path.isfile(m):
            now = str(time.time()).encode('utf-8')
            file_encoded = str(file.filename).encode('utf-8')
            m = str(hashlib.md5(file_encoded + now).hexdigest())
        return m
