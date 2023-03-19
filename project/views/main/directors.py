from flask_restx import Resource, Namespace

from project.container import director_service

from project.setup.api.models import director
from project.setup.api.parsers import page_parser

api = Namespace('directors')

@api.route('/')
class DirectorsView(Resource):
    @api.expect(page_parser)
    @api.marshal_with(director, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all directors.
        """
        res = director_service.get_all(**page_parser.parse_args())
        return res, 200


@api.route('/<int:director_id>/')
class DirectorView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(director, code=201, description='OK')
    def get(self, director_id: int):
        """
        Get director by id.
        """
        return director_service.get_item(director_id)

