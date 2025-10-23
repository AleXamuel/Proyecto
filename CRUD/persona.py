from flask import Blueprint, request, jsonify
from db import db
from models import Persona

bp_persona = Blueprint("persona", __name__, url_prefix="/api/personas")

@bp_persona.post("")
def create_persona():
    def create_persona():
        data = request.get_json() or {}
        required = ["nombre", "apellido", "username", "contrasena", "correo"]
        if not all(k in data for k in required):
            return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400

        p = Persona(**{k: data.get(k) for k in [
            "nombre", "apellido", "username", "contrasena", "correo", "telefono", "direccion"
        ]})
        db.session.add(p)
        db.session.commit()
        return jsonify(p.to_dict()), 201
@bp_persona.get("")
def list_personas():
        items = Persona.query.all()
        return jsonify([p.to_dict() for p in items])
@bp_persona.get("/<int:id_persona>")
def get_persona(id_persona):
    persona = Persona.query.get_or_404(id_persona)
    return jsonify(persona.to_dict())
@bp_persona.patch("/<int:id_persona>")
def update_persona(id_persona):
        p = Persona.query.get_or_404(id_persona)
        for field, value in request.get_json().items():
            if hasattr(p, field):
                setattr(p, field, value)
        db.session.commit()
        return jsonify(p.to_dict())
@bp_persona.delete("/<int:id_persona>")
def delete_persona(id_persona):
        p = Persona.query.get_or_404(id_persona)
        db.session.delete(p)
        db.session.commit()
        return jsonify(ok=True)
