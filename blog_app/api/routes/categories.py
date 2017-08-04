import logging

from flask import request
from flask_restplus import Resource

from blog_app.api import api, service
from blog_app.api.serializers import category, category_with_articles
from blog_app.database.models import Category

log = logging.getLogger(__name__)

ns = api.namespace('blog/categories', description='blog categories related operations')


@ns.route('/')
class CategoryCollection(Resource):
    @api.marshal_list_with(category)
    def get(self):
        """
        :return: list of all blog categories
        """
        return Category.query.all()

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
        service.create_category(data)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'category not found')
class CategoryItem(Resource):
    @api.marshal_with(category_with_articles)
    def get(self, category_id):
        """
        :param category_id: the category to get
        :return: category with a list of articles
        """
        return Category.query.filter(Category.id == category_id).one()

    @api.expect(category)
    @api.response(204, 'category successfully updated')
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
        service.update_category(category_id, data)
        return None, 204

    @api.response(204, 'category sucessfully deleted')
    def delete(self, category_id):
        """
        deletes the category for the given id
        :param category_id: the category to delete
        :return: None, status_code=204
        """
        service.delete_category(category_id)
        return None, 204
