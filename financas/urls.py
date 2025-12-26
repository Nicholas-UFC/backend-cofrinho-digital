from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet, RegisterView, TransacaoViewSet

router = DefaultRouter()
router.register(r"transacoes", TransacaoViewSet, basename="transacao")
router.register(r"categorias", CategoriaViewSet, basename="categoria")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
]
