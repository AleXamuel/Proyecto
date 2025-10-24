from db import db
from models import *
from flask import jsonify

def crear_persona(data):
    required_fields = ["nombre", "apellido", "username", "contrasena", "correo", "telefono"]
    # Validar campos requeridos
    for field in required_fields:
        if not data.get(field):
            return jsonify(error=f"Campo '{field}' requerido"), 400,None
    # Validar correo y username únicos
    if Persona.query.filter_by(correo=data["correo"]).first():
        return jsonify(error="Correo ya registrado"), 409,None
    if Persona.query.filter_by(username=data["username"]).first():
        return jsonify(error="Username ya registrado"), 409,None
    persona = Persona(
        nombre=data["nombre"],
        apellido=data["apellido"],
        username=data["username"],
        contrasena=data["contrasena"],
        correo=data["correo"],
        telefono=data.get("telefono"),
        direccion=data.get("direccion")
    )
    db.session.add(persona)
    db.session.commit()
    return None, 201, persona
def crear_usuario(data,new_persona):
    new_usuario = Usuario(
        id_persona=new_persona.id_persona,
        estado=data.get("estado", "activo")  # Valor por defecto si no se envía    )
    )
    db.session.add(new_usuario)
    db.session.commit()
    return 

def crear_admin(data,new_persona):
    new_admin= Administrador(
        id_persona=new_persona.id_persona,
        cargo=data.get("estado", "Administrador")  # Valor por defecto si no se envía    )
    )
    db.session.add(new_admin)
    db.session.commit()
    return new_admin