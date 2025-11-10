Sistema de Gerenciamento de Projetos

Sistema web para gerenciar empresas e projetos com controle de acesso.

Como Rodar a Aplicação

1. Clone e entre na pasta

git clone https://github.com/robert-angelo19/gestao

cd gestao

2. Configure o ambiente virtual

python -m venv venv

source venv/bin/activate

3. Instale as dependências

pip install -r requirements.txt

4. Execute o servidor

python manage.py runserver

5. Acesse no navegador
http://127.0.0.1:8000

Contas para Testar:

Admin: admin / admin123

User1: user1 / senha_caso1 (Criador das empresas A e B)

User2: user2 / senha_caso2 (Criador dos 3 projetos na empresa A)

User3: user3 / senha_caso3 (Participante de 2 projetos criados pelo user 2)

User4: user4 / senha_caso4 (Participante de 1 projeto criado pelo user 2)