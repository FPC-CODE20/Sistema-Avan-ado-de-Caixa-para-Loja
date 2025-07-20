from rest_framework import viewsets, permissions
from .models import Produto, Venda, Cliente
from .serializers import ProdutoSerializer, VendaSerializer, ClienteSerializer
from .permissions import IsGerenteOrAdmin, IsCaixaOrAbove

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsGerenteOrAdmin]

class VendaViewSet(viewsets.ModelViewSet):
    serializer_class = VendaSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            permission_classes = [IsCaixaOrAbove]
        else:
            permission_classes = [IsGerenteOrAdmin]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.nivel_acesso in ['GERENTE', 'ADMIN']:
            return Venda.objects.filter(operador__loja=user.loja)
        return Venda.objects.filter(operador=user)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsCaixaOrAbove]
