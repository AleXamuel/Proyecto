from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Category, Product
from .forms import CategoryForm, ProductForm


# Create your views here.
#Muestra la template home.html
def home(request):
 return render(request, "home.html", {"title": "Hola bhbhjbjhbjhkbjhkbkh!"})
def api_echo(request):
    msg = request.GET.get("msg")
    if not msg:
        return JsonResponse({"error": "Falta 'msg'."}, status=400)
    return JsonResponse({"echo": msg, "length": len(msg)})
def api_ping(request):
 return JsonResponse({"ok": True, "message": "pong"})

# ---------- Category ----------
def category_list(request):
    qs = Category.objects.all()
    return render(request, "categories/list.html", {"categories": qs})
def category_detail(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    # opcional: incluir productos relacionados
    products = obj.products.all()
    return render(request, "categories/detail.html", {"category": obj, "products": products})
@require_http_methods(["GET", "POST"])
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect("core:category_detail", pk=obj.pk)
    else:
         form = CategoryForm()
    return render(request, "categories/form.html", {"form": form, "mode": "create"})
@require_http_methods(["GET", "POST"])
def category_update(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            return redirect("core:category_detail", pk=obj.pk)
    else:
        form = CategoryForm(instance=obj)
    return render(request, "categories/form.html", {"form": form, "mode": "edit", "category": obj})
@require_http_methods(["POST", "GET"])
def category_delete(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
         obj.delete()
         return redirect("core:category_list")
 # confirmación sencilla
    return render(request, "categories/confirm_delete.html", {"category": obj})
# ---------- Product ----------
def product_list(request):
    qs = Product.objects.select_related("category").all()
    return render(request, "products/list.html", {"products": qs})

def product_detail(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    return render(request, "products/detail.html", {"product": obj})

@require_http_methods(["GET", "POST"])
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect("core:product_detail", pk=obj.pk)
    else:
        form = ProductForm()
    return render(request, "products/form.html", {"form": form, "mode": "create"})
@require_http_methods(["GET", "POST"])
def product_update(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            return redirect("core:product_detail", pk=obj.pk)
    else:
        form = ProductForm(instance=obj)
    return render(request, "products/form.html", {"form": form, "mode": "edit", "product": obj})
@require_http_methods(["POST", "GET"])
def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("core:product_list")
    return render(request, "products/confirm_delete.html", {"product": obj})