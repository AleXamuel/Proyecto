from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_cancion = Blueprint("cancion", __name__, url_prefix="/api/cancion")

#post canciones con .get from or

@bp_cancion.post("")
def create_cancion():
    data = request.get_json() or {}

    # Si es una lista, procesamos varias canciones
    if isinstance(data, list):
        canciones_creadas = []
        for item in data:
            required = ["id_admin", "nombre", "artista", "precio", "duracion", "memoria", "calidad"]
            if not all(k in item for k in required):
                return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400

            c = Cancion(**item)
            db.session.add(c)
            canciones_creadas.append(c)

        db.session.commit()
        return jsonify([c.to_dict() for c in canciones_creadas]), 201

    # Si es un solo diccionario, procesamos una canción
    else:
        required = ["id_admin", "nombre", "artista", "precio", "duracion", "memoria", "calidad"]
        if not all(k in data for k in required):
            return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400

        c = Cancion(**data)
        db.session.add(c)
        db.session.commit()
        return jsonify(c.to_dict()), 201


@bp_cancion.get("")
def list_canciones():
    return jsonify([c.to_dict() for c in Cancion.query.all()])

@bp_cancion.get("/<int:id_cancion>")
def get_cancion(id_cancion):
    return jsonify(Cancion.query.get_or_404(id_cancion).to_dict())

#Update cancion 
@bp_cancion.patch("/<int:id_cancion>")
def update_cancion(id_cancion):
    c = Cancion.query.get_or_404(id_cancion)
    for k, v in request.get_json().items():
        if hasattr(c, k):
            setattr(c, k, v)
    db.session.commit()
    return jsonify(c.to_dict())

@bp_cancion.delete("/<int:id_cancion>")
def delete_cancion(id_cancion):
    c = Cancion.query.get_or_404(id_cancion)
    db.session.delete(c)
    db.session.commit()
    return jsonify(ok=True)
