from blog_app.database import db
from blog_app.database.models.auth.users import Users


def find(user_id):
    return Users.query.filter(Users.id == user_id).one()


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
