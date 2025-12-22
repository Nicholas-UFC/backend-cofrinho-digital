from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("financas.urls")),

    # Rotas da documentação
    path(
        "api/schema", SpectacularAPIView.as_view(), name="schema"
    ),  # esquema cru em JSON
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),  # Interface bonita

    # Rotas de autentificação JWT
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"), # login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # renovar token
]
