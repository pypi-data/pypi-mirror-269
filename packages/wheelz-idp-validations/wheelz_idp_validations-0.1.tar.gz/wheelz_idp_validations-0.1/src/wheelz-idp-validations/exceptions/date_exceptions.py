from ..sanitize_exception import SanitizeException


class InvalidBirthDateException(SanitizeException):
    def __init__(self, found_birthdate):
        self.message = ('Specified birth date does not match the format DD/MM/YYYY - '
                        'Birth Date Found: ' + found_birthdate)
        super().__init__(self.message)


class InvalidExpirationDateException(SanitizeException):
    def __init__(self, found_expiration_date):
        self.message = ('Specified expiration date does not match the format DD/MM/YYYY - '
                        'Expiration Date Found: ' + found_expiration_date)
        super().__init__(self.message)
