import sys

from .utilities import ArgumentParser as _ArgumentParser
from .utilities import Colr as _Colr
from .utilities import PyProjectConfig as _PyProjectConfig
from .utilities import compiler

__version__ = "0.5.0"


def setup_subparsers(pars):
    subparsers = pars.add_subparsers()

    subparsers.add_parser("compile").set_defaults(compile=False).add_argument(
        "-y", action="store_true"
    )
    subparsers.add_parser("list").set_defaults(list=False)
    subparsers.add_parser("ls").set_defaults(list=False)


def load_vite_apps(pyproject):
    for vite_app in pyproject.vite_apps:
        pyproject.vite_apps.append(
            {
                "vite_app": vite_app,
                "serve_app": pyproject.vt_config.get("serve_app"),
            }
        )


def list_ls(pars):
    print("")
    if not pars.vite_apps:
        print(f" {_Colr.WARNING}No vite apps found in pyproject.toml{_Colr.END}")
    else:
        for app in pars.vite_apps:
            print(
                f"{_Colr.OKGREEN}{app.get('vite_app')}/dist/assets{_Colr.END} "
                f"{_Colr.BOLD}=>{_Colr.END} "
                f"{_Colr.OKGREEN}{app.get('serve_app')}/vt/{app.get('vite_app')}/{_Colr.END}"
            )
    print("")
    sys.exit(0)


def compile_(pyproject, pars, args):
    compiler(
        pyproject,
        pars.vite_apps,
        replace=True if hasattr(args, "y") and args.y else False,
    )
    sys.exit(0)


def cli_entry():
    pars = _ArgumentParser(prog="vtf", add_help=False)
    pars.add_argument(
        "--version", "-v", action="version", version=f"vite-to-flask {__version__}"
    )
    pars.add_argument("--help", "-h", action="help")

    setup_subparsers(pars)

    with _PyProjectConfig() as pyproject:
        pypro: _PyProjectConfig = pyproject

        load_vite_apps(pypro)

        args = pars.parse_args()

        if hasattr(args, "compile"):
            compile_(pypro, pars, args)

        if hasattr(args, "list") or hasattr(args, "ls"):
            list_ls(pars)

    # print help if no command is given
    pars.print_help()
