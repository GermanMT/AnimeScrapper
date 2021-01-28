from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.inicio),
    path('carga/',views.carga),
    path('cargaRS/',views.cargaRS),
    path('buscaranimesportitulo/', views.buscar_titulo),
    path('buscaranimesportipo/', views.buscar_tipo),
    path('buscaranimesporsinopsis/', views.buscar_sinopsis),
    path('buscaranimesporgenero/', views.buscar_genero),
    path('recomendadossimilares/', views.animes_parecidos),
    path('recomendadosporpuntuacion/', views.animes_recomendados_puntuacion),
]