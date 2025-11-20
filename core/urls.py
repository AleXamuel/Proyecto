from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    # Category CRUD
    path("persona/", views.persona_list, name="persona_list"),
    path("persona/new/", views.persona_create, name="persona_create"),
    path("persona/<int:pk>/", views.persona_detail, name="persona_detail"),
    path("persona/<int:pk>/edit/", views.persona_update, name="persona_update"),
    path("persona/<int:pk>/delete/", views.persona_delete, name="persona_delete"),
    
]
