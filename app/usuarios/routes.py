from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from werkzeug.security import generate_password_hash

from app.usuarios import usuarios_bp
from app.models import db, Usuario


@usuarios_bp.route("/")
@login_required
def listar():
    usuarios = Usuario.query.all()
    return render_template("usuarios/listar.html", usuarios=usuarios)


@usuarios_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():

    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        password = request.form.get("password")
        rol = request.form.get("rol", "usuario")

        if Usuario.query.filter_by(correo=correo).first():
            flash("El correo ya está registrado", "danger")
            return redirect(url_for("usuarios.nuevo"))

        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            password_hash=generate_password_hash(password),
            rol=rol
        )

        db.session.add(usuario)
        db.session.commit()

        flash("Usuario agregado correctamente", "success")
        return redirect(url_for("usuarios.listar"))

    return render_template("usuarios/formulario.html", usuario=None)


@usuarios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):

    usuario = db.session.get(Usuario, id)

    if usuario is None:
        return "Usuario no encontrado", 404

    if request.method == "POST":
        usuario.nombre = request.form.get("nombre")
        usuario.correo = request.form.get("correo")
        usuario.rol = request.form.get("rol")

        password = request.form.get("password")

        if password:
            usuario.password_hash = generate_password_hash(password)

        db.session.commit()

        flash("Usuario actualizado correctamente", "success")
        return redirect(url_for("usuarios.listar"))

    return render_template("usuarios/formulario.html", usuario=usuario)


@usuarios_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):

    usuario = db.session.get(Usuario, id)

    if usuario is None:
        return "Usuario no encontrado", 404

    if usuario.anuncios:
        flash("No se puede eliminar: el usuario tiene anuncios asociados", "warning")
        return redirect(url_for("usuarios.listar"))

    db.session.delete(usuario)
    db.session.commit()

    flash("Usuario eliminado correctamente", "success")

    return redirect(url_for("usuarios.listar"))