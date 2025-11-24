from django.db import models
from django.utils import timezone


class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    contrasena = models.CharField(max_length=100)
    correo = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    fecha_registro = models.CharField(
        default=timezone.localdate
    )

    class Meta:
        db_table = "Persona"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="usuarios")
    estado = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "Usuario"

    def __str__(self):
        return f"Usuario {self.id_usuario}"


class Administrador(models.Model):
    id_admin = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="administradores")
    cargo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "Administrador"

    def __str__(self):
        return f"Admin {self.id_admin}"


class Vinilo(models.Model):
    id_vinilo = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="vinilos")
    nombre = models.CharField(max_length=150)
    precio = models.FloatField()
    caratula = models.ImageField(upload_to="vinilo/", null=True, blank=True)  
    descripcion = models.TextField(blank=True, null=True)
    canciones = models.ManyToManyField('Cancion', through='ContenidoVinilos')

    class Meta:
        db_table = "Vinilo"

    def __str__(self):
        return self.nombre

class Cancion(models.Model):
    id_cancion = models.AutoField(primary_key=True)
    admin = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name="canciones")
    nombre = models.CharField(max_length=150)
    artista = models.CharField(max_length=150)
    precio = models.FloatField()
    duracion = models.IntegerField()
    genero = models.CharField(max_length=150, null=True)
    caratula = models.ImageField(upload_to="cancion/", null=True, blank=True)  

    class Meta:
        db_table = "Cancion"

    def __str__(self):
        return self.nombre



class Playlist(models.Model):
    id_lista = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="playlists")
    votos = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "Playlist"

    def __str__(self):
        return f"Playlist {self.id_lista}"


class ContenidoPlaylist(models.Model):
    id_contenido_playlist = models.AutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="contenidos")
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE, related_name="contenidos_playlist")

    class Meta:
        db_table = "ContenidoPlaylist"

    def __str__(self):
        return f"ContenidoPlaylist {self.id_contenido_playlist}"


class ContenidoVinilos(models.Model):
    vinilo = models.ForeignKey(Vinilo, on_delete=models.CASCADE, related_name="contenidos")
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE, related_name="canciones")
    class Meta:
        db_table = "ContenidoVinilos"


class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="compras")
    fecha = models.CharField(max_length=10)
    total = models.FloatField()

    class Meta:
        db_table = "Compra"

    def __str__(self):
        return f"Compra {self.id_compra}"


class Resena(models.Model):
    id_resena = models.AutoField(primary_key=True)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="resenas")
    calificacion = models.FloatField()
    comentario = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = "Resena"

    def __str__(self):
        return f"Reseña {self.id_resena}"


class CompraVinilo(models.Model):
    id_compra_vinilo = models.AutoField(primary_key=True)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="compra_vinilos")
    vinilo = models.ForeignKey(Vinilo, on_delete=models.CASCADE, related_name="compras_vinilo")

    class Meta:
        db_table = "CompraVinilo"

    def __str__(self):
        return f"CompraVinilo {self.id_compra_vinilo}"


class CompraCancion(models.Model):
    id_compra_cancion = models.AutoField(primary_key=True)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="compra_canciones")
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE, related_name="compras_cancion")

    class Meta:
        db_table = "CompraCancion"

    def __str__(self):
        return f"CompraCancion {self.id_compra_cancion}"


class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="carritos")

    class Meta:
        db_table = "Carrito"

    def __str__(self):
        return f"Carrito {self.id_carrito}" 


class CarritoCancion(models.Model):
    id_carrito_cancion = models.AutoField(primary_key=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="canciones")
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE, related_name="carritos_cancion")

    class Meta:
        db_table = "CarritoCancion"

    def __str__(self):
        return f"CarritoCancion {self.id_carrito_cancion}"


class CarritoVinilo(models.Model):
    id_carrito_vinilo = models.AutoField(primary_key=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="vinilos")
    vinilo = models.ForeignKey(Vinilo, on_delete=models.CASCADE, related_name="carritos_vinilo")

    class Meta:
        db_table = "CarritoVinilo"

    def __str__(self):
        return f"CarritoVinilo {self.id_carrito_vinilo}"
