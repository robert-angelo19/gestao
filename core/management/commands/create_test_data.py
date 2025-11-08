from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Empresa, Projeto

class Command(BaseCommand):
    help = 'Cria dados de teste para o sistema'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando criação de dados de teste...")
        
        # criar superusuario
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com', 
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Superusuário admin criado (senha: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('Superusuário admin já existe'))

        # criar usuarios
        if not User.objects.filter(username='user1').exists():
            
            user1 = User.objects.create_user('user1', password='senha_caso1')
            user2 = User.objects.create_user('user2', password='senha_caso2') 
            user3 = User.objects.create_user('user3', password='senha_caso3')
            user4 = User.objects.create_user('user4', password='senha_caso4')
            
            self.stdout.write(self.style.SUCCESS('Usuários de teste criados: user1, user2, user3, user4'))

            # criar empresas
            empresa_a = Empresa.objects.create(
                nome='Empresa A', 
                criador=user1, 
                descricao='Empresa principal do sistema'
            )
            
            empresa_b = Empresa.objects.create(
                nome='Empresa B', 
                criador=user1, 
                descricao='Empresa secundária'
            )
            
            self.stdout.write(self.style.SUCCESS('Empresas criadas: Empresa A, Empresa B'))

            # criar projs
            projeto1 = Projeto.objects.create(
                nome='Projeto Alpha', 
                empresa=empresa_a, 
                criador=user2, 
                descricao='Primeiro projeto de desenvolvimento'
            )
            
            projeto2 = Projeto.objects.create(
                nome='Projeto Beta', 
                empresa=empresa_a, 
                criador=user2, 
                descricao='Segundo projeto de marketing'
            )
            
            projeto3 = Projeto.objects.create(
                nome='Projeto Gama', 
                empresa=empresa_a, 
                criador=user2, 
                descricao='Terceiro projeto de pesquisa'
            )
            
            self.stdout.write(self.style.SUCCESS('Projetos criados: Alpha, Beta, Gama'))

            # adicionar membros aos proj
            # user3 participa de 2 projetos do user2
            projeto1.membros.add(user3)
            projeto2.membros.add(user3)

            # user4 participa de 1 projeto do user2  
            projeto1.membros.add(user4)

            self.stdout.write(self.style.SUCCESS('Membros adicionados aos projetos'))
            
            self.stdout.write(self.style.SUCCESS('Todos os dados de teste foram criados com sucesso!'))
            
        else:
            self.stdout.write(self.style.WARNING('Dados de teste já existem no banco'))

        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS("CREDENCIAIS DE TESTE DISPONÍVEIS:"))
        self.stdout.write(self.style.SUCCESS("Admin: admin / admin123"))
        self.stdout.write(self.style.SUCCESS("User1: user1 / senha_caso1 (Criador das empresas)"))
        self.stdout.write(self.style.SUCCESS("User2: user2 / senha_caso2 (Criador dos projetos)"))
        self.stdout.write(self.style.SUCCESS("User3: user3 / senha_caso3 (Membro de 2 projetos)"))
        self.stdout.write(self.style.SUCCESS("User4: user4 / senha_caso4 (Membro de 1 projeto)"))
        self.stdout.write("="*50)