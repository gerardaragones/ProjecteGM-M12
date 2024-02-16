from . import api_bp
from ..models import Product, Category, Order, BannedProduct
from .helper_json import json_request, json_response
from flask import current_app, request
from .errors import not_found, bad_request, forbidden_access
from .helper_auth import basic_auth, token_auth


#List
@api_bp.route('/products', methods=['GET'])
def get_products():
    title = request.args.get('title')
    if title:
        # Watch SQL at terminal
        Product.db_enable_debug()
        # Filter using query param
        my_filter = Product.title.like('%' + title + '%')
        products_with_category = Product.db_query_with(Category).filter(my_filter)
    else:
        # No filter
        products_with_category = Product.get_all_with(Category)
    data = Product.to_dict_collection(products_with_category)
    return json_response(data)

#Create
@api_bp.route('/products', methods=['POST'])
def create_product():
    try:
        data = json_request(['nom', 'category_id', 'unitats'])
    except Exception as e:
        current_app.logger.debug(e)
        return bad_request(str(e))
    else:
        product = Product.create(**data)
        current_app.logger.debug("CREATED product: {}".format(product.to_dict()))
        return json_response(product.to_dict(), 201)

#Read
@api_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    result = Product.get_with(id, Category, BannedProduct)
    if result:
        (product, category, banner_product) = result
        # Serialize data
        data = product.to_dict()
        # Add relationships
        data["category"] = category.to_dict()
        del data["category_id"]
        if banner_product:
            data["banned_product"] = banner_product.to_dict()
        return json_response(data)
    else:
        current_app.logger.debug("Product {} not found".format(id))
        return not_found("Product not found")
    
#List products and filter per title


#Update
@api_bp.route('/products/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_api_product(id):
    product = Product.get(id)
    if basic_auth.current_user().id == product.seller_id :
        data = json_request(['title','description', 'photo', 'price'],False)
        current_app.logger.debug(data)
        product.update(**data)
        return json_response(product.to_dict())
    else: 
        return forbidden_access("You are not the owner of this product")

#Delete
@api_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.get(id)
    if product:
        product.delete()
        current_app.logger.debug("DELETED product: {}".format(id))
        return json_response(product.to_dict())
    else:
        current_app.logger.debug("Product {} not found".format(id))
        return not_found("Product not found")
   
#List orders
@api_bp.route('/products/<int:id>/orders', methods=['GET'])
def get_product_offers(id):
    product = Product.get(id)
    orders = product.get_orders()
    data = Order.to_dict_collection(orders)
    return json_response(data)