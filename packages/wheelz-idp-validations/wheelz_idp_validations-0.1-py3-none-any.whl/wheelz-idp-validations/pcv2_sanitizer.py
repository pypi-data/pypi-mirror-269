from sanitizers.plate import sanitize_plate
from sanitizers.vin import sanitize_vin
from sanitizers.date import sanitize_dates


def sanitize_pcv2(response_dict):
    # Sanitize Plate
    response_dict["A"] = sanitize_plate(response_dict["A"])
    # Sanitize VIN
    response_dict["E"] = sanitize_vin(response_dict["E"])
    # Sanitize multiple Dates
    response_dict["B"], response_dict["H"], response_dict["I"], response_dict["I.1"] = (
        sanitize_dates(response_dict["B"], response_dict["H"], response_dict["I"], response_dict["I.1"]))
