import os
from pathlib import Path

from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import Forbidden, UnprocessableEntity, NotFound

from apis.file_namespace import file_model
from core.config import ALLOWED_PATH
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
    parser.add_argument('path', type=str, help='Path to folder')

    @ns.marshal_list_with(folder_model)
    @ns.expect(parser)
    def get(self, **kwargs):
        path = self.parser.parse_args()['path']
        if not Path(path).is_relative_to(ALLOWED_PATH):
            raise Forbidden

        if os.path.isdir(path):
            return Folder(path)
        raise NotFound

    @ns.expect(parser)
    @ns.response(204, 'Folder deleted')
    def delete(self, **kwargs):
        path = self.parser.parse_args()['path']
        if not Path(path).is_relative_to(ALLOWED_PATH):
            raise Forbidden

        try:
            os.rmdir(path)
            return '', 204
        except (FileNotFoundError, OSError, NotADirectoryError):
            raise UnprocessableEntity