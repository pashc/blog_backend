import logging

from flask import request
from flask_restplus import Resource

from blog_app.api import api
from blog_app.api.serializers import user
from blog_app.api.services import user_service

log = logging.getLogger(__name__)

ns = api.namespace('auth/', description='user related operations')


@ns.route('/user/<int:id')
class UserItem(Resource):
    @api.marshal_with(user)
    def get(self, user_id):
        """
        :param user_id: the user to get
        :return: the user for the given id
        """
        return user_service.find(user_id)

    @api.expect(user)
    @api.response(204, 'user successfully updated')
    def put(self, user_id):
        """
        update a user

        use this operation to change the username and password for the given id

        all the fields are mandatory

        * send a JSON object with the fields in the request body

        '''
        {
            "username": "Topsy",
            "password": "Cret"
        }
        '''
        :param user_id: the user to update
        :return: None, status_code=204
        """
        data = request.json
        return user_service.update(user_id, data)

    @api.responce(204, 'user successfully deleted')
    def delete(self, user_id):
        """
        deletes the user for the given id
        :param user_id: the user to delete
        :return: None, status_code=204
        """
        return user_service.delete(user_id)
