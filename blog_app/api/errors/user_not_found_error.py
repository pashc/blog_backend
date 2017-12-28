class UserNotFoundException(Exception):
    code = 404

    def __init__(self, user_id):
        Exception.__init__(self)
        self.user_id = user_id

    def to_dict(self):
        return {
            "success": False,
            "error": {
                "type": "UserNotFoundException",
                "message": 'The User with the id=[%s] could not be found.' % self.user_id
            }
        }
