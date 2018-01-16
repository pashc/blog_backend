from blog_app.api.errors.article_not_found_error import ArticleNotFoundException
from blog_app.api.services import category_service
from blog_app.database import db
from blog_app.database.models.blog.article import Article


def find(article_id):
    found_article = Article.query.get(article_id)

    if found_article is None:
        raise ArticleNotFoundException(article_id)

    return found_article


def paginate(data):
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)

    return Article.query.paginate(page, per_page, error_out=False).items


def create(data):
    title = data.get('title')
    content = data.get('content')
    category_id = data.get('category_id')
    category = None

    if category_id:
        category = category_service.find(category_id)

    article = Article(title, content, category)

    db.session.add(article)
    db.session.commit()


def update(article_id, data):
    article = find(article_id)

    title = data.get('title')
    content = data.get('content')
    category_id = data.get('category_id')

    if title:
        article.title = title
    if content:
        article.content = content
    if category_id:
        article.category = category_service.find(category_id)

    db.session.add(article)
    db.session.commit()


def delete(article_id):
    article = find(article_id)

    db.session.delete(article)
    db.session.commit()
