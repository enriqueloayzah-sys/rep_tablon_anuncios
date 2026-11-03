
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.anuncios import anuncios_bp
from app.models import db, Anuncio, Categoria


@anuncios_bp.route("/")
@login_required
def listar():

    if current_user.rol == "admin":
        anuncios = Anuncio.query.order_by(
            Anuncio.fecha_publicacion.desc()
        ).all()
    else:
        anuncios = Anuncio.query.filter_by(
            usuario_id=current_user.id
        ).order_by(Anuncio.fecha_publicacion.desc()).all()

    return render_template("anuncios/listar.html", anuncios=anuncios)


@anuncios_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():

    categorias = Categoria.query.all()

    if request.method == "POST":
        anuncio = Anuncio(
            titulo=request.form.get("titulo"),
            contenido=request.form.get("contenido"),
            categoria_id=request.form.get("categoria_id"),
            usuario_id=current_user.id
        )

        db.session.add(anuncio)
        db.session.commit()

        flash("Anuncio publicado correctamente", "success")
        return redirect(url_for("anuncios.listar"))

    return render_template(
        "anuncios/formulario.html",
        anuncio=None,
        categorias=categorias
    )


@anuncios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):

    anuncio = db.session.get(Anuncio, id)

    if anuncio is None:
        return "Anuncio no encontrado", 404

    if current_user.rol != "admin" and anuncio.usuario_id != current_user.id:
        return "No tienes permiso para editar este anuncio", 403

    categorias = Categoria.query.all()

    if request.method == "POST":
        anuncio.titulo = request.form.get("titulo")
        anuncio.contenido = request.form.get("contenido")
        anuncio.categoria_id = request.form.get("categoria_id")

        db.session.commit()

        flash("Anuncio actualizado correctamente", "success")
        return redirect(url_for("anuncios.listar"))

    return render_template(
        "anuncios/formulario.html",
        anuncio=anuncio,
        categorias=categorias
    )


@anuncios_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):

    anuncio = db.session.get(Anuncio, id)

    if anuncio is None:
        return "Anuncio no encontrado", 404

    if current_user.rol != "admin" and anuncio.usuario_id != current_user.id:
        return "No tienes permiso para eliminar este anuncio", 403

    db.session.delete(anuncio)
    db.session.commit()

    flash("Anuncio eliminado correctamente", "success")
    return redirect(url_for("anuncios.listar"))
