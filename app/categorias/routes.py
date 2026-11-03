
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required

from app.categorias import categorias_bp
from app.models import db, Categoria, Anuncio


@categorias_bp.route("/")
@login_required
def listar():
    categorias = Categoria.query.all()
    return render_template(
        "categorias/listar.html",
        categorias=categorias
    )


@categorias_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():

    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")

        if Categoria.query.filter_by(nombre=nombre).first():
            flash("Esta categoría ya existe", "danger")
            return redirect(url_for("categorias.nuevo"))

        categoria = Categoria(
            nombre=nombre,
            descripcion=descripcion
        )

        db.session.add(categoria)
        db.session.commit()

        flash("Categoría registrada correctamente", "success")
        return redirect(url_for("categorias.listar"))

    return render_template(
        "categorias/formulario.html",
        categoria=None
    )


@categorias_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):

    categoria = db.session.get(Categoria, id)

    if categoria is None:
        return "Categoría no encontrada", 404

    if request.method == "POST":
        categoria.nombre = request.form.get("nombre")
        categoria.descripcion = request.form.get("descripcion")

        db.session.commit()

        flash("Categoría actualizada correctamente", "success")
        return redirect(url_for("categorias.listar"))

    return render_template(
        "categorias/formulario.html",
        categoria=categoria
    )


@categorias_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):

    categoria = db.session.get(Categoria, id)

    if categoria is None:
        return "Categoría no encontrada", 404

    if Anuncio.query.filter_by(categoria_id=id).first():
        flash(
            "No se puede eliminar: tiene anuncios asociados",
            "warning"
        )
        return redirect(url_for("categorias.listar"))

    db.session.delete(categoria)
    db.session.commit()

    flash("Categoría eliminada correctamente", "success")
    return redirect(url_for("categorias.listar"))
