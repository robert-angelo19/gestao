from django import forms
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