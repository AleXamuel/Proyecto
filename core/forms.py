from django import forms
from django import forms
from .models import *

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            "nombre", "apellido", "username", "contrasena",
            "correo", "telefono", "direccion", "fecha_registro"
        ]


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["id_persona", "estado"]


class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ["id_persona", "cargo"]


class ViniloForm(forms.ModelForm):
    class Meta:
        model = Vinilo
        fields = ["id_usuario", "nombre", "precio", "imagen_caratula", "descripcion"]


class CancionForm(forms.ModelForm):
    class Meta:
        model = Cancion
        fields = [
            "id_admin", "nombre", "artista", "precio",
            "duracion", "memoria", "calidad"
        ]


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["id_usuario", "votos"]


class ContenidoPlaylistForm(forms.ModelForm):
    class Meta:
        model = ContenidoPlaylist
        fields = ["id_lista", "id_cancion"]


class ContenidoVinilosForm(forms.ModelForm):
    class Meta:
        model = ContenidoVinilos
        fields = ["id_vinilo", "id_cancion"]


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ["id_usuario", "fecha", "total"]


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ["id_compra", "calificacion", "comentario"]


class CompraViniloForm(forms.ModelForm):
    class Meta:
        model = CompraVinilo
        fields = ["id_compra", "id_vinilo"]


class CompraCancionForm(forms.ModelForm):
    class Meta:
        model = CompraCancion
        fields = ["id_compra", "id_cancion"]


class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = ["id_usuario"]


class CarritoCancionForm(forms.ModelForm):
    class Meta:
        model = CarritoCancion
        fields = ["id_carrito", "id_cancion"]


class CarritoViniloForm(forms.ModelForm):
    class Meta:
        model = CarritoVinilo
        fields = ["id_carrito", "id_vinilo"]
