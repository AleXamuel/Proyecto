from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_usuario = Blueprint("usuario", __name__, url_prefix="/api/usuario")
@bp_usuario.post("")
def create_usuario():
    data = request.get_json() or {}
    if not data.get("id_persona"):
        return jsonify(error="Debe especificar id_persona"), 400
    u = Usuario(id_persona=data["id_persona"], estado=data.get("estado", "Activo"))
    db.session.add(u)
    db.session.commit()
    return jsonify(u.to_dict()), 201

@bp_usuario.get("")
def list_usuarios():
    return jsonify([u.to_dict() for u in Usuario.query.all()])

@bp_usuario.get("/<int:id_usuario>")
def get_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    persona = Persona.query.get(usuario.id_persona).to_dict()
    playlists = [p.to_dict() for p in Playlist.query.filter_by(id_usuario=id_usuario).all()]
    vinilos = [v.to_dict() for v in Vinilo.query.filter_by(id_usuario=id_usuario).all()]
    compras = [c.to_dict() for c in Compra.query.filter_by(id_usuario=id_usuario).all()]
    return jsonify({
    "usuario": usuario.to_dict(),
    "persona": persona,
    "playlists": playlists if playlists else "Sin playlists",
    "vinilos": vinilos if vinilos else "Sin vinilos",
    "compras": compras if compras else "Sin compras"
    })


@bp_usuario.patch("/<int:id_usuario>")
def update_usuario(id_usuario):
    u = Usuario.query.get_or_404(id_usuario)
    data = request.get_json() or {}
    for k in ["estado", "id_persona"]:
        if k in data:
            setattr(u, k, data[k])
    db.session.commit()
    return jsonify(u.to_dict())

@bp_usuario.delete("/<int:id_usuario>")
def delete_usuario(id_usuario):
    u = Usuario.query.get_or_404(id_usuario)
    db.session.delete(u)
    db.session.commit()
    return jsonify(ok=True)

