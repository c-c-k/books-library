from django.urls import path

from . import views

app_name = 'site_index'
urlpatterns = [
    path('', views.index, name="index")
]
