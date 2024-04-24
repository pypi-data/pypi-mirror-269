from dotenv import load_dotenv
from quart import Quart, render_template, session

from vite_transporter.platform.quart import ViteTransporter

load_dotenv()


def create_app():
    app = Quart(__name__)
    app.secret_key = "quart_secret"
    ViteTransporter(app, cors_allowed_hosts=["http://127.0.0.1:5003"])

    @app.route("/")
    async def index():
        return await render_template("index.html")

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
    _app.run(port=5000, debug=True)
