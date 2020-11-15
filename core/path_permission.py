import os
from pathlib import Path

from werkzeug.exceptions import Forbidden

from core.config import ALLOWED_PATH


def permitted_path(value):
    if type(value) != str or not Path(os.path.realpath(value)).is_relative_to(ALLOWED_PATH):
        raise Forbidden
    return value