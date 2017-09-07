class Module():
    password = ""
    index = ""
    root = ""

    templates = ""
    cwd = ""

    def CheckPassword(self, password):
        return self.password == password

    def GetTemplateFolder(self):
        return self.cwd

    def Index(self, name, render_template):
        return render_template(self.index)