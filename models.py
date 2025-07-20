from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    NIVEL_ACESSO = [
        ('CAIXA', 'Caixa'),
        ('GERENTE', 'Gerente'),
        ('ADMIN', 'Administrador'),
    ]
    nivel_acesso = models.CharField(max_length=7, choices=NIVEL_ACESSO, default='CAIXA')
    loja = models.ForeignKey('Loja', on_delete=models.SET_NULL, null=True)

class Loja(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.TextField()

class Produto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    pontos_fidelidade = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)

class Venda(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    operador = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    forma_pagamento = models.CharField(max_length=50)
    cupom_fiscal = models.CharField(max_length=44, unique=True)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
