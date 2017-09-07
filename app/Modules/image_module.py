from .base_module import Module
import os, hashlib, time

class ImageModule(Module):
    def __init__(self, module, cwd):
        self.password = module.get("Password")
        self.root = module.get("Root")
        self.index = module.get("Index")
        self.templates = module.get("Template")

        self.cwd = cwd

    def UploadImage(self, image, secure_filename):
        hashResult = self._hash(image)
        image.save(self.cwd + self.root + secure_filename(hashResult) + os.path.splitext(image.filename)[1])

    def GetTemplateFolder(self):
        return self.cwd + self.templates

    def Resources(self, name, send_from_directory):
        return send_from_directory(self.cwd + self.root, name)

    def Index(self, name, render_template):
        return render_template(self.index, image="/"+ self.root + name)

    def _hash(self, file):
        m = None
        while m == None or os.path.isfile(m):
            m = str(hashlib.md5(str(file.filename).encode('utf-8') + str(time.time()).encode('utf-8')).hexdigest())
        return m