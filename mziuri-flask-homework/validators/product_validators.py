class ProductService:

    @staticmethod
    def get_all_products(products, filters):
        result = products

        search = filters.get("search")
        min_price = filters.get("min_price")
        max_price = filters.get("max_price")
        limit = filters.get("limit")

        if search:
            result = [p for p in result if search.lower() in p["name"].lower()]

        if min_price is not None:
            result = [p for p in result if p["price"] >= min_price]

        if max_price is not None:
            result = [p for p in result if p["price"] <= max_price]

        if limit:
            result = result[:limit]

        return result


    @staticmethod
    def get_product_by_id(product_id, products):
        for p in products:
            if p["id"] == product_id:
                return p
        return None


    @staticmethod
    def add_product(new_data, products):
        new_id = max([p["id"] for p in products]) + 1 if products else 1
        new_data["id"] = new_id
        products.append(new_data)
        return new_data