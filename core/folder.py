import os

from .file import File


class Folder(object):
    def __init__(self, path: str):
        path, sub_folders, files = next(os.walk(path))
        self.dir_path = path
        self.sub_folders = [Folder(os.path.join(path, folder)) for folder in sub_folders]
        self.files = [File(os.path.join(path, file)) for file in files]