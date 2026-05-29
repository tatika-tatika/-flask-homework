from flask import Flask, render_template, request, redirect, url_for, session
from services.extensions import db, migrate
from services.models import Product
from services.product_service import  ProductService
from validators.product_validators import validate_product, validate_filters

app = Flask(__name__)
app.secret_key = "12345678"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)



@app.route("/")
def index():
    filters = {
        "search": request.args.get("search"),
        "min_price": request.args.get("min_price", type=float),
        "max_price": request.args.get("max_price", type=float),
        "limit": request.args.get("limit", type=int),
    }

    products = ProductService.get_all_products(filters)
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
    session["last_filters"] = filters
    errors = validate_filters(filters)
    if errors:
        return {"success": False, "data": None, "message": errors}, 400

    result = ProductService.get_all_products(filters)

    return {
        "success": True,
        "data": [product.to_dict() for product in result]
    }, 200


@app.route("/api/products/id/<int:product_id>")
def get_by_id(product_id):
    product = ProductService.get_product_by_id(product_id)

    if not product:
        return {"success": False, "message": "Not found"}, 404

    return {"success": True, "data": product.to_dict()}, 200


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

    ProductService.add_product(data)

    return redirect(url_for("index"))



@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    product = ProductService.get_product_by_id(product_id)

    if not product:
        return {"success": False, "message": "Not found"}, 404

    data = request.json

    updated = ProductService.update_product(product, data)

    return {"success": True, "message": "Updated"}, 200



@app.route("/api/products/<int:product_id>", methods=["PATCH"])
def patch_product(product_id):

    product = ProductService.get_product_by_id(product_id)

    if not product:
        return {"success": False,  "message": "Not found"}, 404

    data = request.json

    updated = ProductService.update_product(product, data)

    return {"success": True, "data": product.to_dict(), "message": "Patched"}, 200




@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    product = ProductService.get_product_by_id(product_id)

    if not product:
        return {"success": False, "message": "Not found"}, 404

    ProductService.delete_product(product)

    return {"success": True, "message": "Deleted"}, 200


if __name__ == "__main__":
    app.run(debug=True)