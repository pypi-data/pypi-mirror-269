from dotenv import load_dotenv
from flask import Flask, render_template, session

from vite_transporter.platform.flask import ViteTransporter

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = "flask_secret"
    ViteTransporter(app, cors_allowed_hosts=["http://127.0.0.1:5003"])

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api")
    def api():
        return {"message": "Hello, World!"}

    @app.route("/api/session")
    def session_():
        session["message"] = "Hello, World!"
        return {"session_message": session["message"]}

    return app


def run():
    # used for pyqwe
    _app = create_app()
    _app.run(port=5001, debug=True)
