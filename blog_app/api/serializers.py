from flask_restplus import fields

from blog_app.api import api

blog_article = api.model('Blog Article', {
    'id': fields.Integer(readOnly=True, description='unique identifier of an article'),
    'title': fields.String(required=True, description='article title'),
    'content': fields.String(required=True, description='article content'),
    'pub_date': fields.DateTime,
    'category_id': fields.Integer(attribute='category.id'),
    'category': fields.String(attribute='category.title')
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='number of the current page of the results'),
    'pages': fields.Integer(description='total number of pages of results'),
    'per_page': fields.Integer(description='number of articles per page of results'),
    'total': fields.Integer(description='total number of results')
})

page_of_articles = api.inherit('Page of articles', pagination, {
    'items': fields.List(fields.Nested(blog_article))
})

category = api.model('Blog Category', {
    'id': fields.Integer(readOnly=True, description='unique identifier of a category'),
    'name': fields.String(required=True, description='Category name')
})

category_with_articles = api.inherit('Blog category with articles', category, {
    'articles': fields.List(fields.Nested(blog_article))
})

user = api.model('User', {
    'username': fields.String(required=True, description='username'),
    'email': fields.String(required=True, description='user email')
})

user_register = api.inherit('Register User', user, {
    'password': fields.String(required=True, description='password'),
    'confirm': fields.String(required=True, description='password confirmation'),
})
