from flask import render_template


class Module:
    fs_root = "app"
    password = None

    def __init__(self, cwd):
        self.cwd = cwd

    def authenticate(self, password):
        return self.password == password

    def index(self, name):
        return render_template(self.index)