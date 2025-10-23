from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_admin = Blueprint("admin", __name__, url_prefix="/api/admin")


@bp_admin.post("")
def create_admin():
    data = request.get_json() or {}
    if not data.get("id_persona") or not data.get("cargo"):
        return jsonify(error="Campos 'id_persona' y 'cargo' requeridos"), 400
    a = Administrador(**data)
    db.session.add(a)
    db.session.commit()
    return jsonify(a.to_dict()), 201

@bp_admin.get("")
def list_admins():
    return jsonify([a.to_dict() for a in Administrador.query.all()])

@bp_admin.get("/<int:id_admin>")
def get_admin(id_admin):
    return jsonify(Administrador.query.get_or_404(id_admin).to_dict())

@bp_admin.patch("/<int:id_admin>")
def update_admin(id_admin):
    a = Administrador.query.get_or_404(id_admin)
    for k, v in request.get_json().items():
        if hasattr(a, k):
            setattr(a, k, v)
    db.session.commit()
    return jsonify(a.to_dict())

@bp_admin.delete("/<int:id_admin>")
def delete_admin(id_admin):
    a = Administrador.query.get_or_404(id_admin)
    db.session.delete(a)
    db.session.commit()
    return jsonify(ok=True)
