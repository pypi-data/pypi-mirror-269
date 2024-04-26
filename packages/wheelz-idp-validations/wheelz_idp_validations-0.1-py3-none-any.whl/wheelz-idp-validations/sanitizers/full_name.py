import re


def sanitize_fullname(received_name, received_first_surname, received_second_surname):
    # Check if name and surnames are correct by reviewing its boundaries. They must be in capital letters too.
    # We use + quantifier because there may be names that have more than one word.
    pattern = re.compile(r'\b[À-ÖA-Z]+\b')

    # TODO Possible improvement to this regexp. Explained below:
    # r'[À-ÖA-Z]+( [À-ÖA-Z])*' --> This new regexp can match this "hadsfLLUIS ALIAÑOañlskj"

    processed_name = pattern.findall(received_name)
    processed_first_surname = pattern.findall(received_first_surname)
    processed_second_surname = pattern.findall(received_second_surname)

    if not processed_name or not processed_first_surname or not processed_second_surname:
        raise InvalidFullNameException(received_name
                                       + received_first_surname
                                       + received_second_surname)

    return " ".join(processed_name), " ".join(processed_first_surname), " ".join(processed_second_surname)
