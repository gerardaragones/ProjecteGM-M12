from . import api_bp
from .errors import not_found
from ..models import Category, Product
from ..helper_json import json_response
from flask import current_app

# List
@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.get_all()
    data = Category.to_dict_collection(categories)
    return json_response(data)

# Read
@api_bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.get(id)
    if category:
        data = category.to_dict()
        return json_response(data)
    else:
        current_app.logger.debug("Category {} not found".format(id))
        return not_found("Category not found")

# Products list
@api_bp.route('/categories/<int:id>/products', methods=['GET'])
def get_category_products(id):
    products = Product.get_all_filtered_by(category_id=id)
    data = Product.to_dict_collection(products)
    return json_response(data)