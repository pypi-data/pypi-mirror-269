from ..sanitize_exception import SanitizeException


class InvalidFullNameException(SanitizeException):
    def __init__(self, found_fullname):
        self.message = ('Specified name is not correct (Not in capital letters or next to a lowercase letter) - '
                        'Full Name Found: ' + found_fullname)
        super().__init__(self.message)
