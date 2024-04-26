import re


def sanitize_dates(received_birth_date, received_expiration_date):

    # TODO Change format yyyy mm dd
    # Dates must match this pattern
    pattern = re.compile(r'\d{2}/\d{2}/\d{4}')

    processed_birth_date = pattern.search(received_birth_date)
    processed_expiration_date = pattern.search(received_expiration_date)

    if not processed_birth_date:
        raise InvalidBirthDateException(processed_birth_date)

    if not processed_expiration_date:
        raise InvalidExpirationDateException(processed_birth_date)

    return processed_birth_date.group(), processed_expiration_date.group()
