import os

from werkzeug.exceptions import Forbidden

from core.config import ALLOWED_PATH


def permitted_path(value):
    normalized_path = os.path.realpath(value)
    if type(value) != str or os.path.commonprefix((normalized_path, ALLOWED_PATH)) != ALLOWED_PATH:
        raise Forbidden
    return normalized_path
