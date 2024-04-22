import os
import sys
import typing as t
from pathlib import Path

from vite_transporter.helpers import Colr

if "quart" in sys.modules:
    from markupsafe import Markup
    from quart import Quart, url_for, send_from_directory
else:
    raise ImportError("Quart is not installed.")

from vite_transporter._html_tags import BodyContent, ScriptTag, LinkTag
from vite_transporter._headers import http_headers


class ViteTransporter:
    app: t.Optional[Quart]
    vt_root_path: Path

    cors_allowed_hosts: list = None

    def __init__(
            self, app: t.Optional[Quart] = None, cors_allowed_hosts: t.Optional[list] = None
    ) -> None:
        if app is not None:
            self.init_app(app, cors_allowed_hosts)

    def init_app(self, app: Quart, cors_allowed_hosts: t.Optional[list] = None) -> None:
        if app is None:
            raise ImportError("No app was passed in.")
        if not isinstance(app, Quart):
            raise TypeError("The app that was passed in is not an instance of Quart")

        self.app = app
        self.cors_allowed_hosts = cors_allowed_hosts

        if "vite_transporter" in self.app.extensions:
            raise ImportError(
                "The app has already been initialized with vite-to-flask."
            )

        self.app.extensions["vite_transporter"] = self
        self.app.config["VTF_APPS"] = {}
        self.vt_root_path = Path(app.root_path) / "vt"

        if not self.vt_root_path.exists():
            raise FileNotFoundError(
                "vt directory not found in the flask app root directory."
            )

        for folder in self.vt_root_path.iterdir():
            if folder.is_dir():
                self.app.config["VTF_APPS"].update({folder.name: folder})

        self._load_routes(app)
        self._load_context_processor(app)
        self._load_cors_headers(app, cors_allowed_hosts=self.cors_allowed_hosts)

    def _load_routes(self, app: Quart) -> None:
        @app.route("/__vt/<vite_app>/<filename>")
        async def __vt(vite_app: str, filename: str):
            return await send_from_directory(self.vt_root_path / vite_app, filename)

    @staticmethod
    def _load_context_processor(app: Quart) -> None:
        @app.context_processor
        async def vt_head_processor():
            def vt_head(vite_app: str) -> t.Any:
                vite_assets = Path(app.root_path) / "vt" / vite_app
                find_vite_js = vite_assets.glob("*.js")
                find_vite_css = vite_assets.glob("*.css")

                tags = []

                for file in find_vite_js:
                    tags.append(
                        ScriptTag(
                            src=url_for(
                                "__vt", vite_app=f"{vite_app}", filename=f"{file.name}"
                            ),
                            type_="module",
                        )
                    )

                for file in find_vite_css:
                    tags.append(
                        LinkTag(
                            rel="stylesheet",
                            href=url_for(
                                "__vt", vite_app=f"{vite_app}", filename=f"{file.name}"
                            ),
                        )
                    )

                return Markup("".join([tag.raw() for tag in tags]))

            return dict(vt_head=vt_head)

        @app.context_processor
        async def vt_body_processor():
            def vt_body(
                    root_id: str = "root",
                    noscript_message: str = "You need to enable JavaScript to run this app.",
            ) -> t.Any:
                return BodyContent(root_id, noscript_message)()

            return dict(vt_body=vt_body)

    @staticmethod
    def _load_cors_headers(app: Quart, cors_allowed_hosts: t.Optional[list] = None) -> None:
        if cors_allowed_hosts:
            print(
                f"\n\r{Colr.WARNING}{Colr.BOLD}vite-transporter is disabling CORS restrictions for:"
                f"{Colr.END}{Colr.END}\n\r"
                f"{Colr.OKCYAN}{", ".join(cors_allowed_hosts)}{Colr.END}\n\r"
            )

            @app.after_request
            async def after_request(response):
                response.headers["Access-Control-Allow-Origin"] = ", ".join(cors_allowed_hosts)
                response.headers["Access-Control-Allow-Headers"] = ", ".join(
                    http_headers
                )
                response.headers["Access-Control-Allow-Methods"] = "*"
                response.headers["Access-Control-Allow-Credentials"] = "true"
                return response
