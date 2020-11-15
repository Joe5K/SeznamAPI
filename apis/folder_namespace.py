import os

from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import UnprocessableEntity

from apis.file_namespace import file_model
from core.folder import Folder
from core.path_permission import permitted_path

ns = Namespace('Folders', description='Folders related operations')

folder_model = ns.model('Folder model', {
    'dir_path': fields.String,
    'files': fields.List(fields.Nested(file_model)),
})

folder_model["sub_folders"] = fields.List(fields.Nested(folder_model))


@ns.route('', methods=['GET', 'DELETE'])
class FolderInfo(Resource):
    parser = ns.parser()
    parser.add_argument('path', type=permitted_path, help='Path to folder')

    @ns.expect(parser)
    @ns.marshal_list_with(folder_model)
    def get(self, **kwargs):
        args = self.parser.parse_args()
        path = args['path']
        if os.path.isdir(path):
            return Folder(path)
        raise UnprocessableEntity

    @ns.expect(parser)
    @ns.response(204, 'Folder deleted')
    def delete(self, **kwargs):
        args = self.parser.parse_args()
        path = args['path']
        try:
            os.rmdir(path)
            return '', 204
        except (FileNotFoundError, OSError, NotADirectoryError):
            raise UnprocessableEntity
