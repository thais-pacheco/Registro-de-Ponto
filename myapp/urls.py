from django.urls import path
from . import views

urlpatterns = [
    path('', views.mysite, name='mysite'),
    path('api/localizacao/', views.registrar_localizacao, name='registrar_localizacao'),
]
