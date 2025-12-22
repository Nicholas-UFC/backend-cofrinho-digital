from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Categoria, Transacao


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome"]


class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = ["id", "descricao", "valor", "data", "tipo", "categoria"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"]
        )
        return user