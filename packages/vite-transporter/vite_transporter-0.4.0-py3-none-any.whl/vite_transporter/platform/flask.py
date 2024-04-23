import sys
import typing as t
from pathlib import Path

if "flask" in sys.modules:
    from flask import Flask, url_for, send_from_directory
    from markupsafe import Markup
else:
    raise ImportError("Flask is not installed.")

from vite_transporter._html_tags import BodyContent, ScriptTag, LinkTag
from vite_transporter.helpers import Colr
from vite_transporter._headers import http_headers


class ViteTransporter:
    app: t.Optional[Flask]
    vt_root_path: Path

    cors_allowed_hosts: list = None

    def __init__(
            self, app: t.Optional[Flask] = None, cors_allowed_hosts: t.Optional[list] = None
    ) -> None:
        if app is not None:
            self.init_app(app, cors_allowed_hosts)

    def init_app(self, app: Flask, cors_allowed_hosts: t.Optional[list] = None) -> None:
        if app is None:
            raise ImportError("No app was passed in.")
        if not isinstance(app, Flask):
            raise TypeError("The app that was passed in is not an instance of Flask")

        self.app = app

        if cors_allowed_hosts is not None:
            self.cors_allowed_hosts = cors_allowed_hosts

        if "vite_transporter" in self.app.extensions:
            raise ImportError(
                "The app has already been initialized with vite-to-flask."
            )

        self.app.extensions["vite_transporter"] = self
        self.app.config["VTF_APPS"] = {}
        self.vt_root_path = Path(app.root_path) / "vt"

        if not self.vt_root_path.exists():
            print(
                f"{Colr.WARNING}{Colr.BOLD}vt folder not found, a new one was created.{Colr.END}{Colr.END}\n\r"
                f"{Colr.OKCYAN}{self.vt_root_path}{Colr.END}\n\r"
            )
            self.vt_root_path.mkdir()

        for folder in self.vt_root_path.iterdir():
            if folder.is_dir():
                self.app.config["VTF_APPS"].update({folder.name: folder})

        self._load_routes(app)
        self._load_context_processor(app)
        self._load_cors_headers(app, self.cors_allowed_hosts)

    def _load_routes(self, app: Flask) -> None:
        @app.route("/__vt/<vite_app>/<filename>")
        def __vt(vite_app: str, filename: str):
            return send_from_directory(self.vt_root_path / vite_app, filename)

    @staticmethod
    def _load_context_processor(app: Flask) -> None:
        @app.context_processor
        def vt_head_processor():
            def vt_head(vite_app: str) -> t.Any:
                vite_assets = Path(app.root_path) / "vt" / vite_app
                find_vite_js = vite_assets.glob("*.js")
                find_vite_css = vite_assets.glob("*.css")

                tags = []

                for file in find_vite_js:
                    print("found", file)
                    tags.append(
                        ScriptTag(
                            src=url_for("__vt", vite_app=vite_app, filename=file.name),
                            type_="module",
                        )
                    )

                for file in find_vite_css:
                    print("found", file)
                    tags.append(
                        LinkTag(
                            rel="stylesheet",
                            href=url_for("__vt", vite_app=vite_app, filename=file.name),
                        )
                    )

                return Markup("".join([tag.raw() for tag in tags]))

            return dict(vt_head=vt_head)

        @app.context_processor
        def vt_body_processor():
            def vt_body(
                    root_id: str = "root",
                    noscript_message: str = "You need to enable JavaScript to run this app.",
            ) -> t.Any:
                return BodyContent(root_id, noscript_message)()

            return dict(vt_body=vt_body)

    @staticmethod
    def _load_cors_headers(app: Flask, cors_allowed_hosts: t.Optional[list] = None) -> None:
        if cors_allowed_hosts:
            print(
                f"\n\r{Colr.WARNING}{Colr.BOLD}vite-transporter is disabling CORS restrictions for:"
                f"{Colr.END}{Colr.END}\n\r"
                f"{Colr.OKCYAN}{', '.join(cors_allowed_hosts)}{Colr.END}\n\r"
            )

            @app.after_request
            def after_request(response):
                response.headers["Access-Control-Allow-Origin"] = ", ".join(cors_allowed_hosts)
                response.headers["Access-Control-Allow-Headers"] = ", ".join(
                    http_headers
                )
                response.headers["Access-Control-Allow-Methods"] = "*"
                response.headers["Access-Control-Allow-Credentials"] = "true"
                return response
