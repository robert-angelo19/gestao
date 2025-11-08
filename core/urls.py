from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # Empresas
    path('empresas/', views.empresa_list, name='empresa_list'),
    path('empresas/novo/', views.empresa_create, name='empresa_create'),
    path('empresas/<int:pk>/', views.empresa_detail, name='empresa_detail'),
    path('empresas/<int:pk>/editar/', views.empresa_update, name='empresa_update'),
    path('empresas/<int:pk>/excluir/', views.empresa_delete, name='empresa_delete'),
    # Projetos
    path('projetos/novo/', views.projeto_create, name='projeto_create'),
    path('projetos/<int:pk>/', views.projeto_detail, name='projeto_detail'),
    path('projetos/<int:pk>/editar/', views.projeto_update, name='projeto_update'),
    path('projetos/<int:pk>/excluir/', views.projeto_delete, name='projeto_delete'),
    path('projetos/<int:pk>/membros/', views.projeto_membros_manage, name='projeto_membros_manage'),
    path('projetos/novo-global/', views.projeto_create_global, name='projeto_create_global'),  # ← NOVA
    # Users
    path('users/', views.user_list, name='user_list'),
    path('users/novo/', views.user_create, name='user_create'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/editar/', views.user_update, name='user_update'),
    path('users/<int:pk>/excluir/', views.user_delete, name='user_delete'),
]