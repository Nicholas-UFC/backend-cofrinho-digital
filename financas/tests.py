from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Transacao
from django.urls import reverse

class TransacaoAPITest(APITestCase):
    def setUp(self):
        # Cria um usuario de mentira
        self.usuario = User.objects.create_user(username="testuser", password='123')

        # Cria uma transação de exemplo
        self.transacao = Transacao.objects.create(
            descricao="Teste Pizza",
            valor=50.00,
            data="2020-01-01",
            tipo="DESPESA",
            usuario=self.usuario
        )

        # O robo faz login
        self.client.force_authenticate(user=self.usuario)

    def test_listar_transacoes(self):
        # O robo tenta ver a lista
        url = '/api/transacoes/'
        resposta = self.client.get(url)

        # O robo ver se deu certo
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.data['results']), 1)
        print("Teste de listagem: ✅")

    def test_criar_transacao(self):
        # O robo tenta criar uma receita nova
        dados = {
            "descricao": "Salário",
            "valor": 5000,
            "data": "2020-12-12",
            "tipo": "RECEITA",
        }

        url = "/api/transacoes/"
        resposta = self.client.post(url, dados)

        # Verificação
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(Transacao.objects.count(), 2)
        print("Teste de Criação: ✅")

    def test_atualizar_transacao(self):
        url = f'/api/transacoes/{self.transacao.id}/'
        novos_dados = {
            "descricao": "Pizza Gigante", 
            "valor": 80.00,             
            "data": "2023-10-27",
            "tipo": "DESPESA"
        }
        resposta = self.client.put(url, novos_dados)
        
        self.assertEqual(resposta.status_code, 200) 
        self.transacao.refresh_from_db() 
        self.assertEqual(self.transacao.valor, 80.00)
        print("Teste de Edição: ✅")

    def test_seguranca_outros_usuarios(self):
        # Crio um usuário ladrão
        ladrao = User.objects.create_user(username='ladrao', password='123')
        
        # Logo como o ladrão
        self.client.force_authenticate(user=ladrao)
        
        # Tento acessar a transação do usuário original (criada no setUp)
        url = f'/api/transacoes/{self.transacao.id}/'
        resposta = self.client.get(url)
        
        # Esperamos um 404 (Não Encontrado) 
        self.assertEqual(resposta.status_code, 404)
        print("Teste de Segurança (Espião): ✅")

    def test_calculadora_saldo(self):
        Transacao.objects.create(
            descricao="Bónus", 
            valor=200.00, 
            data="2023-10-28", 
            tipo="RECEITA", 
            usuario=self.usuario
        )
        
        # Saldo esperado: 200 (Receita) - 50 (Despesa) = 150
        url = '/api/transacoes/resumo/'
        resposta = self.client.get(url)
        
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.data['saldo_atual'], 150.00)
        self.assertEqual(resposta.data['receita_total'], 200.00)
        print("Teste da Matemática: ✅")

    def test_registro_usuario(self):
        url = '/api/register/'
        dados = {
            "username": "usuario_teste_auto",
            "email": "teste@auto.com",
            "password": "senha_super_secreta_123"
        }
        
        # Tenta criar (POST)
        resposta = self.client.post(url, dados)
        
        # Verificações Básicas
        self.assertEqual(resposta.status_code, 201) # Criou?
        
        # Verificando se está no banco
        novo_user = User.objects.get(username="usuario_teste_auto")
        self.assertEqual(novo_user.email, "teste@auto.com")
        
        # A senha no banco NÃO pode ser igual ao texto enviado
        self.assertNotEqual(novo_user.password, "senha_super_secreta_123")
        self.assertTrue(novo_user.check_password("senha_super_secreta_123"))
        
        print("Teste de Registro e Criptografia: ✅")