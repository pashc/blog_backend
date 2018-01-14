class ArticleNotFoundException(Exception):
    code = 404

    def __init__(self, article_id):
        Exception.__init__(self)
        self.article_id = article_id

    def to_dict(self):
        return {
            "success": False,
            "error": {
                "type": "ArticleNotFoundException",
                "message": 'The article with the id=[%s] could not be found.' % self.article_id
            }
        }
