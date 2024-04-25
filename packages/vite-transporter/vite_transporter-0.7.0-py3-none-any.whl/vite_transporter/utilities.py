import argparse
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from tomllib import loads
from typing import Optional

from markupsafe import Markup

http_headers = (
    "Accept",
    "Accept-Language",
    "Authorization",
    "Content-Language",
    "Content-Type",
    "DPR",
    "Downlink",
    "Origin",
    "Save-Data",
    "Viewport-Width",
    "Width",
    "X-AUTH-TOKEN",
    "X-CSRF-TOKEN",
    "X-REQUESTED-WITH",
    "X-Auth-Token",
    "X-Csrf-Token",
    "X-Requested-With",
    "x-Auth-Token",
    "x-Csrf-Token",
    "x-Requested-With",
    "x-auth-token",
    "x-csrf-token",
    "x-requested-with",
)


class Colr:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class PyProjectConfig:
    cwd: Path
    pyproject: Path
    vt_config: dict

    npm_exec: str
    npx_exec: str
    serve_app: str
    vite_apps: list

    def __init__(self):
        self.cwd = Path.cwd()
        self.pyproject = self.cwd / "pyproject.toml"
        self.load_pyproject()

    def load_pyproject(self):
        if not self.pyproject.exists():
            raise FileNotFoundError("pyproject.toml not found.")

        pyproject_raw = loads(str(self.pyproject.read_text()))
        self.vt_config = pyproject_raw.get("tool", {}).get("vite_transporter", {})
        self.npm_exec = self.vt_config.get("npm_exec", "npm")
        self.npx_exec = self.vt_config.get("npx_exec", "npx")
        self.serve_app = self.vt_config.get("serve_app", "app")
        self.vite_apps = self.vt_config.get("vite_apps", [])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None


class NPXCommander:
    def __init__(self, workdir: Path, npx_binary: str = "npx"):
        self.npx_binary = npx_binary
        self.workdir = workdir

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def run(self, command: str):
        subprocess.run([self.npx_binary, *shlex.split(command)], cwd=self.workdir)


class NPMCommander:
    def __init__(self, workdir: Path, npm_binary: str = "npm"):
        self.npm_binary = npm_binary
        self.workdir = workdir

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def run(self, command: str):
        subprocess.run([self.npm_binary, *shlex.split(command)], cwd=self.workdir)


def compiler(pyproject_config: PyProjectConfig, vite_apps_found: list[dict], replace: bool = False):

    print("Compiling Vite apps...")
    vt_dir = pyproject_config.cwd / pyproject_config.serve_app / "vt"

    # Delete contents of vt_dir
    if vt_dir.exists():
        if not replace:
            prompt = input(
                f"Continuing will replace the contents of \n\r"
                f"{vt_dir} \n\r"
                f"Do you want to continue? (Y/n): "
            )
        else:
            prompt = "y"

        if prompt.lower() == "y" or prompt == "":
            for item in vt_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

        else:
            print("Operation aborted.")
            sys.exit(0)

    else:
        vt_dir.mkdir()

    # Create directories for vite apps
    for app in vite_apps_found:
        va_path = pyproject_config.cwd / app.get("vite_app")
        va_node_modules = va_path / "node_modules"
        va_dist = va_path / "dist"
        va_assets = va_dist / "assets"

        va_vt_path = vt_dir / app.get("vite_app")

        if not va_vt_path.exists():
            va_vt_path.mkdir()

        if not va_node_modules.exists():
            with NPMCommander(va_path, pyproject_config.npm_exec) as npm:
                npm.run("install")

        with NPXCommander(va_path, pyproject_config.npx_exec) as npx:
            npx.run("vite build --mode production")

        for item in va_assets.iterdir():
            print(f"{Colr.OKGREEN}Copying {item.name} to {va_vt_path}{Colr.END}")

            if item.suffix == ".js":
                with open(va_vt_path / item.name, "w") as f:
                    content = item.read_text()
                    f.write(content.replace("assets/", f"__vt/{app.get('vite_app')}/"))
            else:
                shutil.copy(item, va_vt_path / item.name)

        shutil.rmtree(va_dist)

    print("Compilation complete.")


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)
        self.vite_apps: list[dict] = []

    def print_help(self, file=None):
        print(
            "\n\r"
            "Usage: vtf <option>"
            "\n\r\n\r"
            f" {Colr.OKCYAN}list, ls{Colr.END} => List all vite apps in pyproject.toml"
            "\n\r"
            f" {Colr.OKCYAN}compile (-y){Colr.END} => Attempt to compile all vite apps"
            "\n\r"
            f"  | {Colr.OKCYAN}-y{Colr.END} => Accept all prompts while compiling"
            "\n\r"
            f" {Colr.OKCYAN}-h, --help{Colr.END} => Show the help message and exit"
            "\n\r"
            f" {Colr.OKCYAN}-v, --version{Colr.END} => Show the version and exit"
        )
        print("")


class LinkTag:
    rel: str = None
    href: str = None
    sizes: str = None
    type: str = None
    hreflang: str = None

    _rel: str = None
    _href: str = None
    _sizes: str = None
    _type: str = None
    _hreflang: str = None

    def __init__(
        self,
        rel: str,
        href: Optional[str] = None,
        sizes: Optional[str] = None,
        type_: Optional[str] = None,
        hreflang: Optional[str] = None,
    ):
        self.rel = rel
        self.href = href
        self.sizes = sizes
        self.type = type_
        self.hreflang = hreflang

        self._rel = f'rel="{self.rel}" '
        self._href = f'href="{self.href}" ' if self.href is not None else ""
        self._sizes = f'sizes="{self.sizes}" ' if self.sizes is not None else ""
        self._type = f'type="{self.type}" ' if self.type is not None else ""
        self._hreflang = (
            f'hreflang="{self.hreflang}" ' if self.hreflang is not None else ""
        )

    def __repr__(self):
        return Markup(
            f"<LinkTag {self._rel}{self._href}{self._sizes}{self._type}{self._hreflang}>".replace(
                " >", ">"
            )
        )

    def __str__(self):
        return Markup(self._compile())

    def __call__(self, *args, **kwargs):
        return Markup(self._compile())

    def raw(self):
        return self._compile()

    def _compile(self):
        return f"<link {self._rel}{self._href}{self._sizes}{self._type}{self._hreflang}>".replace(
            " >", ">"
        )


class ScriptTag:
    src: str = None
    type: str = None
    async_: bool = False
    defer: bool = False
    crossorigin: str = None
    integrity: str = None
    nomodule: bool = False
    referrerpolicy: str = None

    _src: str = None
    _type: str = None
    _async: str = None
    _defer: str = None
    _crossorigin: str = None
    _integrity: str = None
    _nomodule: str = None
    _referrerpolicy: str = None

    def __init__(
        self,
        src: str,
        type_: Optional[str] = None,
        async_: bool = False,
        defer: bool = False,
        crossorigin: Optional[str] = None,
        integrity: Optional[str] = None,
        nomodule: bool = False,
        referrerpolicy: Optional[str] = None,
    ):
        self.src = src
        self.type = type_
        self.async_ = async_
        self.defer = defer
        self.crossorigin = crossorigin
        self.integrity = integrity
        self.nomodule = nomodule
        self.referrerpolicy = referrerpolicy

        self._src = f'src="{self.src}" '
        self._type = f'type="{self.type}" ' if self.type is not None else ""
        self._async = f'async="{str(self.async_).lower()}" ' if self.async_ else ""
        self._defer = "defer " if self.defer else ""
        self._crossorigin = (
            f'crossorigin="{self.crossorigin}" ' if self.crossorigin is not None else ""
        )
        self._integrity = (
            f'integrity="{self.integrity}" ' if self.integrity is not None else ""
        )
        self._nomodule = "nomodule " if self.nomodule else ""
        self._referrerpolicy = (
            f'referrerpolicy="{self.referrerpolicy}" '
            if self.referrerpolicy is not None
            else ""
        )

    def __repr__(self):
        return Markup(
            (
                f"<ScriptTag {self._src}{self._type}"
                f"{self._async}{self._defer}{self._crossorigin}"
                f"{self._integrity}{self._nomodule}{self._referrerpolicy}>"
            ).replace(" >", ">")
        )

    def __str__(self):
        return Markup(self._compile())

    def __call__(self, *args, **kwargs):
        return Markup(self._compile())

    def raw(self):
        return self._compile()

    def _compile(self):
        return (
            f"<script {self._src}{self._type}"
            f"{self._async}{self._defer}{self._crossorigin}"
            f"{self._integrity}{self._nomodule}{self._referrerpolicy}></script>"
        ).replace(" >", ">")


class BodyContent:
    div_id: str = None
    noscript_message: str = None

    def __init__(
        self,
        div_id: str = "root",
        noscript_message: str = "You need to enable JavaScript to run this app.",
    ):
        self.div_id = div_id
        self.noscript_message = noscript_message

    def __repr__(self):
        return (
            "BodyContent< "
            f"id = {self.div_id} "
            f"noscript = {self.noscript_message} "
            ">"
        )

    def __str__(self):
        return Markup(self._compile())

    def __call__(self, *args, **kwargs):
        return Markup(self._compile())

    def _compile(self):
        return Markup(
            f'<div id="{self.div_id}"></div>\n'
            f"<noscript>{self.noscript_message}</noscript>"
        )
