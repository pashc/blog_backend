from sqlalchemy.orm.exc import NoResultFound

from blog_app.api.exceptions.UserNotFoundException import UserNotFoundException
from blog_app.database import db
from blog_app.database.models.auth.users import Users


def find(user_id):
    user = Users.query.get(user_id)
    if user is None:
        raise UserNotFoundException('the user with the id %s could not be found.' % user_id)
    return user


def create(data):
    username = data.get('username')
    password = data.get('password')

    user = Users(username, password)

    db.session.add(user)
    db.session.commit()
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
    found_user = Users.verify_auth_token(username_or_token)
    if not found_user:
        # try to authenticate with username/password
        try:
            found_user = Users.query.filter(Users.username == username_or_token).one()
            return found_user.verify_password(password)
        except NoResultFound:
            return False
    g.user = found_user
    return True
