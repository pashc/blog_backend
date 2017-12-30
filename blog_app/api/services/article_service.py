from blog_app.api.services import category_service
from blog_app.database import db
from blog_app.database.models.blog.article import Article


def find(article_id):
    return Article.query.filter(Article.id == article_id).one()


# todo add date validation
def find_by_date(data, year, month, day):
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)

    start_day = day if day else 1
    end_day = day + 1 if day else 31

    start_month = month if month else 1
    end_month = month + 1 if month else 12
    start_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, start_month, start_day)
    end_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, end_month, end_day)
    return Article.query.filter(
        Article.pub_date >= start_date).filter(
        Article.pub_date <= end_date).paginate(
        page, per_page, error_out=False)


def paginate(data):
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)

    return Article.query.paginate(page, per_page, error_out=False)


def create(data):
    title = data.get('title')
    content = data.get('content')
    category = category_service.find(data.get('category_id'))

    article = Article(title, content, category)

    db.session.add(article)
    db.session.commit()
    return None, 201


def update(article_id, data):
    article = find(article_id)

    article.title = data.get('title')
    article.content = data.get('content')
    # todo add not found validation
    article.category = category_service.find(data.get('category_id'))

    db.session.add(article)
    db.session.commit()
    return None, 204


def delete(article_id):
    article = find(article_id)

    db.session.delete(article)
    db.session.commit()
    return None, 204
