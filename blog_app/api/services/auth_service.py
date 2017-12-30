from flask import g
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

from blog_app.api.errors.password_confirmation_error import PasswordConfirmationException
from blog_app.api.errors.user_not_found_error import UserNotFoundException
from blog_app.api.errors.username_or_email_already_in_use_error import UsernameOrEmailAlreadyInUseException
from blog_app.database import db
from blog_app.database.models.auth.user import User


def find(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise UserNotFoundException(user_id)
    return user


def register(data):
    if data.get('password') != data.get('confirm'):
        raise PasswordConfirmationException()

    if __username_or_password_already_exists(data.get('username'), data.get('email')):
        raise UsernameOrEmailAlreadyInUseException()

    __create(data)
    return None, 201


def update(user_id, data):
    user = find(user_id)

    user.username = data.get('username')
    user.hash_password(data.get('password'))

    db.session.add(user)
    db.session.commit()
    return None, 204


def delete(user_id):
    user = find(user_id)

    db.session.delete(user)
    db.session.commit()
    return None, 204


def verify_password(username_or_token, password):
    # first try to authenticate by token
    found_user = User.verify_auth_token(username_or_token)
    if not found_user:
        # try to authenticate with username/password
        try:
            found_user = User.query.filter(User.username == username_or_token).one()
            return found_user.verify_password(password)
        except NoResultFound:
            return False
    g.user = found_user
    return True


def __username_or_password_already_exists(username, email):
    try:
        found_user = User.query.filter(or_(User.username == username, User.email == email)).one()
        return found_user is not None
    except NoResultFound:
        return False


def __create(data):
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    user = User(username, email, password)

    db.session.add(user)
    db.session.commit()
    return None, 201
