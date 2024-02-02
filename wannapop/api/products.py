from . import api_bp
from ..models import Product, Category, BannedProduct
from ..helper_json import json_request, json_response
from flask import current_app, request
from .errors import not_found, bad_request


#List
@api_bp.route('/products', methods=['GET'])
def get_products():
    search = request.args.get('search')
    if search:
        # Watch SQL at terminal
        Product.db_enable_debug()
        # Filter using query param
        my_filter = Product.nom.like('%' + search + '%')
        products_with_store = Product.db_query_with(Category).filter(my_filter)
    else:
        # No filter
        products_with_store = Product.get_all_with(Category)
    data = Product.to_dict_collection(products_with_store)
    return json_response(data)

#Create
@api_bp.route('/products', methods=['POST'])
def create_product():
    try:
        data = json_request(['nom', 'store_id', 'unitats'])
    except Exception as e:
        current_app.logger.debug(e)
        return bad_request(str(e))
    else:
        product = Product.create(**data)
        current_app.logger.debug("CREATED product: {}".format(product.to_dict()))
        return json_response(product.to_dict(), 201)


#Read
@api_bp.route('/products/{id}', methods=['GET'])
def get_product(id):
    result = Product.get_with(id, Category, BannedProduct)
    if result:
        (product, store, discount) = result
        # Serialize data
        data = product.to_dict()
        # Add relationships
        data["store"] = store.to_dict()
        del data["store_id"]
        if (discount):
            data["discount"] = discount.discount
        return json_response(data)
    else:
        current_app.logger.debug("Product {} not found".format(id))
        return not_found("Product not found")

#Update
@api_bp.route('/products/{id}', methods=['PUT'])
def update_product(id):
    product = Product.get(id)
    if product:
        try:
            data = json_request(['nom', 'store_id', 'unitats'], False)
        except Exception as e:
            current_app.logger.debug(e)
            return bad_request(str(e))
        else:
            product.update(**data)
            current_app.logger.debug("UPDATED product: {}".format(product.to_dict()))
            return json_response(product.to_dict())
    else:
        current_app.logger.debug("Product {} not found".format(id))
        return not_found("Product not found")

#Delete
@api_bp.route('/products/{id}', methods=['DELETE'])
def delete_product(id):
    product = Product.get(id)
    if product:
        product.delete()
        current_app.logger.debug("DELETED product: {}".format(id))
        return json_response(product.to_dict())
    else:
        current_app.logger.debug("Product {} not found".format(id))
        return not_found("Product not found")