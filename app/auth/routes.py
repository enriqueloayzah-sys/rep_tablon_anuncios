from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.auth import auth_bp
from app.models import db, Usuario


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        correo = request.form.get("correo")
        password = request.form.get("password")

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and check_password_hash(usuario.password_hash, password):
            login_user(usuario)
            return redirect(url_for("inicio"))

        flash("Correo o contraseña incorrectos", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        password = request.form.get("password")

        existente = Usuario.query.filter_by(correo=correo).first()

        if existente:
            flash("Este correo ya está registrado", "danger")
            return redirect(url_for("auth.registro"))

        cantidad = Usuario.query.count()

        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            password_hash=generate_password_hash(password),
            rol="admin" if cantidad == 0 else "usuario"
        )

        db.session.add(usuario)
        db.session.commit()

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/registro.html")


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Sesión cerrada correctamente", "success")

    return redirect(url_for("auth.login"))