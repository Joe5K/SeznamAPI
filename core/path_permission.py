from pathlib import Path

from werkzeug.exceptions import Forbidden

from core.config import ALLOWED_PATH


def permissed_path(value):
    if type(value) != str or not Path(value).is_relative_to(ALLOWED_PATH):
        raise Forbidden
    return value