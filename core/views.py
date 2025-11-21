from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .models import *
from .forms import *

def home(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            persona = Persona.objects.get(username=username, contrasena=password)
            request.session["persona_id"] = persona.id_persona
            if Administrador.objects.filter(persona=persona).exists():
                admin_obj = Administrador.objects.get(persona=persona)
                request.session["admin_id"] = admin_obj.id_admin
                return redirect("core:opcion_admin") 
            user_obj = Usuario.objects.get(persona=persona)
            request.session["user_id"] = user_obj.id_usuario
            return redirect("core:opcion_usuario")  
        except Persona.DoesNotExist:
            return render(request, "home.html", {
                "error": "Usuario o contraseña incorrectos."
            })

    return render(request, "home.html")

#opciones
def opcion_admin(request):
    return render(request, "opcion/admin.html")
def opcion_usuario(request):
    return render(request, "opcion/cliente.html")
#Persona
def persona_list(request):
    qs = Persona.objects.all()
    return render(request, "persona/list.html", {"persona": qs})

def persona_detail(request, pk):
    obj = get_object_or_404(Persona, pk=pk)
    usuario = obj.usuarios.all()
    return render(request, "persona/detail.html", {"persona": obj, "usuario": usuario})

@require_http_methods(["GET", "POST"])
def persona_create(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)
        if form.is_valid():
            obj = form.save()
            Usuario.objects.create(
                persona=obj,
                estado="activo"
            )
            return redirect("core:home", pk=obj.pk)
    else:
         form = PersonaForm()
    return render(request, "persona/form.html", {"form": form, "mode": "create"})

@require_http_methods(["GET", "POST"])
def persona_update(request, pk):
    obj = get_object_or_404(Persona, pk=pk)
    if request.method == "POST":
        form = PersonaForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            return redirect("core:persona_detail", pk=obj.pk)
    else:
        form = PersonaForm(instance=obj)
    return render(request, "persona/form.html", {"form": form, "mode": "edit", "category": obj})

@require_http_methods(["POST", "GET"])
def persona_delete(request, pk):
    obj = get_object_or_404(Persona, pk=pk)
    if request.method == "POST":
         obj.delete()
         return redirect("core:persona_list")
    return render(request, "persona/delete.html", {"persona": obj})

#Create de admin
@require_http_methods(["GET", "POST"])
def persona_create_admin(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)
        if form.is_valid():
            obj = form.save()
            Administrador.objects.create(
                persona=obj,
                cargo="Artista"   # Valor quemado
            )
            return redirect("core:home", pk=obj.pk)
    else:
         form = PersonaForm()
    return render(request, "persona/form_admin.html", {"form": form, "mode": "create"})

#Metodos de segunda pagina de usuario
def buscar_cancion(request):
    return render(request, "buscar/cancion.html")
def buscar_lista(request):
    return render(request, "buscar/lista.html")
def buscar_vinilo(request):
    return render(request, "buscar/vinilo.html")

#Metodos de segunda pagina admin
@require_http_methods(["GET", "POST"])
def cancion_create(request):
    admin_id = request.session.get("admin_id")
    # Si no hay admin_id, evitar acceso
    if not admin_id:
        return redirect("core:home")
    admin_obj = Administrador.objects.get(pk=admin_id)
    if request.method == "POST":
        form = CancionForm(request.POST, request.FILES)
        if form.is_valid():
            cancion = form.save(commit=False)  
            cancion.admin = admin_obj         
            cancion.save()                    
            return redirect("core:cancion_create")
    else:
        form = CancionForm()

    return render(request, "cancion/form.html", {
        "form": form,
        "mode": "create"
    })

@require_http_methods(["GET"])
def cancion_list(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return redirect("core:home")
    admin_obj = Administrador.objects.get(pk=admin_id)
    canciones = Cancion.objects.filter(admin=admin_obj)
    return render(request, "cancion/list.html", {
        "canciones": canciones
    })