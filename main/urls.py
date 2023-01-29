from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index),
    path('index.html', views.index),
]
