import re

def sanitize_plate(text):
    # Definir patrones para los diferentes tipos de matrículas
    patterns = [
        r'\b\d{4}[BCDFGHJKLMNPQRSTVWXYZ]{3}\b',       # Tipo 1: 4 números seguidos de 3 letras no vocales
        r'\b[A-Z]{1,3}-\d{6}\b',                       # Tipo 2: Hasta 3 letras, guion, 6 números
        r'\b[A-Z]{1,2}-\d{4}-[A-Z]{1,2}\b',            # Tipo 3: 1-2 letras, guion, 4 números, guion, 1-2 letras
        r'\bR\d{3}[A-Z]{3}\b',                         # Tipo 4: Una R, 3 números y 3 letras
        r'\bH\d{4}[A-Z]{3}\b',                         # Tipo 5: Una H, 4 números y 3 letras
        r'\bC\d{4}[A-Z]{3}\b',                         # Tipo 6: Una C, 4 números y 3 letras
    ]

    # Buscar la primera matrícula que coincida con alguno de los patrones
    for pattern in patterns:
        match = re.search(pattern, text.upper().replace(' ', ''))
        if match:
            return match.group(0)

    # Si no se encuentra ninguna matrícula, lanzar excepción
    raise InvalidPlateException("No valid plate found in the text")

# Ejemplo de uso:
"""
text = 'El vehículo tiene la matrícula 1715JYL. Otro texto R123YHG, y más información H1234BBB.'
first_plate = extract_first_plate(text)
print(first_plate)  # Debería imprimir la primera matrícula válida encontrada
"""
