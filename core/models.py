from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="empresas_criadas")
    descricao = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    nome = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="projetos")
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projetos_criados")
    membros = models.ManyToManyField(User, related_name="projetos_participando", blank=True)
    descricao = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.empresa.nome})"
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        
        # add o criador como membro
        if self.criador not in self.membros.all():
            self.membros.add(self.criador)