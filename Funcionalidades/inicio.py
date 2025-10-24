from flask import Blueprint, request, jsonify
from models import *
from db import db
from Servicios.create import *
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

@bp_inicio.post("/registrar/usuario")
def register_usuario():
    data = request.get_json() or {}
    # Crear nueva persona
    error_response, status, new_persona = crear_persona(data)
    if error_response:
        return error_response, status
    # Crear el usuario asociado
    new_usuario = crear_usuario(data, new_persona)
    return jsonify({
        "mensaje": "Registro exitoso",
        "id_persona": new_persona.id_persona,
        "id_usuario": new_usuario.id_usuario
    }), 201

@bp_inicio.post("/registrar/admin")
def register_admin():
    data = request.get_json() or {}
    # Crear nueva persona
    error_response, status, new_persona = crear_persona(data)
    if error_response:
        return error_response, status
    # Crear el usuario asociado
    new_admin = crear_admin(data, new_persona)
    return jsonify({
        "mensaje": "Registro exitoso",
        "id_persona": new_persona.id_persona,
        "id_admin": new_admin.id_admin
    }), 201