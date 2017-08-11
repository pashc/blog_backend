import logging

from flask import request
from flask_restplus import Resource

from blog_app.api import api, service
from blog_app.api.parser import pagination_parser
from blog_app.api.serializers import page_of_articles, blog_article
from blog_app.database.models.articles import Articles

log = logging.getLogger(__name__)

ns = api.namespace('blog/articles', description='blog articles related operations')


@ns.route('/')
class ArticleCollection(Resource):
    @api.expect(pagination_parser)
    @api.marshal_with(page_of_articles)
    def get(self):
        """
        :return: list of blog articles
        """
        data = pagination_parser.parse_args(request)
        page = data.get('page', 1)
        per_page = data.get('per_page', 10)

        return Articles.query.paginate(page, per_page, error_out=False)

    @api.expect(blog_article)
    def post(self):
        """
        creates a new blog article
        :return: None, status_code=201
        """
        data = request.json
        service.create_article(data)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'article not found')
class ArticleItem(Resource):
    @api.marshal_with(blog_article)
    def get(self, article_id):
        """
        :param article_id: the article to get
        :return: the article for the given id
        """
        return Articles.query.filter(Articles.id == article_id).one()

    @api.expect(blog_article)
    @api.response(204, 'article successfully updated')
    def put(self, article_id):
        """
        update a blog article

        use this operation to change the title, the content,
        or the related category of an article for the given id

        all the fields are mandatory

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
        service.update_article(article_id, data)
        return None, 204

    @api.response(204, 'article successfully deleted')
    def delete(self, article_id):
        """
        deletes the article for the given id
        :param article_id: the article to delte
        :return: None, status_code=204
        """
        service.delete_article(article_id)
        return None, 204


@ns.route('/archive/<int:year>/')
@ns.route('/archive/<int:year>/<int:month>/')
@ns.route('/archive/<int:year>/<int:month>/<int:day>/')
class ArticleArchiveCollection(Resource):
    @api.expect(pagination_parser, validate=True)
    @api.marshal_with(page_of_articles)
    def get(self, year, month=None, day=None):
        """
        returns list of articles for the given time period
        :param year: the year, mandatory
        :param month: the month, optional
        :param day: the day, optional
        :return: articles for the given tie period
        """
        data = pagination_parser.parse_args(request)
        page = data.get('page', 1)
        per_page = data.get('per_page', 10)

        start_day = day if day else 1
        end_day = day + 1 if day else 31

        start_month = month if month else 1
        end_month = month + 1 if month else 12
        start_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, start_month, start_day)
        end_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, end_month, end_day)
        return Articles.query.filter(
            Articles.pub_date >= start_date).filter(
            Articles.pub_date <= end_date).paginate(
            page, per_page, error_out=False)
