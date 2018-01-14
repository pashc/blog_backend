import logging

from flask import request, g
from flask.json import jsonify
from flask_restplus import Resource

from blog_app.api import api
from blog_app.api.errors.password_confirmation_error import PasswordConfirmationException
from blog_app.api.errors.user_not_found_error import UserNotFoundException
from blog_app.api.errors.username_or_email_already_in_use_error import UsernameOrEmailAlreadyInUseException
from blog_app.api.serializers import user, user_register
from blog_app.api.services import auth_service
from blog_app.auth import auth

log = logging.getLogger(__name__)

ns = api.namespace('auth', description='authentication related operations')


@ns.route('/users/<int:user_id>')
class UserItem(Resource):

    @api.marshal_with(user)
    def get(self, user_id):
        """
        :param user_id: the user to get
        :return: the user for the given id
        """
        return auth_service.find(user_id).to_dict(), 200

    @auth.login_required
    def delete(self, user_id):
        """
        deletes the user for the given id
        :param user_id: the user to delete
        :return: None, status_code=204
        """
        auth_service.delete(user_id)
        return None, 204


@ns.route("/register")
class Register(Resource):

    @api.expect(user_register)
    @api.response(201, "user successfully registered")
    def post(self):
        data = request.json
        return auth_service.register(data).to_dict(), 201


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
    return auth_service.verify_password(username_or_token, password)


@ns.errorhandler(UserNotFoundException)
@ns.errorhandler(PasswordConfirmationException)
@ns.errorhandler(UsernameOrEmailAlreadyInUseException)
def handle_user_not_found(error):
    return error.to_dict(), error.code
