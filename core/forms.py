from django import forms
from django import forms
from .models import *

#Add CRUD ModelForms for main entities
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
        fields = ["persona", "estado"]


class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ["persona", "cargo"]

class ViniloForm(forms.ModelForm):
    canciones = forms.ModelMultipleChoiceField(
        queryset=Cancion.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False
    )

    class Meta:
        model = Vinilo
        fields = ['nombre', 'precio', 'caratula', 'descripcion', 'canciones']




class CancionForm(forms.ModelForm):
    class Meta:
        model = Cancion
        fields = ["nombre", "artista", "precio", "duracion","genero", "caratula"]
        labels = {
            "duracion": "Duración (segundos)",
        }



class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["usuario", "votos"]


class ContenidoPlaylistForm(forms.ModelForm):
    class Meta:
        model = ContenidoPlaylist
        fields = ["playlist", "cancion"]


class ContenidoVinilosForm(forms.ModelForm):
    class Meta:
        model = ContenidoVinilos
        fields = ["vinilo", "cancion"]


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ["usuario", "fecha", "total"]


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ["compra", "calificacion", "comentario"]


class CompraViniloForm(forms.ModelForm):
    class Meta:
        model = CompraVinilo
        fields = ["compra", "vinilo"]


class CompraCancionForm(forms.ModelForm):
    class Meta:
        model = CompraCancion
        fields = ["compra", "cancion"]


class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = ["usuario"]


class CarritoCancionForm(forms.ModelForm):
    class Meta:
        model = CarritoCancion
        fields = ["carrito", "cancion"]


class CarritoViniloForm(forms.ModelForm):
    class Meta:
        model = CarritoVinilo
        fields = ["carrito", "vinilo"]
