from blog_app.database import db
from blog_app.database.models import Article, Category


def create_article(data):
    title = data.get('title')
    content = data.get('content')
    category_id = data.get('category_id')
    category = Category.query.filter(Category.id == category_id).one()
    article = Article(title, content, category)
    db.session.add(article)
    db.session.commit()


def update_article(article_id, data):
    article = Article.query.filter(Article.id == article_id).one()
    article.title = data.get('title')
    article.content = data.get('content')
    category_id = data.get('category_id')
    article.category = Category.query.filter(Category.id == category_id).one()
    db.session.add(article)
    db.session.commit()


def delete_article(article_id):
    article = Article.query.filter(Article.id == article_id).one()
    db.session.delete(article)
    db.session.commit()


def create_category(data):
    name = data.get('name')
    category_id = data.get('id')
    category = Category(name)
    if category_id:
        category.id = category_id

    db.session.add(category)
    db.session.commit()


def update_category(category_id, data):
    category = Category.query.filter(Category.id == category_id).one()
    category.name = data.get['name']
    db.sesson.add(category)
    db.session.commit()


def delete_category(category_id):
    category = Category.query.filter(Category.id == category_id).one()
    db.session.delete(category)
    db.session.commit()
