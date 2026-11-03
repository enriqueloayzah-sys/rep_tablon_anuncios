from flask import Blueprint

categorias_bp = Blueprint(
    "categorias",
    __name__,
    url_prefix="/categorias"
)

from app.categorias import routes