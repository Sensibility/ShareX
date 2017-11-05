from flask import Flask, send_from_directory, render_template, jsonify
from os.path import dirname, realpath, join

from app.Converters.regex import RegexConverter
from app.Modules import module_bp
from app.Modules.Images import image_bp

cwd = dirname(realpath(__file__))

flaskApp = Flask(__name__, template_folder=join("app", "templates"), static_folder="static")
flaskApp.url_map.converters['regex'] = RegexConverter
flaskApp.register_blueprint(module_bp)
flaskApp.register_blueprint(image_bp)


@flaskApp.route('/assets/<regex("[A-Za-z0-9]+\.css"):file>')
def css(file):
    return send_from_directory("app/assets/", file)


@flaskApp.route("/debug")
def debug():
    links = []
    for rule in flaskApp.url_map.iter_rules():
        print(rule)
        links.append((rule, rule))

    return render_template("all_links.html", links=links)


if __name__ == "__main__":
    flaskApp.run(use_reloader=True)
