from django.urls import path

from . import views

app_name = "gestao"

urlpatterns = [
    path('', views.index, name="index"),
    path('nova-os/', views.nova_ordem_de_servico, name="nova_ordem_de_servico"),
    path('ordens-de-servico/', views.OrdemDeServicoListView.as_view(), name="ordens_de_servico"),
    path('ordens-de-servico/atribuidas/', views.ordens_de_servico_atribuidas, name="ordens_de_servico_atribuidas"),
    path('ordens-de-servico/<int:pk>/', views.OrdemDeServicoDetailView.as_view(), name="detalhe_ordem_de_servico"),
    path('ordens-de-servico/<int:pk>:update', views.OrdemDeServicoUpdateView.as_view(), name="atualizacao_ordem_de_servico")
]
