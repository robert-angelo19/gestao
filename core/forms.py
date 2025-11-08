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
            self.fields['empresa'].queryset = Empresa.objects.all()
            
        if self.instance and self.instance.pk:
            current_members = self.instance.membros.all()
            if user in current_members:
                self.fields['membros'].queryset = self.fields['membros'].queryset
            else:
                self.fields['membros'].queryset = self.fields['membros'].queryset.exclude(id=user.id)
        else:
            self.fields['membros'].queryset = self.fields['membros'].queryset.exclude(id=user.id)
    
    
    def save(self, commit=True):
        projeto = super().save(commit=False)
        if commit:
            projeto.save()
            # garante que o criador do proj seja membro
            if projeto.criador not in projeto.membros.all():
                projeto.membros.add(projeto.criador)
            self.save_m2m()
        return projeto  