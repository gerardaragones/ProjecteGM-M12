from . import api_bp
from ..models import User, BlockedUser, Product
from ..helper_json import json_request, json_response
from flask import current_app, request
from .errors import not_found, bad_request

@api_bp.route('/users', methods=['GET'])
def get_users():
    nom = request.args.get('nom')
    if nom:
        # Watch SQL at terminal
        User.db_enable_debug()
        # Filter using query param
        my_filter = User.nom.like('%' + nom + '%')
        blocked_users = User.db_query_with(BlockedUser).filter(my_filter)
    else:
        blocked_users = User.get_all_with(BlockedUser)
    data = User.to_dict_collection(blocked_users)
    return json_response(data)

@api_bp.route('/users/<int:id>', methods=['GET'])
def get_profile(id):
    usuario = User.query.get(id)
    if usuario:
        perfil_usuario = {
            'id': usuario.id,
            'nombre': usuario.name,
            'email': usuario.email,
            'role': usuario.role,
            'verified': usuario.verified,
        }
        return json_response(perfil_usuario)
    else:
        return json_response({'error': 'Usuario no encontrado'}, status_code=404)

@api_bp.route('/users/<int:user_id>/products', methods=['GET'])
def get_user_products(user_id):
    usuario = User.query.get(user_id)

    if usuario:
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
    else:
        return json_response({'error': 'Usuario no encontrado'}, status_code=404)