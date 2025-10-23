from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_vinilo = Blueprint("vinilo", __name__, url_prefix="/api/vinilo")

@bp_vinilo.post("")
def create_vinilo():
    data = request.get_json() or {}
    if not data.get("id_usuario") or not data.get("nombre"):
        return jsonify(error="Campos 'id_usuario' y 'nombre' requeridos"), 400
    v = Vinilo(**data)
    db.session.add(v)
    db.session.commit()
    return jsonify(v.to_dict()), 201

@bp_vinilo.get("")
def list_vinilos():
    return jsonify([v.to_dict() for v in Vinilo.query.all()])

@bp_vinilo.get("/<int:id_vinilo>")
def get_vinilo(id_vinilo):
    vinilo = Vinilo.query.get_or_404(id_vinilo)
    canciones = [c.to_dict() for c in ContenidoVinilos.query.filter_by(id_vinilo=id_vinilo).all()]
    return jsonify({
    "vinilo": vinilo.to_dict(),
    "canciones": canciones,
})

@bp_vinilo.patch("/<int:id_vinilo>")
def update_vinilo(id_vinilo):
    v = Vinilo.query.get_or_404(id_vinilo)
    for k, v2 in request.get_json().items():
        if hasattr(v, k):
            setattr(v, k, v2)
    db.session.commit()
    return jsonify(v.to_dict())

@bp_vinilo.delete("/<int:id_vinilo>")
def delete_vinilo(id_vinilo):
    v = Vinilo.query.get_or_404(id_vinilo)
    db.session.delete(v)
    db.session.commit()
    return jsonify(ok=True)
