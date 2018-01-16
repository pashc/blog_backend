import logging

from flask import request
from flask_restplus import Resource

from blog_app.api import api
from blog_app.api.errors.article_not_found_error import ArticleNotFoundException
from blog_app.api.errors.category_not_found_error import CategoryNotFoundException
from blog_app.api.errors.invalid_arguments_for_creation_error import InvalidArgumentsForCreationException
from blog_app.api.parser import pagination_parser
from blog_app.api.serializers import blog_article
from blog_app.api.services import article_service
from blog_app.auth import auth

log = logging.getLogger(__name__)

ns = api.namespace('blog/articles', description='blog articles related operations')


@ns.route('/')
@ns.route('/<int:article_id>')
class ArticleItem(Resource):

    @api.marshal_with(blog_article)
    def get(self, article_id):
        """
        :param article_id: the article to get
        :return: the article for the given id
        """
        return article_service.find(article_id).to_dict(), 200

    @api.expect(blog_article)
    @auth.login_required
    def post(self):
        """
        creates a new blog article
        :return: None, status_code=201
        """
        data = request.json
        article_id = article_service.create(data)

        return article_id, 201

    @api.expect(blog_article)
    @auth.login_required
    def put(self, article_id):
        """
        update a blog article

        use this operation to change the title, the content,
        or the related category of an article

        * send a JSON object with the fields in the request body

        '''
        {
            "title": "New Awesome Title",
            "content": "Some New Awesome Content",
            "category_id" "42"
        }
        '''
        :param article_id: the article to update
        :return: None, status_code=204
        """
        data = request.json
        article_service.update(article_id, data)

        return None, 204

    @auth.login_required
    def delete(self, article_id):
        """
        deletes the article for the given id
        :param article_id: the article to delete
        :return: None, status_code=204
        """
        article_service.delete(article_id)
        return None, 204


@ns.route('/list')
class ArticleCollection(Resource):

    @api.expect(pagination_parser)
    def get(self):
        """
        :return: list of blog articles
        """
        data = pagination_parser.parse_args(request)
        return list(map(lambda a: a.to_dict(), article_service.paginate(data)))


@ns.errorhandler(ArticleNotFoundException)
@ns.errorhandler(CategoryNotFoundException)
@ns.errorhandler(InvalidArgumentsForCreationException)
def handle_not_found(error):
    return error.to_dict(), error.code
