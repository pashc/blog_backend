import time
from datetime import datetime

from blog_app.database import db

ARTICLE_ID = db.Sequence('article_id_seq', start=0)


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True, server_default=ARTICLE_ID.next_value())
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    pub_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(id=self.id,
                    title=self.title,
                    content=self.content,
                    pub_date=time.mktime(self.pub_date.timetuple()),
                    category_id=self.category_id)

    def __repr__(self):
        return '<Article %r>' % self.title
