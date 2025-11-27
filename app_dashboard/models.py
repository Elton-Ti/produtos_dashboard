from django.db import models

class Produto(models.Model):
    id_produto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    data_cadastro = models.DateField()
    ativo = models.BooleanField(default=True)
    
    class Meta:
        db_table = "produtos"
    
    def __str__(self):
        return self.nome
