from flask import render_template


class Module:
    fs_root = "app"
    password = None

    def authenticate(self, password):
        return self.password == password

    def index(self, name):
        return render_template(self.index)