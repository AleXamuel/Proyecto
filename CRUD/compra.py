
# Módulo: compra.py
# Descripción: Define las rutas relacionadas con la gestión de compras
# en una API construida con Flask. Incluye creación, listado, consulta,
# actualización y eliminación de compras.


from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_compra = Blueprint("compra", __name__, url_prefix="/api/compra")

# POST /api/compra
# Crear una nueva compra

@bp_compra.post("")
def create_compra():
    data = request.get_json() or {}
    if not data.get("id_usuario"):
        return jsonify(error="Campo 'id_usuario' requerido"), 400
    p = Compra(id_usuario=data["id_usuario"], fecha=data.get("fecha", None), total=data.get("total", 0.0))
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

# GET /api/compra
# Listar todas las compras


@bp_compra.get("")
def list_compras():
    return jsonify([c.to_dict() for c in Compra.query.all()])

@bp_compra.get("/<int:id_compra>")
def get_compra(id_compra):
    compra = Compra.query.get_or_404(id_compra)
    vinilos = [v.to_dict() for v in CompraVinilo.query.filter_by(id_compra=id_compra).all()]
    canciones = [c.to_dict() for c in CompraCancion.query.filter_by(id_compra=id_compra).all()]
    resenas = [r.to_dict() for r in Resena.query.filter_by(id_compra=id_compra).all()]
    return jsonify({
        "compra": compra.to_dict(),
        "vinilos": vinilos,
        "canciones": canciones,
        "resenas": resenas
    })
@bp_compra.get("/usuario/<int:id_usuario>")
def list_compras_por_usuario(id_usuario):
    compras = Compra.query.filter_by(id_usuario=id_usuario).all()
    if not compras:
        return jsonify(message="El usuario no tiene compras registradas"), 200
    return jsonify([c.to_dict() for c in compras])

@bp_compra.patch("/<int:id_compra>")
def update_compra(id_compra):
    c = Compra.query.get_or_404(id_compra)
    for k, v in request.get_json().items():
        if hasattr(c, k):
            setattr(c, k, v)
    db.session.commit()
    return jsonify(c.to_dict())

# DELETE /api/compra/<id_compra>
# Eliminar una compra

@bp_compra.delete("/<int:id_compra>")
def delete_compra(id_compra):
    c = Compra.query.get_or_404(id_compra)
    db.session.delete(c)
    db.session.commit()
    return jsonify(ok=True)

