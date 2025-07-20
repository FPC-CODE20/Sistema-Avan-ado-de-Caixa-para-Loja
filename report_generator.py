import pandas as pd
import matplotlib.pyplot as plt
from django.db.models import Sum, Count, F
from .models import Venda, ItemVenda, Produto
from datetime import datetime, timedelta

class ReportGenerator:
    def __init__(self, loja_id, start_date=None, end_date=None):
        self.loja_id = loja_id
        self.end_date = end_date or datetime.now()
        self.start_date = start_date or (self.end_date - timedelta(days=30))
    
    def vendas_por_periodo(self):
        vendas = Venda.objects.filter(
            operador__loja_id=self.loja_id,
            data__range=[self.start_date, self.end_date]
        ).annotate(
            dia=models.functions.TruncDay('data')
        ).values('dia').annotate(
            total=Sum('total'),
            quantidade=Count('id')
        ).order_by('dia')
        
        df = pd.DataFrame(list(vendas))
        if not df.empty:
            df['dia'] = pd.to_datetime(df['dia'])
            df.set_index('dia', inplace=True)
            
            plt.figure(figsize=(12, 6))
            df['total'].plot(kind='bar')
            plt.title('Vendas por Dia')
            plt.xlabel('Data')
            plt.ylabel('Valor (R$)')
            plt.tight_layout()
            plt.savefig('vendas_por_dia.png')
        
        return df
    
    def produtos_mais_vendidos(self):
        produtos = ItemVenda.objects.filter(
            venda__operador__loja_id=self.loja_id,
            venda__data__range=[self.start_date, self.end_date]
        ).values(
            'produto__nome'
        ).annotate(
            quantidade=Sum('quantidade'),
            total=Sum(F('quantidade') * F('preco_unitario'))
        ).order_by('-quantidade')[:10]
        
        df = pd.DataFrame(list(produtos))
        if not df.empty:
            plt.figure(figsize=(12, 6))
            df.plot(x='produto__nome', y='quantidade', kind='bar')
            plt.title('Produtos Mais Vendidos')
            plt.xlabel('Produto')
            plt.ylabel('Quantidade Vendida')
            plt.tight_layout()
            plt.savefig('produtos_mais_vendidos.png')
        
        return df
    
    def lucro_por_categoria(self):
        # Implementar quando tiver categorias de produtos
        pass
    
    def gerar_relatorio_completo(self):
        vendas = self.vendas_por_periodo()
        produtos = self.produtos_mais_vendidos()
        
        with open('relatorio_completo.html', 'w') as f:
            f.write("<html><head><title>Relatório Completo</title></head><body>")
            f.write("<h1>Relatório de Vendas</h1>")
            f.write(f"<p>Período: {self.start_date} a {self.end_date}</p>")
            
            f.write("<h2>Vendas por Dia</h2>")
            f.write(vendas.to_html())
            f.write('<img src="vendas_por_dia.png" alt="Vendas por Dia">')
            
            f.write("<h2>Produtos Mais Vendidos</h2>")
            f.write(produtos.to_html())
            f.write('<img src="produtos_mais_vendidos.png" alt="Produtos Mais Vendidos">')
            
            f.write("</body></html>")
        
        return 'relatorio_completo.html'
