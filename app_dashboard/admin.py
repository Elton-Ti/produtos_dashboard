from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ["id_produto", "nome", "categoria", "marca", "preco", "estoque", "ativo"]
    list_filter = ["categoria", "marca", "ativo"]
    search_fields = ["nome", "marca"]
