from services.models import Product
from services.extensions import db, migrate

class ProductService:

    @staticmethod
    def get_all_products(filters):
        query = Product.query

        search = filters.get("search")
        min_price = filters.get("min_price")
        max_price = filters.get("max_price")
        limit = filters.get("limit")

        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if limit:
            query = query.limit(limit)

        return query.all()


    @staticmethod
    def get_product_by_id(product_id):
        return Product.query.get(product_id)


    @staticmethod
    def add_product(data):
        product = Product(
            name=data["name"],
            price=data["price"]
        )
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def update_product(product, data):
        product.name = data.get("name", product.name)
        product.price = data.get("price", product.price)

        db.session.commit()
        return product

    @staticmethod
    def delete_product(product):
        db.session.delete(product)
        db.session.commit()