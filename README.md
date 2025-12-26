# 💰 Cofrinho Digital API

Backend profissional para gestão financeira pessoal. Desenvolvido com **Django REST Framework**.

## 🚀 Tecnologias Usadas
- **Python & Django**
- **Django REST Framework (DRF)**
- **MySQL** (Banco de Dados de Produção)
- **JWT** (Autenticação Segura)
- **Django Jazzmin** (Admin Dashboard Moderno)
- **Unit Tests** (Cobertura de Segurança e Lógica)
- **Swagger/OpenAPI** (Documentação Automática)

## ⚙️ Funcionalidades
- [x] CRUD de Transações (Receitas e Despesas)
- [x] Gestão de Categorias
- [x] Cálculo automático de Saldo em Tempo Real
- [x] Exportação de dados para CSV (Excel Compatível)
- [x] Registo de Usuários com senha Criptografada
- [x] Isolamento de dados (Cada usuário vê apenas o seu)

## 🔧 Como Rodar Localmente

1. Clone o repositório:
git clone https://github.com/Nicholas-UFC/backend-cofrinho-digital.git

2. Instale as dependências:
pip install -r requirements_dev.txt

3. Crie um arquivo `.env` na raiz com suas credenciais:
SECRET_KEY=sua_chave
DEBUG=True
DB_NAME=cofrinho_db
DB_USER=root
DB_PASSWORD=sua_senha

4. Rode as migrações e o servidor:
python manage.py migrate
python manage.py runserver

## 🧪 Testes
Para rodar a bateria de testes automatizados:
python manage.py test financas