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
            # filtra empresas: apenas as que o usuario pode acessar
            self.fields['empresa'].queryset = Empresa.objects.filter(
                Q(criador=user) | Q(projetos__membros=user)
            ).distinct()
            
            
        if self.instance and self.instance.pk:
            #editando projeto existente mantem o usuario atual se ja for membro
            current_members = self.instance.membros.all()
            if user in current_members:
                #inclui o usuario na lista para manter a selecao
                self.fields['membros'].queryset = self.fields['membros'].queryset
            else:
                # exclui o usuario da lista
                self.fields['membros'].queryset = self.fields['membros'].queryset.exclude(id=user.id)
        else:
            # criando novo projeto exclui o usuario da lista
            self.fields['membros'].queryset = self.fields['membros'].queryset.exclude(id=user.id)