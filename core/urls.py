from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    # Category CRUD
    path("persona/", views.persona_list, name="persona_list"),
    path("persona/new/", views.persona_create, name="persona_create"),
    path("persona/admin/", views.persona_create_admin, name="persona_create_admin"),
    path("persona/<int:pk>/", views.persona_detail, name="persona_detail"),
    path("persona/<int:pk>/edit/", views.persona_update, name="persona_update"),
    path("persona/<int:pk>/delete/", views.persona_delete, name="persona_delete"),
    path("buscar/cancion/", views.buscar_cancion, name="buscar_cancion"),
    path("cancion/new/", views.cancion_create, name="cancion_create"),
    path("opcion_usuario/", views.opcion_usuario, name="opcion_usuario"),
    path("opcion_admin/", views.opcion_admin, name="opcion_admin"),
    path("cancion/", views.cancion_list_admin, name="cancion_list_admin"),
    path("cancion/<int:pk>/", views.cancion_detail, name="cancion_detail"),
    path("cancion/<int:pk>/edit/", views.cancion_update, name="cancion_update"),
    path("cancionu/<int:pk>/", views.cancion_detail_usuario, name="cancion_detail_usuario"),
    path("vinilo/new/", views.vinilo_create, name="vinilo_create"),
    path("vinilo/lista/", views.vinilo_list, name="vinilo_list"),
    path("vinilo/listau/", views.vinilo_list_user, name="vinilo_list_user"),
    path("vinilo/<int:pk>/", views.vinilo_detail, name="vinilo_detail"),
    path("vinilo/user/<int:pk>/", views.vinilo_detail_user, name="vinilo_detail_user"),
    path("vinilo/<int:pk>/edit/", views.vinilo_update, name="vinilo_update"),   
    path("carrito/vinilo/<int:pk>", views.carrito_vinilo, name="carrito_vinilo"),
    path("carrito/cancion/<int:pk>", views.carrito_cancion, name="carrito_cancion"),
    path("carrito", views.carrito_list, name="carrito_list"),
    path("carrito/pago", views.carrito_pagar, name="carrito_pagar"),
    path("compras/", views.compra_list, name="compra_list"),
    path("compras/<int:compra_id>/", views.compra_detail, name="compra_detail"),
    path("carrito/eliminar_vinilo/<int:pk>/", views.carrito_eliminar_vinilo, name="carrito_eliminar_vinilo"),
    path("carrito/elliminar_cancion/<int:pk>/", views.carrito_eliminar_cancion, name="carrito_eliminar_cancion"),
    path("ventas/", views.venta_list, name="venta_list"),
    path("ventas/<int:id_compra>/", views.venta_detail, name="venta_detail"),



    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
