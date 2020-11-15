import os
from pathlib import Path

from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import Forbidden, UnprocessableEntity, NotFound

from core.config import ALLOWED_PATH
from core.file import File

ns = Namespace('Files', description='Files related operations')

file_model = ns.model('File model', {
    'file_name': fields.String,
    'creation_date': fields.DateTime,
    'modification_date': fields.DateTime,
    'size': fields.Integer,
})


@ns.route('', methods=['GET', 'POST', 'DELETE'])
class FileInfo(Resource):
    parser = ns.parser()
    parser.add_argument('path', type=str, help='Path to file')

    @ns.marshal_list_with(file_model)
    @ns.expect(parser)
    def get(self, **kwargs):
        path = self.parser.parse_args()['path']
        if not Path(path).is_relative_to(ALLOWED_PATH):
            raise Forbidden

        if os.path.isfile(path):
            return File(path)
        raise NotFound

    @ns.expect(parser)
    @ns.response(204, 'File deleted')
    def delete(self, **kwargs):
        path = self.parser.parse_args()['path']
        if not Path(path).is_relative_to(ALLOWED_PATH):
            raise Forbidden

        try:
            os.remove(path)
            return '', 204
        except (FileNotFoundError, PermissionError):
            raise UnprocessableEntity

    @ns.expect(parser)
    @ns.response(204, 'File created')
    def post(self, **kwargs):
        path = self.parser.parse_args()['path']
        if not Path(path).is_relative_to(ALLOWED_PATH):
            raise Forbidden

        try:
            open(path, "x")
            return '', 204
        except (FileExistsError, PermissionError):
            raise UnprocessableEntity