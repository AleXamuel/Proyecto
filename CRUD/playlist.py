from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_playlist = Blueprint("playlist", __name__, url_prefix="/api/playlist")


@bp_playlist.post("")
def create_playlist():
    data = request.get_json() or {}
    if not data.get("id_usuario"):
        return jsonify(error="Campo 'id_usuario' requerido"), 400
    p = Playlist(id_usuario=data["id_usuario"], votos=data.get("votos", 0))
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

@bp_playlist.get("")
def list_playlists():
    return jsonify([p.to_dict() for p in Playlist.query.all()])

@bp_playlist.get("/<int:id_lista>")
def get_playlist(id_lista):
    pl = Playlist.query.get_or_404(id_lista)
    canciones = [c.to_dict() for c in ContenidoPlaylist.query.filter_by(id_lista=id_lista).all()]
    return jsonify({"playlist": pl.to_dict(), "canciones": canciones})

@bp_playlist.patch("/<int:id_lista>")
def update_playlist(id_lista):
    pl = Playlist.query.get_or_404(id_lista)
    data = request.get_json() or {}
    for k, v in data.items():
        if hasattr(pl, k):
            setattr(pl, k, v)
    db.session.commit()
    return jsonify(pl.to_dict())
@bp_playlist.delete("/<int:id_lista>")
def delete_playlist(id_lista):
    pl = Playlist.query.get_or_404(id_lista)
    db.session.delete(pl)
    db.session.commit()
    return jsonify(ok=True)