from . import api_bp
from ..models import User, BlockedUser, Product
from ..helper_json import json_response
from flask import request

@api_bp.route('/users', methods=['GET'])
def get_users():
    name = request.args.get('name')
    if name:
        User.db_enable_debug()
        my_filter = User.name.ilike('%' + name + '%')
        users = User.db_query_with(BlockedUser).filter(my_filter)
    else:
        users = User.get_all_with(BlockedUser)
    data = User.to_dict_collection(users)
    return json_response(data)

@api_bp.route('/users/<int:id>', methods=['GET'])
def get_profile(id):
    usuario = User.query.get_or_404(id)
    
    perfil_usuario = {
        'id': usuario.id,
        'nombre': usuario.name,
        'email': usuario.email,
        'role': usuario.role,
        'verified': usuario.verified,
    }

    return json_response(perfil_usuario)

@api_bp.route('/users/<int:user_id>/products', methods=['GET'])
def get_user_products(user_id):
    usuario = User.query.get_or_404(user_id)

    user_products = Product.query.filter_by(seller_id=user_id).all()

    products_data = [
        {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'price': float(product.price),
        }
        for product in user_products
    ]

    return json_response(products_data)