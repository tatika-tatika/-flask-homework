def validate_product(data):
    errors = []

    name = data.get("name")
    price = data.get("price")

    if not name or len(name) < 2:
        errors.append("Name must be at least 2 characters")

    if price is None:
        errors.append("Price is required")
    elif not isinstance(price, (int, float)):
        errors.append("Price must be number")
    elif price < 0:
        errors.append("Price cannot be negative")

    return errors


def validate_filters(args):
    errors = []

    min_price = args.get("min_price")
    max_price = args.get("max_price")

    if min_price and max_price and float(min_price) > float(max_price):
        errors.append("min_price cannot be greater than max_price")

    return errors