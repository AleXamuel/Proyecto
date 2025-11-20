from flask import Blueprint, request, jsonify
from db import db
from models import *

bp_carrito = Blueprint("carrito", __name__, url_prefix="/api/carrito")

#post de carrito de compras para visualizacion
@bp_carrito.post("")
def create_carrito():
    data = request.get_json() or {}
    if not data.get("id_usuario"):
        return jsonify(error="Campo 'id_usuario' requerido"), 400
    c = Carrito(**data)
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201


@bp_carrito.get("")
def list_carritos():
    return jsonify([c.to_dict() for c in Carrito.query.all()])


@bp_carrito.get("/<int:id_carrito>")
def get_carrito(id_carrito):
    return jsonify(Carrito.query.get_or_404(id_carrito).to_dict())


@bp_carrito.patch("/<int:id_carrito>")
def update_carrito(id_carrito):
    c = Carrito.query.get_or_404(id_carrito)
    for k, v in request.get_json().items():
        if hasattr(c, k):
            setattr(c, k, v)
    db.session.commit()
    return jsonify(c.to_dict())


@bp_carrito.delete("/<int:id_carrito>")
def delete_carrito(id_carrito):
    c = Carrito.query.get_or_404(id_carrito)
    db.session.delete(c)
    db.session.commit()
    return jsonify(ok=True)

@bp_carrito.post("/canciones")
def create_carrito_cancion():
    data = request.get_json() or {}
    if not data.get("id_carrito") or not data.get("id_cancion"):
        return jsonify(error="Campos 'id_carrito' y 'id_cancion' requeridos"), 400
    cc = CarritoCancion(**data)
    db.session.add(cc)
    db.session.commit()
    return jsonify(cc.to_dict()), 201


@bp_carrito.get("/canciones")
def list_carrito_canciones():
    return jsonify([cc.to_dict() for cc in CarritoCancion.query.all()])


@bp_carrito.get("/canciones/<int:id_carrito_cancion>")
def get_carrito_cancion(id_carrito_cancion):
    return jsonify(CarritoCancion.query.get_or_404(id_carrito_cancion).to_dict())


@bp_carrito.patch("/canciones/<int:id_carrito_cancion>")
def update_carrito_cancion(id_carrito_cancion):
    cc = CarritoCancion.query.get_or_404(id_carrito_cancion)
    for k, v in request.get_json().items():
        if hasattr(cc, k):
            setattr(cc, k, v)
    db.session.commit()
    return jsonify(cc.to_dict())


@bp_carrito.delete("/canciones/<int:id_carrito_cancion>")
def delete_carrito_cancion(id_carrito_cancion):
    cc = CarritoCancion.query.get_or_404(id_carrito_cancion)
    db.session.delete(cc)
    db.session.commit()
    return jsonify(ok=True)

@bp_carrito.post("/vinilos")
def create_carrito_vinilo():
    data = request.get_json() or {}
    if not data.get("id_carrito") or not data.get("id_vinilo"):
        return jsonify(error="Campos 'id_carrito' y 'id_vinilo' requeridos"), 400
    cv = CarritoVinilo(**data)
    db.session.add(cv)
    db.session.commit()
    return jsonify(cv.to_dict()), 201


@bp_carrito.get("/vinilos")
def list_carrito_vinilos():
    return jsonify([cv.to_dict() for cv in CarritoVinilo.query.all()])


@bp_carrito.get("/vinilos/<int:id_carrito_vinilo>")
def get_carrito_vinilo(id_carrito_vinilo):
    return jsonify(CarritoVinilo.query.get_or_404(id_carrito_vinilo).to_dict())


@bp_carrito.patch("/vinilos/<int:id_carrito_vinilo>")
def update_carrito_vinilo(id_carrito_vinilo):
    cv = CarritoVinilo.query.get_or_404(id_carrito_vinilo)
    for k, v in request.get_json().items():
        if hasattr(cv, k):
            setattr(cv, k, v)
    db.session.commit()
    return jsonify(cv.to_dict())


@bp_carrito.delete("/vinilos/<int:id_carrito_vinilo>")
def delete_carrito_vinilo(id_carrito_vinilo):
    cv = CarritoVinilo.query.get_or_404(id_carrito_vinilo)
    db.session.delete(cv)
    db.session.commit()
    return jsonify(ok=True)
