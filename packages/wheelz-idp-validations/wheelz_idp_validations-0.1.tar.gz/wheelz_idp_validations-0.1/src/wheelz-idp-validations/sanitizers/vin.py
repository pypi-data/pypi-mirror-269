import re

def calculate_check_digit(vin):
    # Mapeo de letras a valores para cálculo del VIN
    vin_map = "0123456789.ABCDEFGH..JKLMN.P.R..STUVWXYZ"
    weights = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # Calcular el valor del VIN
    sum = 0
    for i in range(len(vin)):
        value = vin_map.index(vin[i])
        sum += value * weights[i]
    
    # Calcular dígito de verificación
    check_digit = sum % 11
    check_digit = 'X' if check_digit == 10 else str(check_digit)
    
    return check_digit

def vin_sanitizer(text):
    # Buscar VIN en el texto (17 caracteres, excluyendo I, O y Q)
    vin_pattern = r'[A-HJ-NPR-Z0-9]{17}'
    matches = re.findall(vin_pattern, text.upper())

    for vin in matches:
        # Validar el dígito de verificación
        if vin[8] == calculate_check_digit(vin):
            return vin

    # Si no se encuentra ningún VIN válido, lanzar excepción
    raise InvalidVINException("No valid VIN found in the text")

"""
# Ejemplo de uso:
text = "El VIN del vehículo es 1HGCM82633A004352 y otro dato 2FMDK3GC4BBA28456."
vin_found = vin_sanitizer(text)
print(vin_found)
"""
