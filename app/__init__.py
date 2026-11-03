
from flask import Flask, render_template
from config import Config
from app.models import db, login_manager


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Importar los Blueprints
    from app.auth import auth_bp
    from app.usuarios import usuarios_bp
    from app.categorias import categorias_bp
    from app.anuncios import anuncios_bp

    # Registrar los Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(anuncios_bp)

    # Página principal
    @app.route("/")
    def inicio():
        from app.models import Anuncio
        anuncios = Anuncio.query.order_by(
            Anuncio.fecha_publicacion.desc()
        ).all()

        return render_template(
            "inicio.html",
            anuncios=anuncios
        )

    # Crear las tablas
    with app.app_context():
        db.create_all()

    return app
