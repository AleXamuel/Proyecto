from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_contenido_vinilo = Blueprint("contenido_vinilo", __name__, url_prefix="/api/contenido_vinilo")

@bp_contenido_vinilo.post("")
def create_contenido_vinilo():
    data = request.get_json() or {}
    required = ["id_vinilo", "id_cancion"]
    if not all(k in data for k in required):
        return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400

    cv = ContenidoVinilos(**data)
    db.session.add(cv)
    db.session.commit()
    return jsonify(cv.to_dict()), 201

@bp_contenido_vinilo.get("")
def list_contenido_vinilos():
    return jsonify([cv.to_dict() for cv in ContenidoVinilos.query.all()])

@bp_contenido_vinilo.get("/<int:id_contenido_playlist>")
def get_contenido_vinilo(id_contenido_playlist):
    return jsonify(ContenidoVinilos.query.get_or_404(id_contenido_playlist).to_dict())

@bp_contenido_vinilo.delete("/<int:id_contenido_playlist>")
def delete_contenido_vinilo(id_contenido_playlist):
    cv = ContenidoVinilos.query.get_or_404(id_contenido_playlist)
    db.session.delete(cv)
    db.session.commit()
    return jsonify(ok=True)
@bp_contenido_vinilo.delete("/remove/<int:id_lista>/<int:id_cancion>")
def remove_cancion_from_playlist(id_vinilo, id_cancion):
        cp = ContenidoVinilos.query.filter_by(id_vinilo=id_vinilo, id_cancion=id_cancion).first()
        if not cp:
            return jsonify(error="Canción no encontrada en la playlist"), 404
        db.session.delete(cp)
        db.session.commit()
        return jsonify(ok=True)
    
