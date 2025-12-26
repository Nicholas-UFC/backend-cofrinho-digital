import csv

from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Categoria, Transacao
from .serializers import RegisterSerializer, TransacaoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = TransacaoSerializer
    permission_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class TransacaoViewSet(viewsets.ModelViewSet):
    serializer_class = TransacaoSerializer
    permission_class = [permissions.IsAuthenticated]

    # Configurações dos filtros
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]  # Ativando a ferramenta

    filterset_fields = ["tipo", "data"]  # Os tipos de filtros aceitos

    ordering_fields = ["data", "valor"]  # Os tipos de ordenação aceitos
    ordering = ["-data"]  # padrão: Ordenar dos mais recentes para os mais antigos

    def get_queryset(self):
        return Transacao.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=["get"])
    def resumo(self, request):
        usuario = request.user

        # Soma todas as receitas desse usuario
        total_receita = (
            Transacao.objects.filter(usuario=usuario, tipo="RECEITA").aggregate(
                soma=Sum("valor")
            )["soma"]
            or 0
        )

        # soma todas as despesas desse usuario
        total_despesa = (
            Transacao.objects.filter(usuario=usuario, tipo="DESPESA").aggregate(
                soma=Sum("valor")
            )["soma"]
            or 0
        )

        # calcula o saldo
        saldo = total_receita - total_despesa

        return Response(
            {
                "receita_total": total_receita,
                "despesa_total": total_despesa,
                "saldo_atual": saldo,
            }
        )

    @action(detail=False, methods=["get"])
    def exportar(self, request):
        # Função que serve para baixar um arquivo csv com todas as transações do usuario
        usuario = request.user
        queryset = Transacao.objects.filter(usuario=usuario)

        # Preparando resposta HTTP para ser um arquivo
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="meu_cofrinho.csv"'
        response.write("\ufeff".encode("utf8"))

        # Criando o escritor de csv
        writer = csv.writer(response)

        writer.writerow(["ID", "Descrição", "Valor", "Data", "Tipo"])

        for transacao in queryset:
            writer.writerow(
                [
                    transacao.id,
                    transacao.descricao,
                    transacao.valor,
                    transacao.data,
                    transacao.tipo,
                ]
            )

        return response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
