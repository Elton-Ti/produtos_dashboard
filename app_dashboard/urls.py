from django.urls import path
from . import views

app_name = "app_dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("atualizar/", views.atualizar_dados, name="atualizar_dados"),
]
