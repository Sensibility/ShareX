from .base_module import Module
import os, hashlib, time

class ImageModule(Module):
    def __init__(self, module, cwd):
        self.password = module.get("Password")
        self.root = module.get("Root")
        self.index = module.get("Index")
        self.templates = module.get("Template")
        self.list = module.get("List")

        self.extension = module.get("Extension")
        self.MaxSize = module.get("MaxSize")

        self.cwd = cwd

    def IsAllowedFile(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.extension

    def UploadImage(self, image, secure_filename):
        if(self.IsAllowedFile(image.filename)):
            hashResult = self._hash(image)
            fileName = secure_filename(hashResult) + os.path.splitext(image.filename)[1]
            image.save(self.cwd + self.root + fileName)
            return fileName
        else:
            return False

    def GetTemplateFolder(self):
        return self.cwd + self.templates

    def GetImageFolder(self):
        return self.cwd + self.root

    def Resources(self, name, send_from_directory):
        return send_from_directory(self.cwd + self.root, name)

    def Index(self, name, render_template):
        return render_template(self.index, image="/"+ self.root + name)

    def List(self, render_template):
        list = []
        for f in [f for f in os.listdir(self.GetImageFolder())]:
            if(os.path.isfile(os.path.join(self.GetImageFolder(), f)) and self.IsAllowedFile(f)):
                list.append(f)

        return render_template(self.list, images=list)

    def _hash(self, file):
        m = None
        while m == None or os.path.isfile(m):
            m = str(hashlib.md5(str(file.filename).encode('utf-8') + str(time.time()).encode('utf-8')).hexdigest())
        return m