from flask import Blueprint, render_template, redirect, url_for, flash, current_app, Flask, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from .models import Product, Category, User
from .forms import ProductForm, DeleteForm, RegisterForm
from werkzeug.utils import secure_filename
from . import db_manager as db
import uuid
import os
from io import TextIOWrapper
import csv
from werkzeug.security import generate_password_hash


# Blueprint
admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates/admin", static_folder="static"
)

@admin_bp.route('/admin')
@login_required
@require_editor_role.require(http_exception=403)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@login_required
@require_editor_role.require(http_exception=403)
def admin_users():
    users = db.session.query(User).all()
    return render_template('users_list.html', users=users)