from flask import Flask
from flask_migrate import Migrate
from db import db
from CRUD.persona import bp_persona
from CRUD.usuario import bp_usuario
from CRUD.admin import bp_admin
from CRUD.cancion import bp_cancion
from CRUD.vinilo import bp_vinilo
from CRUD.playlist import bp_playlist
from CRUD.compra import bp_compra
from CRUD.resena import bp_resena
from CRUD.compra_cancion import bp_compra_cancion
from CRUD.compra_vinilo import bp_compra_vinilo
from CRUD.contenido_playlist import bp_contenido_playlist
from CRUD.contenido_vinilo import bp_contenido_vinilo

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Desarrollo2.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    # Registrar todos los blueprints
    app.register_blueprint(bp_persona)
    app.register_blueprint(bp_usuario)
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_cancion)
    app.register_blueprint(bp_vinilo)
    app.register_blueprint(bp_playlist)
    app.register_blueprint(bp_compra)
    app.register_blueprint(bp_resena)
    app.register_blueprint(bp_compra_cancion)
    app.register_blueprint(bp_compra_vinilo)
    app.register_blueprint(bp_contenido_playlist)
    app.register_blueprint(bp_contenido_vinilo)
    @app.get("/api/health")
    def health():
        return {"ok": True, "message": "API REST en funcionamiento ✅"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
