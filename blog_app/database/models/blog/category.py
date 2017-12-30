from blog_app.database import db

CATEGORY_ID = db.Sequence('category_id_seq', start=0)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, server_default=CATEGORY_ID.next_value())
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name
