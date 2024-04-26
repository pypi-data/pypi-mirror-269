from ..sanitize_exception import SanitizeException

class InvalidPlateException(SanitizeException):
    def __init__(self, plate):
        self.plate = plate
        super().__init__(f"Invalid plate format: {plate}")
