from django.contrib import admin

from django.contrib import admin
from .models import Empresa, Projeto

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'criador', 'created_at')

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'empresa', 'criador', 'created_at')
    filter_horizontal = ('membros',)
