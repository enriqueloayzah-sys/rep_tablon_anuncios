from flask import Blueprint

anuncios_bp = Blueprint(
    "anuncios",
    __name__,
    url_prefix="/anuncios"
)

from app.anuncios import routes