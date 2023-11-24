from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_user, login_required, logout_user
from . import login_manager
from .models import User
from .forms import LoginForm
from . import db_manager as db
from werkzeug.security import check_password_hash

# Blueprint
auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ya está autenticado, salimos de aquí
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = LoginForm()
    if form.validate_on_submit():  # si se ha enviado el formulario via POST y es correcto
        # Quitamos la parte relacionada con el correo electrónico
        name = form.name.data
        plain_text_password = form.password.data

        user = load_user(name)
        if user and user.password == plain_text_password:
            #check_password_hash
            login_user(user)
            return redirect(url_for("main_bp.init"))

        # si llega aquí, es que no se ha autenticado correctamente
        return redirect(url_for("auth_bp.login"))

    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(name):
    if name is not None:
        # select con 1 resultado o ninguno
        user_or_none = db.session.query(User).filter(User.name == name).one_or_none()
        return user_or_none
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))