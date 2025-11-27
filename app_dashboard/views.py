from django.shortcuts import render
from django.http import JsonResponse
from .models import Produto
from .utils import importar_planilha
from django.db.models import Count, Sum, Avg

def dashboard(request):
    resultado_importacao = importar_planilha()
    
    total_produtos = Produto.objects.count()
    total_estoque = Produto.objects.aggregate(total=Sum("estoque"))["total"] or 0
    
    produtos = Produto.objects.all()
    valor_total_estoque = sum(produto.preco * produto.estoque for produto in produtos)
    
    preco_medio = Produto.objects.aggregate(media=Avg("preco"))["media"] or 0
    
    produtos_por_categoria = Produto.objects.values("categoria").annotate(
        total=Count("id_produto"),
        estoque_total=Sum("estoque")
    )
    
    marcas_top = Produto.objects.values("marca").annotate(
        total=Count("id_produto")
    ).order_by("-total")[:5]
    
    estoque_baixo = Produto.objects.filter(estoque__lt=10).count()
    
    context = {
        "total_produtos": total_produtos,
        "total_estoque": total_estoque,
        "valor_total_estoque": round(valor_total_estoque, 2),
        "preco_medio": round(preco_medio, 2),
        "produtos_por_categoria": list(produtos_por_categoria),
        "marcas_top": list(marcas_top),
        "estoque_baixo": estoque_baixo,
        "produtos": produtos,
        "importacao": resultado_importacao,
    }
    
    return render(request, "app_dashboard/dashboard.html", context)

def atualizar_dados(request):
    resultado = importar_planilha()
    return JsonResponse(resultado)
