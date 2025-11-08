from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Empresa, Projeto

class Command(BaseCommand):
    help = 'Cria dados de teste conforme especificado no teste técnico'

    def handle(self, *args, **options):
        # Criar usuários
        user1 = User.objects.create_user('user1', password='senha_caso1')
        user2 = User.objects.create_user('user2', password='senha_caso2') 
        user3 = User.objects.create_user('user3', password='senha_caso3')
        user4 = User.objects.create_user('user4', password='senha_caso4')

        # Empresa A criada por user1
        empresa_a = Empresa.objects.create(nome='Empresa A', criador=user1, descricao='Empresa principal')
        
        # Empresa B criada por user1
        empresa_b = Empresa.objects.create(nome='Empresa B', criador=user1, descricao='Empresa secundária')

        # user2 cria 3 projetos na Empresa A
        projeto1 = Projeto.objects.create(nome='Projeto Alpha', empresa=empresa_a, criador=user2, descricao='Primeiro projeto')
        projeto2 = Projeto.objects.create(nome='Projeto Beta', empresa=empresa_a, criador=user2, descricao='Segundo projeto')
        projeto3 = Projeto.objects.create(nome='Projeto Gama', empresa=empresa_a, criador=user2, descricao='Terceiro projeto')

        # user3 participa de 2 projetos do user2
        projeto1.membros.add(user3)
        projeto2.membros.add(user3)

        # user4 participa de 1 projeto do user2
        projeto1.membros.add(user4)

        self.stdout.write(self.style.SUCCESS('Dados de teste criados com sucesso!'))