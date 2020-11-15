import os
import platform
from datetime import datetime


class File(object):
    def __init__(self, path: str):
        self.path = path

    @property
    def file_name(self) -> str:
        return os.path.basename(self.path)

    @property
    def creation_date(self) -> datetime:
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        """
        if platform.system() == 'Windows':
            date = os.path.getctime(self.path)
        else:
            stat = os.stat(self.path)
            try:
                date = stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                date = stat.st_mtime
        return datetime.fromtimestamp(date)

    @property
    def modification_date(self) -> datetime:
        return datetime.fromtimestamp(os.path.getmtime(self.path))

    @property
    def size(self) -> int:
        return os.stat(self.path).st_size
