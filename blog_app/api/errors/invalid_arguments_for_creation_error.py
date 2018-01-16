class InvalidArgumentsForCreationException(Exception):
    code = 422

    def __init__(self, errors):
        Exception.__init__(self)
        self.errors = errors

    def to_dict(self):
        return {
            "success": False,
            "errors": self.errors
        }
