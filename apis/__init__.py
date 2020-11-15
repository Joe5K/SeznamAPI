from flask_restx import Api

from .file_namespace import ns as file_api
from .folder_namespace import ns as folder_api

api = Api(
    title='Seznam API',
    version='1.0'
)

api.add_namespace(folder_api, path='/folder')
api.add_namespace(file_api, path='/file')
