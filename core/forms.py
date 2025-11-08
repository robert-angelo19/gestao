from django import forms
from django.db.models import Q
from .models import Empresa, Projeto

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome', 'descricao']

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'descricao', 'empresa', 'membros']
        widgets = {
            'membros': forms.CheckboxSelectMultiple
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProjetoForm, self).__init__(*args, **kwargs)
        
        if user:
            # Filtra empresas: apenas as que o usuário pode acessar
            self.fields['empresa'].queryset = Empresa.objects.filter(
                Q(criador=user) | Q(projetos__membros=user)
            ).distinct()
            
            # Filtra membros: exclui o próprio usuário da lista de membros
            self.fields['membros'].queryset = self.fields['membros'].queryset.exclude(id=user.id)