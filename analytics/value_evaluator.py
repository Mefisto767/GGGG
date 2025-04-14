def is_value_bet(probability: float, odds: float, threshold: float = 0.05) -> bool:
    value = (probability * odds) - 1
    return value > threshold

def calculate_value(probability: float, odds: float) -> float:
    return (probability * odds) - 1
