import math

def calculate_entropy(length: int, pool_size: int) -> float:
    """Calculate password entropy in bits."""
    if pool_size <= 0 or length <= 0:
        return 0.0
    try:
        entropy = length * math.log2(pool_size)
        return round(entropy, 2)
    except ValueError:
        return 0.0