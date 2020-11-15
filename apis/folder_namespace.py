import os
from pathlib import Path

from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import Forbidden, UnprocessableEntity, NotFound

from apis.file_namespace import file_model
from core.path_permission import ALLOWED_PATH, permissed_path
from core.folder import Folder

ns = Namespace('Folders', description='Folders related operations')

folder_model = ns.model('Folder model', {
    'dir_path': fields.String,
    'files': fields.List(fields.Nested(file_model)),
})

folder_model["sub_folders"] = fields.List(fields.Nested(folder_model))


@ns.route('', methods=['GET', 'DELETE'])
class FolderInfo(Resource):
    parser = ns.parser()
    parser.add_argument('path', type=permissed_path, help='Path to folder')

    @ns.marshal_list_with(folder_model)
    @ns.expect(parser)
    def get(self, **kwargs):
        path = self.parser.parse_args()['path']

        if os.path.isdir(path):
            return Folder(path)
        raise UnprocessableEntity

    @ns.expect(parser)
    @ns.response(204, 'Folder deleted')
    def delete(self, **kwargs):
        path = self.parser.parse_args()['path']

        try:
            os.rmdir(path)
            return '', 204
        except (FileNotFoundError, OSError, NotADirectoryError):
            raise UnprocessableEntity
