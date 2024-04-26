import re
from ..exceptions.id_exceptions import *


# If we are looking to check only for the first match in a given text, we must use this function with
# keep_search=False, otherwise, it must be keep_searching=True
# received_id variable stand for chatgpt output or, if keep_searching=True, for all ID text.
def sanitize_id_number(received_id, keep_searching):
    dni_regexp = "([0-9O]{8})([A-Z])"
    letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    not_valid = {"00000000T", "00000001R", "99999999R"}

    # Get an iterator of all the matches
    matches = list(re.finditer(dni_regexp, received_id))

    # If there is no match, throw exception
    if not matches:
        if keep_searching:
            raise NoValidIDFoundInMultipleSearchException(received_id)
        raise NoIDMatchFoundException(received_id)

    # If keep_search=True, we will store here valid ID numbers
    id_list = []

    for match in matches:
        # Replace O (letter) for 0 (number) in case of errors
        processed_id = match.group(1).replace('O', '0')
        # Add the letter to the ID
        processed_id += match.group(2)

        # Received id cannot be one of these: "00000000T", "00000001R", "99999999R"
        if processed_id in not_valid:
            # If we have one of this ID numbers, it means we found the correct string and the ID is invalid.
            # So we stop searching for other matches
            raise InvalidIDException(received_id)

        # Getting the module of the ID number with 23, gives us the position of the letter
        # the ID number should have on the defined letters array
        if not processed_id[8] == letters[int(processed_id[0:8]) % 23]:
            # If we are doing multiple search
            if keep_searching:
                # We did not find anything valid in this iteration, so we continue to the next
                continue
            # Else we throw an error
            raise IDValidationFailedException(processed_id)

        # If doing multiple search, add the valid ID number to a list
        if keep_searching:
            id_list.append(processed_id)
            continue

        # If not, return the found ID number without looking other matches
        return processed_id

    # If id_list is empty, we raise an error, else we return the list.
    if not id_list:
        raise NoValidIDFoundInMultipleSearchException(received_id)

    return id_list
