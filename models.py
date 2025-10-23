from db import db

class Persona(db.Model):
    __tablename__ = "Persona"
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    fecha_registro = db.Column(db.String(10))

    usuario = db.relationship("Usuario", backref="persona", cascade="all, delete-orphan")
    administrador = db.relationship("Administrador", backref="persona", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_persona": self.id_persona,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "username": self.username,
            "correo": self.correo,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "fecha_registro": str(self.fecha_registro) if self.fecha_registro else None
        }


class Usuario(db.Model):
    __tablename__ = "Usuario"
    id_usuario = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey("Persona.id_persona"))
    estado = db.Column(db.String(50))

    vinilos = db.relationship("Vinilo", backref="usuario", cascade="all, delete-orphan")
    playlists = db.relationship("Playlist", backref="usuario", cascade="all, delete-orphan")
    compras = db.relationship("Compra", backref="usuario", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "id_persona": self.id_persona,
            "estado": self.estado
        }


class Administrador(db.Model):
    __tablename__ = "Administrador"
    id_admin = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey("Persona.id_persona"))
    cargo = db.Column(db.String(100))

    canciones = db.relationship("Cancion", backref="admin", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_admin": self.id_admin,
            "id_persona": self.id_persona,
            "cargo": self.cargo
        }


class Vinilo(db.Model):
    __tablename__ = "Vinilo"
    id_vinilo = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("Usuario.id_usuario"))
    nombre = db.Column(db.String(150), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen_caratula = db.Column(db.String(255))
    descripcion = db.Column(db.Text)

    contenidos = db.relationship("ContenidoVinilos", backref="vinilo", cascade="all, delete-orphan")
    compras_vinilo = db.relationship("CompraVinilo", backref="vinilo", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_vinilo": self.id_vinilo,
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "precio": self.precio,
            "imagen_caratula": self.imagen_caratula,
            "descripcion": self.descripcion
        }


class Cancion(db.Model):
    __tablename__ = "Cancion"
    id_cancion = db.Column(db.Integer, primary_key=True)
    id_admin = db.Column(db.Integer, db.ForeignKey("Administrador.id_admin"))
    nombre = db.Column(db.String(150), nullable=False)
    artista = db.Column(db.String(150), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    memoria = db.Column(db.Float, nullable=False)
    calidad = db.Column(db.String(50), nullable=False)

    contenidos_playlist = db.relationship("ContenidoPlaylist", backref="cancion", cascade="all, delete-orphan")
    contenidos_vinilos = db.relationship("ContenidoVinilos", backref="cancion", cascade="all, delete-orphan")
    compras_cancion = db.relationship("CompraCancion", backref="cancion", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_cancion": self.id_cancion,
            "id_admin": self.id_admin,
            "nombre": self.nombre,
            "artista": self.artista,
            "precio": self.precio,
            "duracion": self.duracion,
            "memoria": self.memoria,
            "calidad": self.calidad
        }


class Playlist(db.Model):
    __tablename__ = "Playlist"
    id_lista = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("Usuario.id_usuario"))
    votos = db.Column(db.Integer)

    contenidos = db.relationship("ContenidoPlaylist", backref="playlist", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_lista": self.id_lista,
            "id_usuario": self.id_usuario,
            "votos": self.votos
        }


class ContenidoPlaylist(db.Model):
    __tablename__ = "ContenidoPlaylist"
    id_contenido_playlist = db.Column(db.Integer, primary_key=True)
    id_lista = db.Column(db.Integer, db.ForeignKey("Playlist.id_lista"))
    id_cancion = db.Column(db.Integer, db.ForeignKey("Cancion.id_cancion"))

    def to_dict(self):
        return {
            "id_contenido_playlist": self.id_contenido_playlist,
            "id_lista": self.id_lista,
            "id_cancion": self.id_cancion
        }


class ContenidoVinilos(db.Model):
    __tablename__ = "ContenidoVinilos"
    id_contenido_playlist = db.Column(db.Integer, primary_key=True)
    id_vinilo = db.Column(db.Integer, db.ForeignKey("Vinilo.id_vinilo"))
    id_cancion = db.Column(db.Integer, db.ForeignKey("Cancion.id_cancion"))

    def to_dict(self):
        return {
            "id_contenido_playlist": self.id_contenido_playlist,
            "id_vinilo": self.id_vinilo,
            "id_cancion": self.id_cancion
        }


class Compra(db.Model):
    __tablename__ = "Compra"
    id_compra = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("Usuario.id_usuario"))
    fecha = db.Column(db.String(10), nullable=False)
    total = db.Column(db.Float, nullable=False)

    vinilos = db.relationship("CompraVinilo", backref="compra", cascade="all, delete-orphan")
    canciones = db.relationship("CompraCancion", backref="compra", cascade="all, delete-orphan")
    resenas = db.relationship("Resena", backref="compra", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_compra": self.id_compra,
            "id_usuario": self.id_usuario,
            "fecha": str(self.fecha) if self.fecha else None,
            "total": self.total
        }

class Resena(db.Model):
    __tablename__ = "Resena"
    id_resena = db.Column(db.Integer, primary_key=True)
    id_compra = db.Column(db.Integer, db.ForeignKey("Compra.id_compra"))
    calificacion = db.Column(db.Float, nullable=False)
    comentario = db.Column(db.String(500))

    def to_dict(self):
        return {
            "id_resena": self.id_resena,
            "id_compra": self.id_compra,
            "calificacion": self.calificacion,
            "comentario": self.comentario
        }


class CompraVinilo(db.Model):
    __tablename__ = "CompraVinilo"
    id_compra_vinilo = db.Column(db.Integer, primary_key=True)
    id_compra = db.Column(db.Integer, db.ForeignKey("Compra.id_compra"))
    id_vinilo = db.Column(db.Integer, db.ForeignKey("Vinilo.id_vinilo"))

    def to_dict(self):
        return {
            "id_compra_vinilo": self.id_compra_vinilo,
            "id_compra": self.id_compra,
            "id_vinilo": self.id_vinilo
        }


class CompraCancion(db.Model):
    __tablename__ = "CompraCancion"
    id_compra_cancion = db.Column(db.Integer, primary_key=True)
    id_compra = db.Column(db.Integer, db.ForeignKey("Compra.id_compra"))
    id_cancion = db.Column(db.Integer, db.ForeignKey("Cancion.id_cancion"))

    def to_dict(self):
        return {
            "id_compra_cancion": self.id_compra_cancion,
            "id_compra": self.id_compra,
            "id_cancion": self.id_cancion
        }
