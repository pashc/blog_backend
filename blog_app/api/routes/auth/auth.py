import logging

from flask import request, g
from flask.json import jsonify
from flask_restplus import Resource

from blog_app.api import api
from blog_app.api.serializers import user
from blog_app.api.services import user_service
from blog_app.app import auth
from blog_app.database.models.auth.users import Users

log = logging.getLogger(__name__)

ns = api.namespace('auth', description='user related operations')


@ns.route('/users/<int:id')
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

    @api.response(204, 'user successfully deleted')
    def delete(self, user_id):
        """
        deletes the user for the given id
        :param user_id: the user to delete
        :return: None, status_code=204
        """
        return user_service.delete(user_id)


@ns.route('/token')
@auth.login_required
def get_auth_token():
    """
    generates the authentication token for the current user with a ttl of
    :return:
    """
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    found_user = Users.verify_auth_token(username_or_token)
    if not found_user:
        # try to authenticate with username/password
        found_user = Users.query.filter(Users.username == username_or_token).one()
        if not found_user or not found_user.verify_password(password):
            return False
    g.user = found_user
    return True
