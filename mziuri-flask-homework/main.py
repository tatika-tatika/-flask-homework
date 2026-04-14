from flask import Flask, render_template, request, redirect, url_for

from services.product_service import validate_product, validate_filters
from validators.product_validators import ProductService

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Phone", "price": 800},
    {"id": 3, "name": "Tablet", "price": 600},
]

@app.route("/")
def index():
    return render_template("index.html", products=products)


@app.route("/api/products", methods=["GET"])
@app.route("/api/products/<search>", methods=["GET"])
def get_products(search=None):

    filters = {
        "search": search or request.args.get("search"),
        "min_price": request.args.get("min_price", type=float),
        "max_price": request.args.get("max_price", type=float),
        "limit": request.args.get("limit", type=int),
    }

    errors = validate_filters(filters)
    if errors:
        return {"success": False, "data": None, "message": errors}, 400

    result = ProductService.get_all_products(products, filters)

    return {"success": True, "data": result, "message": None}, 200


@app.route("/api/products/id/<int:product_id>")
def get_by_id(product_id):
    product = ProductService.get_product_by_id(product_id, products)

    if not product:
        return {"success": False, "data": None, "message": "Not found"}, 404

    return {"success": True, "data": product, "message": None}, 200


@app.route("/add-product", methods=["GET", "POST"])
def add_product():

    if request.method == "GET":
        return render_template("add_product.html")

    data = {
        "name": request.form.get("name"),
        "price": request.form.get("price", type=float)
    }

    errors = validate_product(data)

    if errors:
        return render_template("add_product.html", error=errors)

    ProductService.add_product(data, products)

    return redirect(url_for("index"))


@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    product = ProductService.get_product_by_id(product_id, products)

    if not product:
        return {"success": False, "data": None, "message": "Not found"}, 404

    data = request.json

    product["name"] = data.get("name", product["name"])
    product["price"] = data.get("price", product["price"])

    return {"success": True, "data": product, "message": "Updated"}, 200



@app.route("/api/products/<int:product_id>", methods=["PATCH"])
def patch_product(product_id):

    product = ProductService.get_product_by_id(product_id, products)

    if not product:
        return {"success": False, "data": None, "message": "Not found"}, 404

    data = request.json

    if "name" in data:
        product["name"] = data["name"]

    if "price" in data:
        product["price"] = data["price"]

    return {"success": True, "data": product, "message": "Patched"}, 200


if __name__ == "__main__":
    app.run(debug=True)