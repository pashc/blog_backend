from blog_app.database import db
from blog_app.database.models.articles import Articles
from blog_app.database.models.categories import Categories


def create_article(data):
    title = data.get('title')
    content = data.get('content')
    category_id = data.get('category_id')
    category = Categories.query.filter(Categories.id == category_id).one()
    article = Articles(title, content, category)
    db.session.add(article)
    db.session.commit()


def update_article(article_id, data):
    article = Articles.query.filter(Articles.id == article_id).one()
    article.title = data.get('title')
    article.content = data.get('content')
    category_id = data.get('category_id')
    article.category = Categories.query.filter(Categories.id == category_id).one()
    db.session.add(article)
    db.session.commit()


def delete_article(article_id):
    article = Articles.query.filter(Articles.id == article_id).one()
    db.session.delete(article)
    db.session.commit()


def create_category(data):
    name = data.get('name')
    category_id = data.get('id')
    category = Categories(name)
    if category_id:
        category.id = category_id

    db.session.add(category)
    return db.session.commit()


def update_category(category_id, data):
    category = Categories.query.filter(Categories.id == category_id).one()
    category.name = data.get['name']
    db.sesson.add(category)
    db.session.commit()


def delete_category(category_id):
    category = Categories.query.filter(Categories.id == category_id).one()
    db.session.delete(category)
    db.session.commit()
