from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('entrar/', views.entrar, name='entrar'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('sair/', views.sair, name='sair'),
    path('nova_denuncia/', views.nova_denuncia, name='nova_denuncia'),
    path('minhas_denuncias/', views.minhas_denuncias, name='minhas_denuncias'),
    path('denuncia_anonima/', views.denuncia_anonima, name='denuncia_anonima'),
    path('denuncia/<int:token>/', views.ver_denuncia, name='ver_denuncia'),
]