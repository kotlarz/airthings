def parse_radon_data(radon_data):
    return radon_data if 0 <= radon_data <= 16383 else None
