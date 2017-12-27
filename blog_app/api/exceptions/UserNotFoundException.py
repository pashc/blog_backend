class UserNotFoundException(Exception):
    code = 404

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        return {
            "success": False,
            "error": {
                "type": "UserNotFoundException",
                "message": self.message
            }
        }
