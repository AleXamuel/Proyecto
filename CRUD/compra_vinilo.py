from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_compra_vinilo = Blueprint("compra_vinilo", __name__, url_prefix="/api/compra_vinilo")


@bp_compra_vinilo.post("")
def create_compra_vinilo():
    data = request.get_json() or {}
    required = ["id_compra", "id_vinilo"]
    if not all(k in data for k in required):
        return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400

    cv = CompraVinilo(**data)
    db.session.add(cv)
    db.session.commit()
    return jsonify(cv.to_dict()), 201

@bp_compra_vinilo.get("")
def list_compras_vinilos():
    return jsonify([cv.to_dict() for cv in CompraVinilo.query.all()])

@bp_compra_vinilo.get("/<int:id_compra_vinilo>")
def get_compra_vinilo(id_compra_vinilo):
    return jsonify(CompraVinilo.query.get_or_404(id_compra_vinilo).to_dict())

@bp_compra_vinilo.delete("/<int:id_compra_vinilo>")
def delete_compra_vinilo(id_compra_vinilo):
    cv = CompraVinilo.query.get_or_404(id_compra_vinilo)
    db.session.delete(cv)
    db.session.commit()
    return jsonify(ok=True)