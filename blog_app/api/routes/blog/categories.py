import logging

from flask import request
from flask_restplus import Resource

from blog_app.api import api
from blog_app.api.serializers import category, category_with_articles
from blog_app.api.services import category_service
from blog_app.auth import auth

log = logging.getLogger(__name__)

ns = api.namespace('blog/categories', description='blog categories related operations')


@ns.route('/')
class CategoryCollection(Resource):

    @api.marshal_list_with(category)
    def get(self):
        """
        :return: list of all blog categories
        """
        all_categories = category_service.find_all()
        return list(map(lambda c: c.to_dict(), all_categories)), 200

    @api.expect(category)
    @api.response(201, 'category successfully created')
    def post(self):
        """
        creates a new blog category

        * send a JSON object with name and an optional id
        '''
        {
            "id": "42",
            "name": "Ultimate Category Name"
        }
        '''

        :return: None, status_code=201
        """
        data = request.json
        return category_service.create(data).to_dict(), 201

    @ns.route('/<int:category_id>')
    class CategoryItem(Resource):

        @api.marshal_with(category_with_articles)
        def get(self, category_id):
            """
            :param category_id: the category to get
            :return: category with a list of articles
            """
            return category_service.find(category_id).to_dict(), 200

        @api.expect(category)
        @auth.login_required
        def put(self, category_id):
            """
            updates a blog category

            use this operation to change the name of a blog category

            * send a JSON object with the new name in the request body

            '''
            {
                "name": "New Category Name"
            }
            '''
            * specify the ID of the category to modify in the request URL path

            :param category_id: the category to update
            :return: None, status_code=201
            """
            data = request.json
            return category_service.update(category_id, data).to_dict(), 200

        @auth.login_required
        def delete(self, category_id):
            """
            deletes the category for the given id
            :param category_id: the category to delete
            :return: None, status_code=204
            """
            category_service.delete(category_id)
            return None, 204
