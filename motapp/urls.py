from django.urls import path
from motapp import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('financiacion/', views.financiacion_view, name='financiacion'),
    path('contrato/', views.contrato_view, name='contrato'),
    path('ayuda/', views.ayuda_view, name='ayuda'),
    path('ver-contrato/', views.contrato_dinamico_view, name='ver_contrato'),
]