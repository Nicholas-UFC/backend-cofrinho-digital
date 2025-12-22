from django.db import models
from django.contrib.auth.models import User


# Modelo de categoria das transações para gerar uma chave extrangeira e facilitar analise
class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    dt_criacao = models.DateTimeField(auto_now_add=True)

    # Cada usuario vai ter suas categorias
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

# Modelo das transações
class Transacao(models.Model):
    # Tipos de Transação
    TIPOS = (
        ("RECEITA", "Receita (Entrou Dinheiro)"),
        ("DESPESA", "Despesa (Saiu Dinheiro)"),
    )

    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPOS)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    
    # Chave estrangeira: Para saber quem fez a transação
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.tipo == "RECEITA":
            return f"{self.descricao} + R$ {self.valor}"
        else:
            return f"{self.descricao} - R$ {self.valor}"
