def run():
    """
    Dynamic pricing logic for urban parking
    """

    # Inputs (can later come from sensors / APIs)
    base_price = 50          # base price per hour
    occupancy_rate = 0.75    # 75% parking occupied
    time_of_day = "peak"     # peak / offpeak

    # Demand multiplier
    if occupancy_rate > 0.8:
        demand_multiplier = 1.5
    elif occupancy_rate > 0.6:
        demand_multiplier = 1.2
    else:
        demand_multiplier = 1.0

    # Time-based multiplier
    if time_of_day == "peak":
        time_multiplier = 1.3
    else:
        time_multiplier = 1.0

    final_price = base_price * demand_multiplier * time_multiplier

    return {
        "base_price": base_price,
        "occupancy_rate": occupancy_rate,
        "time_of_day": time_of_day,
        "final_price_per_hour": round(final_price, 2)
    }
 