from flask_restx import Api

from .file_namespace import ns as file_ns
from .folder_namespace import ns as folder_ns

api = Api(
    title='Seznam API',
    version='1.0',
    doc=False
)

api.add_namespace(folder_ns, path='/folder')
api.add_namespace(file_ns, path='/file')
