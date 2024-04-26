import re
#from ..exceptions.date_exceptions import *


# Cif algorithm documentation https://www.mapa.gob.es/app/materialvegetal/docs/CIF.pdf
def sanitize_cif(received_cif):
    cif_regexp_default = "([ABCDEFGHQSKLM])(\d{7})(\d)"
    # CIF Letters P and X may be on the end
    cif_regexp_special = "(\d)(\d{7})([PX])"
    special = False

    # Get only the CIF number (try first default CIF Format)
    match = re.search(cif_regexp_default, received_cif)

    # If there is no match, try second format, if failed, throw exception
    if not match:
        match = re.search(cif_regexp_special, received_cif)
        special = True
        if not match:
            print('hola')
            #raise NoCIFMatchFoundException(received_cif)

    # Replace O (letter) for 0 (number) in case of errors
    # We store digits and letter because we will use it later to validate CIF
    digits = match.group(2).replace('O', '0')
    if not special:
        letter = match.group(1)
        processed_cif = letter + digits + match.group(3).replace('O', '0')
    else:
        letter = match.group(3)
        processed_cif = match.group(1).replace('O', '0') + digits + letter

    # CIF Validation algorithm
    # 1 - Add pair position digits from digits string to total_sum
    # 2 - Multiply by two odd positions, then add their digits, finally add them to total+_sum
    total_sum = 0
    for pos in range(0, len(digits)):
        # Pair digits are in positions 1,3,5...
        if pos % 2:
            total_sum += int(digits[pos])
        # Odd digits are in position 0,2,4...
        else:
            total_sum += sum(int(digit) for digit in str(digits[pos] * 2))

    print(total_sum)


sanitize_cif("A58818501")
