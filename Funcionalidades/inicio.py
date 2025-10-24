from flask import Blueprint, request, jsonify
from models import *
from db import db
bp_inicio = Blueprint("incio", __name__, url_prefix="/api/inicio")

@bp_inicio.post("/login")
def login():
    data = request.get_json() or {}
    # Validar campos requeridos
    if not data.get("username") or not data.get("password"):
        return jsonify(error="Campos 'username' y 'password' requeridos"), 400
    username = data.get("username")
    password = data.get("password")
    # Buscar usuario
    user = Persona.query.filter_by(username=username).first()
    if not user:
        return jsonify(error="Usuario no encontrado"), 404

    # Verificar contraseña
    if user.contrasena == password:
        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "user_id": user.id_persona,
            "nombre": user.nombre
        }), 200
    else:
        return jsonify(error="Contraseña incorrecta"), 401
