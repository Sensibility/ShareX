import hashlib
import imghdr
import io
import time
from os.path import isfile, join, splitext

from flask import render_template, send_from_directory

from app.Modules.base_module import Module


class ImageModule(Module):
    fs_root = join("app", "Modules", "Images")
    images = join("app", "resources", "images")
    extensions = ['png', 'jpg', 'jpeg']
    password = '<pw>'

    def allowed_file(self, filename, contents):
        result = '.' in filename and \
                 (filename.rsplit('.', 1)[1].lower() in self.extensions) \
                 or \
                 (imghdr.what(contents) in self.extensions)
        return result

    def upload(self, image, secure_filename):
        contents = io.BytesIO(image.read())

        if self.allowed_file(image.name, contents):
            hashResult = self._hash(image)
            fileName = secure_filename(hashResult) + splitext(image.filename)[1]
            with open(join(self.images, fileName), 'wb') as f:
                f.writelines(contents)
            return fileName

    def resources(self, name):
        return send_from_directory(self.images, name)

    def index(self, name):
        return "image.html"

    def _hash(self, file):
        m = None
        while m is None or isfile(m):
            now = str(time.time()).encode('utf-8')
            file_encoded = str(file.filename).encode('utf-8')
            m = str(hashlib.md5(file_encoded + now).hexdigest())
        return m
