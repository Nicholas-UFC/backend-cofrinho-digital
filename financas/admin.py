from django.contrib import admin

from .models import Categoria, Transacao

admin.site.register(Transacao)
admin.site.register(Categoria)
