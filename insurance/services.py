def calculate_premium_logic(age, vehicle_type, accidents):

    premium = 50

    # Age factor
    if age < 25:
        premium *= 1.2

    # Vehicle adjustment
    if vehicle_type == "motorcycle":
        premium += 10
    elif vehicle_type == "car":
        premium += 20
    elif vehicle_type == "electric_scooter":
        premium -= 5

    # Accident history
    premium += accidents * 15

    return round(premium, 2)