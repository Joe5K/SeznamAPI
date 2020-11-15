import os

from werkzeug.exceptions import Forbidden

from core.config import ALLOWED_PATH


def permitted_path(value):
    if type(value) == str:
        normalized_path = os.path.realpath(value)
        if os.path.commonprefix((normalized_path, ALLOWED_PATH)) == ALLOWED_PATH:
            return normalized_path
    raise Forbidden
