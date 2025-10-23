from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_contenido_playlist = Blueprint("contenido_playlist", __name__, url_prefix="/api/contenido_playlist")

@bp_contenido_playlist.post("")
def create_contenido_playlist():
    data = request.get_json() or {}
    required = ["id_lista", "id_cancion"]
    if not all(k in data for k in required):
        return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400

    cp = ContenidoPlaylist(**data)
    db.session.add(cp)
    db.session.commit()
    return jsonify(cp.to_dict()), 201

@bp_contenido_playlist.get("")
def list_contenido_playlists():
    return jsonify([cp.to_dict() for cp in ContenidoPlaylist.query.all()])

@bp_contenido_playlist.get("/<int:id_contenido_playlist>")
def get_contenido_playlist(id_contenido_playlist):
    return jsonify(ContenidoPlaylist.query.get_or_404(id_contenido_playlist).to_dict())

@bp_contenido_playlist.delete("/<int:id_contenido_playlist>")
def delete_contenido_playlist(id_contenido_playlist):
    cp = ContenidoPlaylist.query.get_or_404(id_contenido_playlist)
    db.session.delete(cp)
    db.session.commit()
    return jsonify(ok=True)
@bp_contenido_playlist.delete("/remove/<int:id_lista>/<int:id_cancion>")
def remove_cancion_from_playlist(id_lista, id_cancion):
        cp = ContenidoPlaylist.query.filter_by(id_lista=id_lista, id_cancion=id_cancion).first()
        if not cp:
            return jsonify(error="Canción no encontrada en la playlist"), 404
        db.session.delete(cp)
        db.session.commit()
        return jsonify(ok=True)


