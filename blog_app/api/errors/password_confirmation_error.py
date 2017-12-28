class PasswordConfirmationException(Exception):
    code = 400

    def __init__(self):
        Exception.__init__(self)

    def to_dict(self):
        return {
            "success": False,
            "error": {
                "type": "PasswordConfirmationException",
                "message": "The password confirmation failed."
            }
        }
