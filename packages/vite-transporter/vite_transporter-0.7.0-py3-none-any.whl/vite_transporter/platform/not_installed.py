class FlaskNotInstalled:
    def __init__(*args, **kwargs) -> None:
        raise ImportError("Flask is not installed.")


class QuartNotInstalled:
    def __init__(*args, **kwargs) -> None:
        raise ImportError("Quart is not installed.")
