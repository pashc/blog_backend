from blog_app.api.errors.category_not_found_error import CategoryNotFoundException
from blog_app.database import db
from blog_app.database.models.blog.category import Category


def find(category_id):
    found_category = Category.query.get(category_id)

    if found_category is None:
        raise CategoryNotFoundException(category_id)

    return found_category


def find_all():
    return Category.query.all()


def create(data):
    name = data.get('name')
    category_id = data.get('id')
    category = Category(name)

    if category_id:
        category.id = category_id

    db.session.add(category)
    db.session.commit()

    return category


def update(category_id, data):
    category = find(category_id)
    category.name = data.get('name')

    db.session.add(category)
    db.session.commit()

    return category


def delete(category_id):
    category = find(category_id)

    db.session.delete(category)
    db.session.commit()
