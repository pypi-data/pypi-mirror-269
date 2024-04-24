import sys

from .utilities import ArgumentParser as _ArgumentParser
from .utilities import Colr as _Colr
from .utilities import PyProjectConfig as _PyProjectConfig
from .utilities import compiler

__version__ = "0.6.0"


def setup_subparsers(parser):
    subparsers = parser.add_subparsers()

    _compile = subparsers.add_parser("compile")
    _compile.set_defaults(compile=False)
    _compile.add_argument("-y", action="store_true")

    _list = subparsers.add_parser("list")
    _list.set_defaults(list=False)
    _ls = subparsers.add_parser("ls")
    _ls.set_defaults(ls=False)


def load_vite_apps(pyproject_config):
    vite_apps = []
    for vite_app in pyproject_config.vite_apps:
        vite_apps.append(
            {
                "vite_app": vite_app,
                "serve_app": pyproject_config.vt_config.get("serve_app"),
            }
        )
    return vite_apps


def list_ls(vite_apps_found):
    print("")
    if not vite_apps_found:
        print(f" {_Colr.WARNING}No vite apps found in pyproject.toml{_Colr.END}")
    else:
        for app in vite_apps_found:
            print(
                f"{_Colr.OKGREEN}{app.get('vite_app')}/dist/assets{_Colr.END} "
                f"{_Colr.BOLD}=>{_Colr.END} "
                f"{_Colr.OKGREEN}{app.get('serve_app')}/vt/{app.get('vite_app')}/{_Colr.END}"
            )
    print("")
    sys.exit(0)


def compile_(pyproject_config, vite_apps_found, parsed_args):
    compiler(
        pyproject_config,
        vite_apps_found,
        replace=True if hasattr(parsed_args, "y") and parsed_args.y else False,
    )
    sys.exit(0)


def cli_entry():
    parser = _ArgumentParser(prog="vtf", add_help=False)
    parser.add_argument(
        "--version", "-v", action="version", version=f"vite-to-flask {__version__}"
    )
    parser.add_argument("--help", "-h", action="help")

    setup_subparsers(parser)

    with _PyProjectConfig() as pyproject_config:
        vite_apps_found = load_vite_apps(pyproject_config)
        parsed_args = parser.parse_args()

        if hasattr(parsed_args, "compile"):
            compile_(pyproject_config, vite_apps_found, parsed_args)

        if hasattr(parsed_args, "list") or hasattr(parsed_args, "ls"):
            list_ls(vite_apps_found)

    # print help if no command is given
    parser.print_help()
