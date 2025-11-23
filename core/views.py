from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .models import *
from .forms import *

def home(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            persona = Persona.objects.filter(username=username, contrasena=password).first()
            request.session["persona_id"] = persona.id_persona
            if Administrador.objects.filter(persona=persona).exists():
                admin_obj = Administrador.objects.get(persona=persona)
                request.session["admin_id"] = admin_obj.id_admin
                return redirect("core:opcion_admin") 
            try:
                user_obj = Usuario.objects.get(persona=persona)
                request.session["user_id"] = user_obj.id_usuario
                return redirect("core:opcion_usuario")  
            except Usuario.DoesNotExist:
                return render(request, "home.html", {
                    "error": "Usuario o contraseña incorrectos."
                })
        except:
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
            return redirect("core:home")
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
         return redirect("core:home")
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
            return redirect("core:home")
    else:
         form = PersonaForm()
    return render(request, "persona/form_admin.html", {"form": form, "mode": "create"})

#Metodos de segunda pagina de usuario
def buscar_cancion(request):
    canciones = Cancion.objects.all()
    return render(request, "buscar/cancion.html", {"canciones": canciones})
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
def cancion_list_admin(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return redirect("core:home")
    admin_obj = Administrador.objects.get(pk=admin_id)
    canciones = Cancion.objects.filter(admin=admin_obj)
    return render(request, "cancion/list.html", {
        "canciones": canciones
    })
#require methods
@require_http_methods(["GET"])
def cancion_detail(request, pk):
    cancion = get_object_or_404(Cancion, pk=pk)
    return render(request, "cancion/detail.html", {
        "cancion": cancion
    })
@require_http_methods(["GET"])
def cancion_detail_usuario(request, pk):
    cancion = get_object_or_404(Cancion, pk=pk)
    return render(request, "cancion/detail_usuario.html", {
        "cancion": cancion
    })

@require_http_methods(["GET", "POST"])
def cancion_update(request, pk):
    cancion = get_object_or_404(Cancion, pk=pk)

    if request.method == "POST":
        form = CancionForm(request.POST, request.FILES, instance=cancion)
        if form.is_valid():
            form.save()
            return redirect("core:cancion_detail", pk=cancion.pk)  # o lista
    else:
        form = CancionForm(instance=cancion)

    return render(request, "cancion/form.html", {"form": form})
#Vinilo
@require_http_methods(["GET", "POST"])
def vinilo_create(request):
    user  = request.session.get("user_id")
    if request.method == "POST":
        form = ViniloForm(request.POST, request.FILES)
        usuario = Usuario.objects.get(pk=user)
        if form.is_valid():
            vinilo = form.save(commit=False)
            vinilo.usuario = usuario
            vinilo.save()
            # Guardar canciones seleccionadas en la tabla intermedia
            canciones = form.cleaned_data['canciones']
            for cancion in canciones:
                ContenidoVinilos.objects.create(
                    vinilo=vinilo,
                    cancion=cancion
                )

            return redirect('core:vinilo_create')

    else:
        form = ViniloForm()

    return render(request, 'vinilo/form.html', {'form': form})

@require_http_methods(["GET"])
def vinilo_list(request):
    canciones = Vinilo.objects.all()
    return render(request, "vinilo/list.html", {"vinilos": canciones})
@require_http_methods(["GET"])
def vinilo_list_user(request):
    user_id = request.session.get("user_id")
    user = Usuario.objects.get(pk=user_id)
    vinilos = Vinilo.objects.filter(usuario=user)
    return render(request, "vinilo/list_user.html", {
        "vinilos": vinilos
    })
@require_http_methods(["GET"])
def vinilo_detail(request, pk):
    cancion = get_object_or_404(Vinilo, pk=pk)
    return render(request, "vinilo/detail.html", {
        "vinilo": cancion
    })
