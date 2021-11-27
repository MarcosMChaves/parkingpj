"""parkingapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('áreas', views.área_listar, name="área_listar"), 
    path('área_inserir', views.área_inserir, name="área_inserir"), 
    path('área_editar/<int:área_id>', views.área_editar, name="área_editar"),
    path('área_excluir/<int:área_id>', views.área_excluir, name="área_excluir"),
    path('estacionamentos', views.estacionamento_listar, name="estacionamento_listar"), 
    path('estacionamento_inserir', views.estacionamento_inserir, name="estacionamento_inserir"), 
    path('estacionamento_editar/<int:estacionamento_id>', views.estacionamento_editar, name="estacionamento_editar"),
    path('estadias', views.estadia_listar, name="estadia_listar"), 
    path('entrada', views.estadia_entrada, name="estadia_entrada"),
    path('saída/<int:estadia_id>', views.estadia_saída, name="estadia_saída"),
    path('receita', views.receita_listar, name="receita_listar"),
    path('fabricantes', views.fabricante_listar, name="fabricante_listar"), 
    path('fabricante_inserir', views.fabricante_inserir, name="fabricante_inserir"), 
    path('fabricante_editar/<int:fabricante_id>', views.fabricante_editar, name="fabricante_editar"),
    path('fabricante_excluir/<int:fabricante_id>', views.fabricante_excluir, name="fabricante_excluir"),
    path('modelos', views.modelo_listar, name="modelo_listar"), 
    path('modelos/<int:fabricante_id>', views.modelo_listar, name="modelo_listar"), 
    path('modelo_inserir', views.modelo_inserir, name="modelo_inserir"), 
    path('modelo_editar/<int:modelo_id>', views.modelo_editar, name="modelo_editar"),
    path('modelo_excluir/<int:modelo_id>', views.modelo_excluir, name="modelo_excluir"),
    path('portes', views.porte_listar, name="porte_listar"), 
    path('porte_inserir', views.porte_inserir, name="porte_inserir"), 
    path('porte_editar/<int:porte_id>', views.porte_editar, name="porte_editar"),
    path('porte_excluir/<int:porte_id>', views.porte_excluir, name="porte_excluir"),
    path('vagas', views.vaga_listar, name="vaga_listar"), 
    path('vaga_inserir', views.vaga_inserir, name="vaga_inserir"), 
    path('vaga_editar/<int:vaga_id>', views.vaga_editar, name="vaga_editar"),
    path('vaga_excluir/<int:vaga_id>', views.vaga_excluir, name="vaga_excluir"),
    path('veículos', views.veículo_listar, name="veículo_listar"), 
    path('pesquisas', views.veículo_pesquisar, name="veículo_pesquisar"),
    path('veículo_insert/<str:placa>/<str:modelo>', views.veículo_insert, name="veículo_insert"), 
    path('veículo_inserir', views.veículo_inserir, name="veículo_inserir"), 
    path('veículo_editar/<int:veículo_id>', views.veículo_editar, name="veículo_editar"),
    path('veículo_excluir/<int:veículo_id>', views.veículo_excluir, name="veículo_excluir"),
    path('user_login', views.user_login, name="user_login"),
    path('user_logout', views.user_logout, name="user_logout"),
]
