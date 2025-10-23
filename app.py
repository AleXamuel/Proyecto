from flask import Flask, request, jsonify
from flask_migrate import Migrate
from db import db
from models import (
    Persona, Usuario, Administrador,
    Cancion, Vinilo, Playlist,
    Compra, Resena, ContenidoPlaylist,
    ContenidoVinilos, CompraVinilo, CompraCancion
)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Desarrollo2.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    @app.get("/api/health")
    def health():
        return {"ok": True, "message": "API de Tienda Musical activa 🎵"}

    # Persona
    @app.post("/api/personas")
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

    @app.get("/api/personas")
    def list_personas():
        items = Persona.query.all()
        return jsonify([p.to_dict() for p in items])

    @app.get("/api/personas/<int:id_persona>")
    def get_persona(id_persona):
        return jsonify(Persona.query.get_or_404(id_persona).to_dict())

    @app.patch("/api/personas/<int:id_persona>")
    def update_persona(id_persona):
        p = Persona.query.get_or_404(id_persona)
        for field, value in request.get_json().items():
            if hasattr(p, field):
                setattr(p, field, value)
        db.session.commit()
        return jsonify(p.to_dict())

    @app.delete("/api/personas/<int:id_persona>")
    def delete_persona(id_persona):
        p = Persona.query.get_or_404(id_persona)
        db.session.delete(p)
        db.session.commit()
        return jsonify(ok=True)

    # usarios
    @app.post("/api/usuarios")
    def create_usuario():
        data = request.get_json() or {}
        if not data.get("id_persona"):
            return jsonify(error="Debe especificar id_persona"), 400
        u = Usuario(id_persona=data["id_persona"], estado=data.get("estado", "Activo"))
        db.session.add(u)
        db.session.commit()
        return jsonify(u.to_dict()), 201

    @app.get("/api/usuarios")
    def list_usuarios():
        return jsonify([u.to_dict() for u in Usuario.query.all()])

    @app.get("/api/usuarios/<int:id_usuario>")
    def get_usuario(id_usuario):
     usuario = Usuario.query.get_or_404(id_usuario)
     persona = Persona.query.get(usuario.id_persona).to_dict()
     playlists = [p.to_dict() for p in Playlist.query.filter_by(id_usuario=id_usuario).all()]
     vinilos = [v.to_dict() for v in Vinilo.query.filter_by(id_usuario=id_usuario).all()]
     compras = [c.to_dict() for c in Compra.query.filter_by(id_usuario=id_usuario).all()]
     return jsonify({
        "usuario": usuario.to_dict(),
        "persona": persona,
        "playlists": playlists,
        "vinilos": vinilos,
        "compras": compras
    })

    @app.patch("/api/usuarios/<int:id_usuario>")
    def update_usuario(id_usuario):
        u = Usuario.query.get_or_404(id_usuario)
        data = request.get_json() or {}
        for k in ["estado", "id_persona"]:
            if k in data:
                setattr(u, k, data[k])
        db.session.commit()
        return jsonify(u.to_dict())

    @app.delete("/api/usuarios/<int:id_usuario>")
    def delete_usuario(id_usuario):
        u = Usuario.query.get_or_404(id_usuario)
        db.session.delete(u)
        db.session.commit()
        return jsonify(ok=True)

    # admin
    @app.post("/api/admins")
    def create_admin():
        data = request.get_json() or {}
        if not data.get("id_persona") or not data.get("cargo"):
            return jsonify(error="Campos 'id_persona' y 'cargo' requeridos"), 400
        a = Administrador(**data)
        db.session.add(a)
        db.session.commit()
        return jsonify(a.to_dict()), 201

    @app.get("/api/admins")
    def list_admins():
        return jsonify([a.to_dict() for a in Administrador.query.all()])

    @app.get("/api/admins/<int:id_admin>")
    def get_admin(id_admin):
        return jsonify(Administrador.query.get_or_404(id_admin).to_dict())

    @app.patch("/api/admins/<int:id_admin>")
    def update_admin(id_admin):
        a = Administrador.query.get_or_404(id_admin)
        for k, v in request.get_json().items():
            if hasattr(a, k):
                setattr(a, k, v)
        db.session.commit()
        return jsonify(a.to_dict())

    @app.delete("/api/admins/<int:id_admin>")
    def delete_admin(id_admin):
        a = Administrador.query.get_or_404(id_admin)
        db.session.delete(a)
        db.session.commit()
        return jsonify(ok=True)

    # canciones 
    @app.post("/api/canciones")
    def create_cancion():
        data = request.get_json() or {}
        required = ["id_admin", "nombre", "artista", "precio", "duracion", "memoria", "calidad"]
        if not all(k in data for k in required):
            return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400
        c = Cancion(**data)
        db.session.add(c)
        db.session.commit()
        return jsonify(c.to_dict()), 201

    @app.get("/api/canciones")
    def list_canciones():
        return jsonify([c.to_dict() for c in Cancion.query.all()])

    @app.get("/api/canciones/<int:id_cancion>")
    def get_cancion(id_cancion):
        return jsonify(Cancion.query.get_or_404(id_cancion).to_dict())

    @app.patch("/api/canciones/<int:id_cancion>")
    def update_cancion(id_cancion):
        c = Cancion.query.get_or_404(id_cancion)
        for k, v in request.get_json().items():
            if hasattr(c, k):
                setattr(c, k, v)
        db.session.commit()
        return jsonify(c.to_dict())

    @app.delete("/api/canciones/<int:id_cancion>")
    def delete_cancion(id_cancion):
        c = Cancion.query.get_or_404(id_cancion)
        db.session.delete(c)
        db.session.commit()
        return jsonify(ok=True)

    # vinilos
    @app.post("/api/vinilos")
    def create_vinilo():
        data = request.get_json() or {}
        if not data.get("id_usuario") or not data.get("nombre"):
            return jsonify(error="Campos 'id_usuario' y 'nombre' requeridos"), 400
        v = Vinilo(**data)
        db.session.add(v)
        db.session.commit()
        return jsonify(v.to_dict()), 201

    @app.get("/api/vinilos")
    def list_vinilos():
        return jsonify([v.to_dict() for v in Vinilo.query.all()])

    @app.get("/api/vinilos/<int:id_vinilo>")
    def get_vinilo(id_vinilo):
     vinilo = Vinilo.query.get_or_404(id_vinilo)
     canciones = [c.to_dict() for c in ContenidoVinilos.query.filter_by(id_vinilo=id_vinilo).all()]
     return jsonify({
        "vinilo": vinilo.to_dict(),
        "canciones": canciones,
    })

    @app.patch("/api/vinilos/<int:id_vinilo>")
    def update_vinilo(id_vinilo):
        v = Vinilo.query.get_or_404(id_vinilo)
        for k, v2 in request.get_json().items():
            if hasattr(v, k):
                setattr(v, k, v2)
        db.session.commit()
        return jsonify(v.to_dict())

    @app.delete("/api/vinilos/<int:id_vinilo>")
    def delete_vinilo(id_vinilo):
        v = Vinilo.query.get_or_404(id_vinilo)
        db.session.delete(v)
        db.session.commit()
        return jsonify(ok=True)

    #playlist
    @app.post("/api/playlists")
    def create_playlist():
        data = request.get_json() or {}
        if not data.get("id_usuario"):
            return jsonify(error="Campo 'id_usuario' requerido"), 400
        p = Playlist(id_usuario=data["id_usuario"], votos=data.get("votos", 0))
        db.session.add(p)
        db.session.commit()
        return jsonify(p.to_dict()), 201

    @app.get("/api/playlists")
    def list_playlists():
        return jsonify([p.to_dict() for p in Playlist.query.all()])

    @app.get("/api/playlists/<int:id_lista>")
    def get_playlist(id_lista):
        pl = Playlist.query.get_or_404(id_lista)
        canciones = [c.to_dict() for c in ContenidoPlaylist.query.filter_by(id_lista=id_lista).all()]
        return jsonify({"playlist": pl.to_dict(), "canciones": canciones})

    @app.patch("/api/playlists/<int:id_lista>")
    def update_playlist(id_lista):
        pl = Playlist.query.get_or_404(id_lista)
        data = request.get_json() or {}
        for k, v in data.items():
            if hasattr(pl, k):
                setattr(pl, k, v)
        db.session.commit()
        return jsonify(pl.to_dict())
    

    @app.delete("/api/playlists/<int:id_lista>")
    def delete_playlist(id_lista):
        pl = Playlist.query.get_or_404(id_lista)
        db.session.delete(pl)
        db.session.commit()
        return jsonify(ok=True)

    def remove_cancion_from_playlist(id_lista, id_cancion):
        cp = ContenidoPlaylist.query.filter_by(id_lista=id_lista, id_cancion=id_cancion).first()
        if not cp:
            return jsonify(error="Canción no encontrada en la playlist"), 404
        db.session.delete(cp)
        db.session.commit()
        return jsonify(ok=True)
    
   

    #reseñas
    @app.post("/api/resenas")
    def create_resena():
        data = request.get_json() or {}
        r = Resena(**data)
        db.session.add(r)
        db.session.commit()
        return jsonify(r.to_dict()), 201

    @app.get("/api/resenas")
    def list_resenas():
        return jsonify([r.to_dict() for r in Resena.query.all()])

    @app.patch("/api/resenas/<int:id_resena>")
    def update_resena(id_resena):
        r = Resena.query.get_or_404(id_resena)
        for k, v in request.get_json().items():
            if hasattr(r, k):
                setattr(r, k, v)
        db.session.commit()
        return jsonify(r.to_dict())

    @app.delete("/api/resenas/<int:id_resena>")
    def delete_resena(id_resena):
        r = Resena.query.get_or_404(id_resena)
        db.session.delete(r)
        db.session.commit()
        return jsonify(ok=True)

    # -------------------------------
    # COMPRAS
    # -------------------------------
    @app.post("/api/compras")
    def create_compra():
        data = request.get_json() or {}
        if not data.get("id_usuario"):
            return jsonify(error="Campo 'id_usuario' requerido"), 400
        p = Compra(id_usuario=data["id_usuario"], fecha=data.get("fecha", None), total=data.get("total", 0.0))
        db.session.add(p)
        db.session.commit()
        return jsonify(p.to_dict()), 201
    

  
    @app.get("/api/compras")
    def list_compras():
        return jsonify([c.to_dict() for c in Compra.query.all()])

    @app.get("/api/compras/<int:id_compra>")
    def get_compra(id_compra):
        compra = Compra.query.get_or_404(id_compra)
        vinilos = [v.to_dict() for v in CompraVinilo.query.filter_by(id_compra=id_compra).all()]
        canciones = [c.to_dict() for c in CompraCancion.query.filter_by(id_compra=id_compra).all()]
        resenas = [r.to_dict() for r in Resena.query.filter_by(id_compra=id_compra).all()]
        return jsonify({
            "compra": compra.to_dict(),
            "vinilos": vinilos,
            "canciones": canciones,
            "resenas": resenas
        })

    @app.patch("/api/compras/<int:id_compra>")
    def update_compra(id_compra):
        c = Compra.query.get_or_404(id_compra)
        for k, v in request.get_json().items():
            if hasattr(c, k):
                setattr(c, k, v)
        db.session.commit()
        return jsonify(c.to_dict())

    @app.delete("/api/compras/<int:id_compra>")
    def delete_compra(id_compra):
        c = Compra.query.get_or_404(id_compra)
        db.session.delete(c)
        db.session.commit()
        return jsonify(ok=True)


    # -------------------------------
    # COMPRA VINILOS
    # -------------------------------
    @app.post("/api/compras_vinilos")
    def create_compra_vinilo():
        data = request.get_json() or {}
        required = ["id_compra", "id_vinilo"]
        if not all(k in data for k in required):
            return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400

        cv = CompraVinilo(**data)
        db.session.add(cv)
        db.session.commit()
        return jsonify(cv.to_dict()), 201

    @app.get("/api/compras_vinilos")
    def list_compras_vinilos():
        return jsonify([cv.to_dict() for cv in CompraVinilo.query.all()])

    @app.get("/api/compras_vinilos/<int:id_compra_vinilo>")
    def get_compra_vinilo(id_compra_vinilo):
        return jsonify(CompraVinilo.query.get_or_404(id_compra_vinilo).to_dict())

    @app.delete("/api/compras_vinilos/<int:id_compra_vinilo>")
    def delete_compra_vinilo(id_compra_vinilo):
        cv = CompraVinilo.query.get_or_404(id_compra_vinilo)
        db.session.delete(cv)
        db.session.commit()
        return jsonify(ok=True)


    # -------------------------------
    # COMPRA CANCIONES
    # -------------------------------
    @app.post("/api/compras_canciones")
    def create_compra_cancion():
        data = request.get_json() or {}
        required = ["id_compra", "id_cancion"]
        if not all(k in data for k in required):
            return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400

        cc = CompraCancion(**data)
        db.session.add(cc)
        db.session.commit()
        return jsonify(cc.to_dict()), 201

    @app.get("/api/compras_canciones")
    def list_compras_canciones():
        return jsonify([cc.to_dict() for cc in CompraCancion.query.all()])

    @app.get("/api/compras_canciones/<int:id_compra_cancion>")
    def get_compra_cancion(id_compra_cancion):
        return jsonify(CompraCancion.query.get_or_404(id_compra_cancion).to_dict())

    @app.delete("/api/compras_canciones/<int:id_compra_cancion>")
    def delete_compra_cancion(id_compra_cancion):
        cc = CompraCancion.query.get_or_404(id_compra_cancion)
        db.session.delete(cc)
        db.session.commit()
        return jsonify(ok=True)


    # -------------------------------
    # CONTENIDO PLAYLIST
    # -------------------------------
    @app.post("/api/contenido_playlists")
    def create_contenido_playlist():
        data = request.get_json() or {}
        required = ["id_lista", "id_cancion"]
        if not all(k in data for k in required):
            return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400

        cp = ContenidoPlaylist(**data)
        db.session.add(cp)
        db.session.commit()
        return jsonify(cp.to_dict()), 201

    @app.get("/api/contenido_playlists")
    def list_contenido_playlists():
        return jsonify([cp.to_dict() for cp in ContenidoPlaylist.query.all()])

    @app.get("/api/contenido_playlists/<int:id_contenido_playlist>")
    def get_contenido_playlist(id_contenido_playlist):
        return jsonify(ContenidoPlaylist.query.get_or_404(id_contenido_playlist).to_dict())

    @app.delete("/api/contenido_playlists/<int:id_contenido_playlist>")
    def delete_contenido_playlist(id_contenido_playlist):
        cp = ContenidoPlaylist.query.get_or_404(id_contenido_playlist)
        db.session.delete(cp)
        db.session.commit()
        return jsonify(ok=True)


    # -------------------------------
    # CONTENIDO VINILOS
    # -------------------------------
    @app.post("/api/contenido_vinilos")
    def create_contenido_vinilo():
        data = request.get_json() or {}
        required = ["id_vinilo", "id_cancion"]
        if not all(k in data for k in required):
            return jsonify(error=f"Campos requeridos: {', '.join(required)}"), 400

        cv = ContenidoVinilos(**data)
        db.session.add(cv)
        db.session.commit()
        return jsonify(cv.to_dict()), 201

    @app.get("/api/contenido_vinilos")
    def list_contenido_vinilos():
        return jsonify([cv.to_dict() for cv in ContenidoVinilos.query.all()])

    @app.get("/api/contenido_vinilos/<int:id_contenido_playlist>")
    def get_contenido_vinilo(id_contenido_playlist):
        return jsonify(ContenidoVinilos.query.get_or_404(id_contenido_playlist).to_dict())

    @app.delete("/api/contenido_vinilos/<int:id_contenido_playlist>")
    def delete_contenido_vinilo(id_contenido_playlist):
        cv = ContenidoVinilos.query.get_or_404(id_contenido_playlist)
        db.session.delete(cv)
        db.session.commit()
        return jsonify(ok=True)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
