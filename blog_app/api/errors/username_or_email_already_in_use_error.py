class UsernameOrEmailAlreadyInUseException(Exception):
    code = 400

    def __init__(self):
        Exception.__init__(self)

    def to_dict(self):
        return {
            "success": False,
            "error": {
                "type": "UsernameOrEmailAlreadyInUseException",
                "message": "The Username or Email is already in use."
            }
        }
