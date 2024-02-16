from . import api_bp
from .errors import bad_request
from .. import db_manager as db
from ..models import Order, ConfirmedOrder, Product, User
from ..helper_json import json_request, json_response
from flask import current_app, jsonify

@api_bp.route('/orders/<int:order_id>/confirmed', methods=['POST'])
def accept_order(order_id):
    order = Order.query.get(order_id)

    if order:
        if order.confirmed_order:
            return bad_request('Order already confirmed')

        confirmed_order = ConfirmedOrder(order=order)

        try:
            confirmed_order.save()
        except:
            return bad_request('Error confirming the order')

        current_app.logger.debug(f"Order {order_id} confirmed successfully")
        return jsonify(
            {   
                'data': order_id, 
                'success': True
            }), 200 
    else:
        return jsonify(
            {
                'error': 'Not Found', 
                'message': 'Order not found', 
                'success': False
            }), 404

@api_bp.route('/orders/<int:order_id>/confirmed', methods=['DELETE'])
def cancel_confirmed_order(order_id):
    confirmed_order = ConfirmedOrder.query.get(order_id)

    if confirmed_order:
        # Elimina la entrada de confirmed_orders
        try:
            confirmed_order.delete()
        except:
            return bad_request('Error canceling the confirmed order')

        current_app.logger.debug(f"ConfirmedOrder {order_id} canceled successfully")
        return jsonify(
            {
                'data': order_id, 
                'success': True
            }), 200  
    else:
        return jsonify(
            {
                'error': 'Not Found', 
                'message': 'ConfirmedOrder not found', 
                'success': False
            }), 404
    
from . import api_bp
from ..models import Order, User, Product
from ..helper_json import json_response, json_request, bad_request
from flask import current_app, jsonify

@api_bp.route('/orders', methods=['POST'])
def make_offer():
    data = json_request()

    # Verificar si los campos necesarios están presentes en la solicitud
    required_fields = ['product_id', 'buyer_id', 'offer']
    if not all(field in data for field in required_fields):
        return bad_request('Missing required fields')

    product_id = data['product_id']
    buyer_id = data['buyer_id']
    offer = data['offer']

    # Verificar si el producto y el comprador existen
    product = Product.query.get(product_id)
    buyer = User.query.get(buyer_id)

    if not product or not buyer:
        return bad_request('Product or buyer not found')

    # Crear una nueva orden (oferta)
    order = Order(product=product, buyer_id=buyer_id, offer=offer)

    try:
        order.save()
        current_app.logger.debug(f"Offer for product {product_id} made successfully")
        return jsonify({'success': True, 'order_id': order.id}), 201
    except Exception as e:
        return bad_request(f'Error making the offer: {str(e)}')

@api_bp.route('/orders/<int:order_id>', methods=['PUT'])
def edit_offer(order_id):
    data = json_request()

    # Verificar si los campos necesarios están presentes en la solicitud
    required_fields = ['offer']
    if not all(field in data for field in required_fields):
        return bad_request('Missing required fields')

    new_offer = data['offer']

    # Verificar si la oferta existe
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'error': 'Not Found', 'message': 'Order not found', 'success': False}), 404

    # Actualizar la oferta
    order.offer = new_offer

    try:
        order.save()
        current_app.logger.debug(f"Offer {order_id} edited successfully")
        return jsonify({'success': True, 'order_id': order.id}), 200
    except Exception as e:
        return bad_request(f'Error editing the offer: {str(e)}')
    
@api_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def cancel_offer(order_id):
    # Verificar si la oferta existe
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'error': 'Not Found', 'message': 'Order not found', 'success': False}), 404

    try:
        order.delete()
        current_app.logger.debug(f"Offer {order_id} canceled successfully")
        return jsonify({'success': True, 'order_id': order_id}), 200
    except Exception as e:
        return bad_request(f'Error canceling the offer: {str(e)}')