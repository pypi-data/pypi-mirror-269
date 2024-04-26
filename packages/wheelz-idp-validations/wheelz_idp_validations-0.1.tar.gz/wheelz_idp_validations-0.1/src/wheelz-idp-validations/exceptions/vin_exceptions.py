from ..sanitize_exception import SanitizeException

class InvalidVINException(SanitizeException):
    def __init__(self, vin):
        self.vin = vin
        super().__init__(f"Invalid VIN: {vin}")
