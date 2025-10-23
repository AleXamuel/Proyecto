from flask import Flask, request, jsonify
from flask_migrate import Migrate
from db import db
from models import (
    Persona, Usuario, Administrador,
    Cancion, Vinilo, Playlist,
    Compra, Resena, ContenidoPlaylist,
    ContenidoVinilos, CompraVinilo, CompraCancion
)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Desarrollo2.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    @app.get("/api/health")
    def health():
        return {"ok": True, "message": "API de Tienda Musical activa 🎵"}

    # Persona
    # usarios
    # admin
    # canciones 
    # vinilos
    #playlist

    
   

    #reseñas

    # -------------------------------
    # COMPRAS
    # -------------------------------

    # -------------------------------
    # COMPRA VINILOS
    # -------------------------------


    # -------------------------------
    # COMPRA CANCIONES
    # -------------------------------


    # -------------------------------
    # CONTENIDO PLAYLIST
    # -------------------------------
    # -------------------------------
    # CONTENIDO VINILOS
    # -------------------------------
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
