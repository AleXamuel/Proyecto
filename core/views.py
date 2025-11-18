from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .models import *
from .forms import *


def crud_list(request, Model, template, ctx_name):
    qs = Model.objects.all()
    return render(request, template, {ctx_name: qs})

def crud_detail(request, pk, Model, template, ctx_name):
    obj = get_object_or_404(Model, pk=pk)
    return render(request, template, {ctx_name: obj})

@require_http_methods(["GET", "POST"])
def crud_create(request, Form, template, redirect_name):
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect(redirect_name, pk=obj.pk)
    else:
        form = Form()
    return render(request, template, {"form": form, "mode": "create"})

@require_http_methods(["GET", "POST"])
def crud_update(request, pk, Model, Form, template, redirect_name, ctx_name):
    obj = get_object_or_404(Model, pk=pk)
    if request.method == "POST":
        form = Form(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            return redirect(redirect_name, pk=obj.pk)
    else:
        form = Form(instance=obj)
    return render(request, template, {"form": form, "mode": "edit", ctx_name: obj})

@require_http_methods(["POST", "GET"])
def crud_delete(request, pk, Model, template, redirect_name, ctx_name):
    obj = get_object_or_404(Model, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect(redirect_name)
    return render(request, template, {ctx_name: obj})

# PERSONA
def persona_list(request):
    return crud_list(request, Persona, "persona/list.html", "personas")

def persona_detail(request, pk):
    return crud_detail(request, pk, Persona, "persona/detail.html", "persona")

def persona_create(request):
    return crud_create(request, PersonaForm, "persona/form.html", "persona_detail")

def persona_update(request, pk):
    return crud_update(request, pk, Persona, PersonaForm, "persona/form.html", "persona_detail", "persona")

def persona_delete(request, pk):
    return crud_delete(request, pk, Persona, "persona/delete.html", "persona_list", "persona")


# USUARIO
def usuario_list(request):
    return crud_list(request, Usuario, "usuario/list.html", "usuarios")

def usuario_detail(request, pk):
    return crud_detail(request, pk, Usuario, "usuario/detail.html", "usuario")

def usuario_create(request):
    return crud_create(request, UsuarioForm, "usuario/form.html", "usuario_detail")

def usuario_update(request, pk):
    return crud_update(request, pk, Usuario, UsuarioForm, "usuario/form.html", "usuario_detail", "usuario")

def usuario_delete(request, pk):
    return crud_delete(request, pk, Usuario, "usuario/delete.html", "usuario_list", "usuario")


# ADMINISTRADOR
def admin_list(request):
    return crud_list(request, Administrador, "admin/list.html", "admins")

def admin_detail(request, pk):
    return crud_detail(request, pk, Administrador, "admin/detail.html", "admin")

def admin_create(request):
    return crud_create(request, AdministradorForm, "admin/form.html", "admin_detail")

def admin_update(request, pk):
    return crud_update(request, pk, Administrador, AdministradorForm, "admin/form.html", "admin_detail", "admin")

def admin_delete(request, pk):
    return crud_delete(request, pk, Administrador, "admin/delete.html", "admin_list", "admin")


# VINILO
def vinilo_list(request):
    return crud_list(request, Vinilo, "vinilo/list.html", "vinilos")

def vinilo_detail(request, pk):
    return crud_detail(request, pk, Vinilo, "vinilo/detail.html", "vinilo")

def vinilo_create(request):
    return crud_create(request, ViniloForm, "vinilo/form.html", "vinilo_detail")

def vinilo_update(request, pk):
    return crud_update(request, pk, Vinilo, ViniloForm, "vinilo/form.html", "vinilo_detail", "vinilo")

def vinilo_delete(request, pk):
    return crud_delete(request, pk, Vinilo, "vinilo/delete.html", "vinilo_list", "vinilo")


# CANCION
def cancion_list(request):
    return crud_list(request, Cancion, "cancion/list.html", "canciones")

def cancion_detail(request, pk):
    return crud_detail(request, pk, Cancion, "cancion/detail.html", "cancion")

def cancion_create(request):
    return crud_create(request, CancionForm, "cancion/form.html", "cancion_detail")

def cancion_update(request, pk):
    return crud_update(request, pk, Cancion, CancionForm, "cancion/form.html", "cancion_detail", "cancion")

def cancion_delete(request, pk):
    return crud_delete(request, pk, Cancion, "cancion/delete.html", "cancion_list", "cancion")


# PLAYLIST
def playlist_list(request):
    return crud_list(request, Playlist, "playlist/list.html", "playlists")

def playlist_detail(request, pk):
    return crud_detail(request, pk, Playlist, "playlist/detail.html", "playlist")

def playlist_create(request):
    return crud_create(request, PlaylistForm, "playlist/form.html", "playlist_detail")

def playlist_update(request, pk):
    return crud_update(request, pk, Playlist, PlaylistForm, "playlist/form.html", "playlist_detail", "playlist")

def playlist_delete(request, pk):
    return crud_delete(request, pk, Playlist, "playlist/delete.html", "playlist_list", "playlist")


# CONTENIDO PLAYLIST
def contenido_playlist_list(request):
    return crud_list(request, ContenidoPlaylist, "contenido_playlist/list.html", "contenidos_playlist")

def contenido_playlist_detail(request, pk):
    return crud_detail(request, pk, ContenidoPlaylist, "contenido_playlist/detail.html", "contenido_playlist")

def contenido_playlist_create(request):
    return crud_create(request, ContenidoPlaylistForm, "contenido_playlist/form.html", "contenido_playlist_detail")

def contenido_playlist_update(request, pk):
    return crud_update(request, pk, ContenidoPlaylist, ContenidoPlaylistForm, "contenido_playlist/form.html", "contenido_playlist_detail", "contenido_playlist")

def contenido_playlist_delete(request, pk):
    return crud_delete(request, pk, ContenidoPlaylist, "contenido_playlist/delete.html", "contenido_playlist_list", "contenido_playlist")


# CONTENIDO VINILOS
def contenido_vinilos_list(request):
    return crud_list(request, ContenidoVinilos, "contenido_vinilos/list.html", "contenidos_vinilos")

def contenido_vinilos_detail(request, pk):
    return crud_detail(request, pk, ContenidoVinilos, "contenido_vinilos/detail.html", "contenido_vinilos")

def contenido_vinilos_create(request):
    return crud_create(request, ContenidoVinilosForm, "contenido_vinilos/form.html", "contenido_vinilos_detail")

def contenido_vinilos_update(request, pk):
    return crud_update(request, pk, ContenidoVinilos, ContenidoVinilosForm, "contenido_vinilos/form.html", "contenido_vinilos_detail", "contenido_vinilos")

def contenido_vinilos_delete(request, pk):
    return crud_delete(request, pk, ContenidoVinilos, "contenido_vinilos/delete.html", "contenido_vinilos_list", "contenido_vinilos")


# COMPRA
def compra_list(request):
    return crud_list(request, Compra, "compra/list.html", "compras")

def compra_detail(request, pk):
    return crud_detail(request, pk, Compra, "compra/detail.html", "compra")

def compra_create(request):
    return crud_create(request, CompraForm, "compra/form.html", "compra_detail")

def compra_update(request, pk):
    return crud_update(request, pk, Compra, CompraForm, "compra/form.html", "compra_detail", "compra")

def compra_delete(request, pk):
    return crud_delete(request, pk, Compra, "compra/delete.html", "compra_list", "compra")


# RESENA
def resena_list(request):
    return crud_list(request, Resena, "resena/list.html", "resenas")

def resena_detail(request, pk):
    return crud_detail(request, pk, Resena, "resena/detail.html", "resena")

def resena_create(request):
    return crud_create(request, ResenaForm, "resena/form.html", "resena_detail")

def resena_update(request, pk):
    return crud_update(request, pk, Resena, ResenaForm, "resena/form.html", "resena_detail", "resena")

def resena_delete(request, pk):
    return crud_delete(request, pk, Resena, "resena/delete.html", "resena_list", "resena")


# COMPRA VINILO
def compra_vinilo_list(request):
    return crud_list(request, CompraVinilo, "compra_vinilo/list.html", "compra_vinilos")

def compra_vinilo_detail(request, pk):
    return crud_detail(request, pk, CompraVinilo, "compra_vinilo/detail.html", "compra_vinilo")

def compra_vinilo_create(request):
    return crud_create(request, CompraViniloForm, "compra_vinilo/form.html", "compra_vinilo_detail")

def compra_vinilo_update(request, pk):
    return crud_update(request, pk, CompraVinilo, CompraViniloForm, "compra_vinilo/form.html", "compra_vinilo_detail", "compra_vinilo")

def compra_vinilo_delete(request, pk):
    return crud_delete(request, pk, CompraVinilo, "compra_vinilo/delete.html", "compra_vinilo_list", "compra_vinilo")


# COMPRA CANCION
def compra_cancion_list(request):
    return crud_list(request, CompraCancion, "compra_cancion/list.html", "compra_canciones")

def compra_cancion_detail(request, pk):
    return crud_detail(request, pk, CompraCancion, "compra_cancion/detail.html", "compra_cancion")

def compra_cancion_create(request):
    return crud_create(request, CompraCancionForm, "compra_cancion/form.html", "compra_cancion_detail")

def compra_cancion_update(request, pk):
    return crud_update(request, pk, CompraCancion, CompraCancionForm, "compra_cancion/form.html", "compra_cancion_detail", "compra_cancion")

def compra_cancion_delete(request, pk):
    return crud_delete(request, pk, CompraCancion, "compra_cancion/delete.html", "compra_cancion_list", "compra_cancion")


# CARRITO
def carrito_list(request):
    return crud_list(request, Carrito, "carrito/list.html", "carritos")

def carrito_detail(request, pk):
    return crud_detail(request, pk, Carrito, "carrito/detail.html", "carrito")

def carrito_create(request):
    return crud_create(request, CarritoForm, "carrito/form.html", "carrito_detail")

def carrito_update(request, pk):
    return crud_update(request, pk, Carrito, CarritoForm, "carrito/form.html", "carrito_detail", "carrito")

def carrito_delete(request, pk):
    return crud_delete(request, pk, Carrito, "carrito/delete.html", "carrito_list", "carrito")


# CARRITO CANCION
def carrito_cancion_list(request):
    return crud_list(request, CarritoCancion, "carrito_cancion/list.html", "carrito_canciones")

def carrito_cancion_detail(request, pk):
    return crud_detail(request, pk, CarritoCancion, "carrito_cancion/detail.html", "carrito_cancion")

def carrito_cancion_create(request):
    return crud_create(request, CarritoCancionForm, "carrito_cancion/form.html", "carrito_cancion_detail")

def carrito_cancion_update(request, pk):
    return crud_update(request, pk, CarritoCancion, CarritoCancionForm, "carrito_cancion/form.html", "carrito_cancion_detail", "carrito_cancion")

def carrito_cancion_delete(request, pk):
    return crud_delete(request, pk, CarritoCancion, "carrito_cancion/delete.html", "carrito_cancion_list", "carrito_cancion")


# CARRITO VINILO
def carrito_vinilo_list(request):
    return crud_list(request, CarritoVinilo, "carrito_vinilo/list.html", "carrito_vinilos")

def carrito_vinilo_detail(request, pk):
    return crud_detail(request, pk, CarritoVinilo, "carrito_vinilo/detail.html", "carrito_vinilo")

def carrito_vinilo_create(request):
    return crud_create(request, CarritoViniloForm, "carrito_vinilo/form.html", "carrito_vinilo_detail")

def carrito_vinilo_update(request, pk):
    return crud_update(request, pk, CarritoVinilo, CarritoViniloForm, "carrito_vinilo/form.html", "carrito_vinilo_detail", "carrito_vinilo")

def carrito_vinilo_delete(request, pk):
    return crud_delete(request, pk, CarritoVinilo, "carrito_vinilo/delete.html", "carrito_vinilo_list", "carrito_vinilo")


