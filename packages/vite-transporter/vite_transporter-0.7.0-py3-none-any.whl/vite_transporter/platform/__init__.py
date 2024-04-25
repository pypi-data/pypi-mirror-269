import sys

if "flask" in sys.modules:
    from .flask import ViteTransporter as FlaskViteTransporter
else:
    from .not_installed import FlaskNotInstalled as FlaskViteTransporter

if "quart" in sys.modules:
    from .quart import ViteTransporter as QuartViteTransporter
else:
    from .not_installed import QuartNotInstalled as QuartViteTransporter

__all__ = ["FlaskViteTransporter", "QuartViteTransporter"]
