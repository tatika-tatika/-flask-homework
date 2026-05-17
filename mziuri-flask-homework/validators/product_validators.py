def validate_product(data):
    errors = []

    if not data.get("name"):
        errors.append("Name required")

    if data.get("price") is None:
        errors.append("Price required")

    return errors


def validate_filters(args):
    errors = []

    min_price = args.get("min_price")
    max_price = args.get("max_price")

    if min_price and max_price and min_price > max_price:
        errors.append("min_price cannot be greater than max_price")

    return errors
