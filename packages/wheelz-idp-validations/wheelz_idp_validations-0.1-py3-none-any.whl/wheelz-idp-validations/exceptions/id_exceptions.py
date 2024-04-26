from ..sanitize_exception import SanitizeException


class InvalidIDException(SanitizeException):
    def __init__(self, found_id):
        self.message = ('Given ID is not valid because it is one of these: "00000000T", "00000001R", "99999999R" - '
                        'ID Found: ' + found_id)
        super().__init__(self.message)


class NoIDMatchFoundException(SanitizeException):
    def __init__(self, found_id):
        self.message = ('No valid ID has been found - '
                        'ID Found: ' + found_id)
        super().__init__(self.message)


class IDValidationFailedException(SanitizeException):
    def __init__(self, found_id):
        self.message = ('The module of the given ID with 23 does not correspond with the letter it should have - '
                        'ID Found: ' + found_id)
        super().__init__(self.message)


class NoValidIDFoundInMultipleSearchException(SanitizeException):
    def __init__(self, text):
        self.message = ('There is no valid ID in this text - '
                        'Text: ' + text)
        super().__init__(self.message)