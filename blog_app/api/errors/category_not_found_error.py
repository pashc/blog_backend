class CategoryNotFoundException(Exception):
    code = 404

    def __init__(self, category_id):
        Exception.__init__(self)
        self.category_id = category_id

    def to_dict(self):
        return {
            "success": False,
            "error": {
                "type": "CategoryNotFoundException",
                "message": 'The category with the id=[%s] could not be found.' % self.category_id
            }
        }
