import re


def sanitize_gender(received_gender):
    # Check if gender is correct (M or F separated with boundaries)
    match = re.search(r'[MF]', received_gender)

    if not match:
        raise InvalidGenderException(received_gender)

    return match.group()
