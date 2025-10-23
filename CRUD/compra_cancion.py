from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_compra_cancion = Blueprint("compra_cancion", __name__, url_prefix="/api/compra_cancion")


@bp_compra_cancion.post("")
def create_compra_cancion():
    data = request.get_json() or {}
    required = ["id_compra", "id_cancion"]
    if not all(k in data for k in required):
        return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400

    cc = CompraCancion(**data)
    db.session.add(cc)
    db.session.commit()
    return jsonify(cc.to_dict()), 201

@bp_compra_cancion.get("")
def list_compras_canciones():
    return jsonify([cc.to_dict() for cc in CompraCancion.query.all()])

@bp_compra_cancion.get("/<int:id_compra_cancion>")
def get_compra_cancion(id_compra_cancion):
    return jsonify(CompraCancion.query.get_or_404(id_compra_cancion).to_dict())

@bp_compra_cancion.delete("/<int:id_compra_cancion>")
def delete_compra_cancion(id_compra_cancion):
    cc = CompraCancion.query.get_or_404(id_compra_cancion)
    db.session.delete(cc)
    db.session.commit()
    return jsonify(ok=True)