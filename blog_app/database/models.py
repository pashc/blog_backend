from datetime import datetime

from blog_app.database import db

ARTICLE_ID = db.Sequence('article_id_seq', start=0)
CATEGORY_ID = db.Sequence('category_id_seq', start=0)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, ARTICLE_ID, primary_key=True, server_default=ARTICLE_ID.next_value())
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref=db.backref('articles', lazy='dynamic'))

    def __init__(self, title, content, category, pub_date=None):
        self.title = title
        self.content = content
        self.category = category
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Article %r>' % self.title


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, CATEGORY_ID, primary_key=True, server_default=CATEGORY_ID.next_value())
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name
