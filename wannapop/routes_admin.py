from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import User, BlockedUser, Product, BannedProduct
from .forms import BlockUserForm, BanProduct
from .helper_role import Role, role_required
from . import db_manager as db

# Blueprint
admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/admin')
@role_required(Role.admin, Role.moderator)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@role_required(Role.admin)
def admin_users():
    users = db.session.query(User).all()
    blocked_users = {blocked_user.user_id for blocked_user in BlockedUser.query.all()}
    return render_template('admin/users_list.html', users=users, blocked_users=blocked_users)

@admin_bp.route('/admin/users/<int:user_id>/block', methods=['GET', 'POST'])
@role_required(Role.admin)
def block_user(user_id):
    user_to_block = User.query.get(user_id)
    form = BlockUserForm()

    blocked_reason = None

    if user_to_block:
        if request.method == 'POST' and form.validate_on_submit():
            blocked_user = BlockedUser(user_id=user_to_block.id, message=form.message.data)
            db.session.add(blocked_user)
            db.session.commit()
            blocked_reason = form.message.data
            flash(f'The user {user_to_block.name} has been blocked with message: {form.message.data}', 'success')
            return redirect(url_for('admin_bp.admin_users'))

        return render_template('admin/blocked_user.html', form=form, user=user_to_block, blocked_reason=blocked_reason)

    flash('User not found.', 'danger')
    return redirect(url_for('admin_bp.admin_users'))

@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=['GET', 'POST'])
@role_required(Role.admin)
def unblock_user(user_id):
    user_to_unblock = User.query.get(user_id)
    
    if user_to_unblock:
        blocked_user = BlockedUser.query.filter_by(user_id=user_to_unblock.id).first()
        
        if blocked_user:
            db.session.delete(blocked_user)
            db.session.commit()
            flash(f'The user {user_to_unblock.name} has been unblocked.', 'success')
        else:
            flash(f'The user {user_to_unblock.name} is not blocked.', 'warning')
    else:
        flash('User not found.', 'danger')
    
    return redirect(url_for('admin_bp.admin_users'))

@admin_bp.route('/admin/products/<int:product_id>/ban', methods=['GET', 'POST'])
@role_required(Role.moderator)
def ban_product(product_id):
    product_to_ban = Product.query.get(product_id)


    product_banned = BannedProduct.query.filter_by(product_id=product_to_ban.id).first()

    if product_to_ban and not product_banned:
        form = BanProduct()  # Inicializar el formulario

        if request.method == 'POST' and form.validate_on_submit():
            banned_product = BannedProduct(product_id=product_to_ban.id, reason=form.reason.data)
            db.session.add(banned_product)
            db.session.commit()
            flash(f'El producto {product_to_ban.title} ha sido bloqueado.', 'success')
            return redirect(url_for('products_bp.product_list'))

        return render_template('admin/ban_product.html', form=form, product=product_to_ban, product_banned=product_banned)

    flash('Producto no encontrado o el producto ya está bloqueado.', 'danger')
    return redirect(url_for('products_bp.product_list'))

@admin_bp.route('/admin/products/<int:product_id>/unban', methods=['POST'])
@role_required(Role.moderator)
def unban_product(product_id):
    product_to_unban = Product.query.get(product_id)

    if product_to_unban:
        banned_product = BannedProduct.query.filter_by(product_id=product_to_unban.id).first()

        if banned_product:
            db.session.delete(banned_product)
            db.session.commit()
            flash(f'The product {product_to_unban.title} has been unbanned.', 'success')
        else:
            flash(f'The product {product_to_unban.title} is not banned.', 'warning')
    else:
        flash('Product not found.', 'danger')

    return redirect(url_for('products_bp.product_list'))