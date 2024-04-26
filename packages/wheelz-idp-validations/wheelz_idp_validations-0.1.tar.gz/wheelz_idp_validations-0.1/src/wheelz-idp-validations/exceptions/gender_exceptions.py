from ..sanitize_exception import SanitizeException


class InvalidGenderException(SanitizeException):
    def __init__(self, found_gender):
        self.message = ('Given gender is not valid because it is not "M" or "F" - '
                        'Gender Found ' + found_gender)
        super().__init__(self.message)