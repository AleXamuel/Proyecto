from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_resena = Blueprint("resena", __name__, url_prefix="/api/resena")

#Sirve para registrar una nueva reseña en la base de datos cuando un usuario evalúa un producto o compra.
#¿Qué hace?
#- Recibe los datos de la reseña en formato JSON.
#- Crea un objeto Resena.
#- Lo guarda en la base de datos.

@bp_resena.post("")
def create_resena():
    data = request.get_json() or {}
    r = Resena(**data)
    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict()), 201

#¿Para qué sirve?
#Sirve para ver todas las reseñas que existen en el sistema.
#¿Qué hace?
#Consulta la tabla de reseñas.
#Devuelve la lista completa en formato JSON.

@bp_resena.get("")
def list_resenas():
    return jsonify([r.to_dict() for r in Resena.query.all()])

@bp_resena.patch("/<int:id_resena>")
def update_resena(id_resena):
    r = Resena.query.get_or_404(id_resena)
    for k, v in request.get_json().items():
        if hasattr(r, k):
            setattr(r, k, v)
    db.session.commit()
    return jsonify(r.to_dict())

@bp_resena.get("/usuario/<int:id_usuario>")
def list_resenas_por_usuario(id_usuario):
    compras = Compra.query.filter_by(id_usuario=id_usuario).all()
    if not compras:
        return jsonify(error="No se encontraron compras para este usuario"), 404
    ids_compras = [c.id_compra for c in compras]
    resenas = Resena.query.filter(Resena.id_compra.in_(ids_compras)).all()
    if not resenas:
        return jsonify(message="El usuario no tiene reseñas aún"), 200
    return jsonify([r.to_dict() for r in resenas])

@bp_resena.delete("/<int:id_resena>")
def delete_resena(id_resena):
    r = Resena.query.get_or_404(id_resena)
    db.session.delete(r)
    db.session.commit()
    return jsonify(ok=True)

