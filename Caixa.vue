<template>
  <div class="caixa-container">
    <div class="produto-search">
      <input v-model="codigoProduto" @keyup.enter="adicionarProduto" placeholder="Código do produto">
      <button @click="adicionarProduto">Adicionar</button>
    </div>
    
    <div class="carrinho">
      <table>
        <thead>
          <tr>
            <th>Produto</th>
            <th>Preço</th>
            <th>Quantidade</th>
            <th>Subtotal</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in carrinho" :key="index">
            <td>{{ item.produto.nome }}</td>
            <td>R$ {{ item.produto.preco_venda.toFixed(2) }}</td>
            <td>
              <input type="number" v-model.number="item.quantidade" min="1">
            </td>
            <td>R$ {{ (item.produto.preco_venda * item.quantidade).toFixed(2) }}</td>
            <td>
              <button @click="removerItem(index)">Remover</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="resumo-venda">
      <h3>Resumo da Venda</h3>
      <p>Total: R$ {{ totalVenda.toFixed(2) }}</p>
      <div class="cliente-section">
        <input v-model="cpfCliente" placeholder="CPF do cliente">
        <button @click="buscarCliente">Buscar</button>
        <div v-if="cliente">
          <p>Cliente: {{ cliente.nome }} (Pontos: {{ cliente.pontos_fidelidade }})</p>
        </div>
      </div>
      <button @click="finalizarVenda" :disabled="carrinho.length === 0">Finalizar Venda</button>
    </div>
    
    <div class="cupom" v-if="cupomFiscal">
      <h3>Cupom Fiscal</h3>
      <pre>{{ cupomFiscal }}</pre>
      <button @click="imprimirCupom">Imprimir</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      codigoProduto: '',
      carrinho: [],
      cpfCliente: '',
      cliente: null,
      cupomFiscal: null
    }
  },
  computed: {
    totalVenda() {
      return this.carrinho.reduce((total, item) => {
        return total + (item.produto.preco_venda * item.quantidade)
      }, 0)
    }
  },
  methods: {
    async adicionarProduto() {
      try {
        const response = await this.$http.get(`/api/produtos/${this.codigoProduto}/`);
        const produto = response.data;
        
        const itemExistente = this.carrinho.find(item => item.produto.codigo === produto.codigo);
        if (itemExistente) {
          itemExistente.quantidade += 1;
        } else {
          this.carrinho.push({
            produto: produto,
            quantidade: 1
          });
        }
        
        this.codigoProduto = '';
      } catch (error) {
        alert('Produto não encontrado!');
      }
    },
    removerItem(index) {
      this.carrinho.splice(index, 1);
    },
    async buscarCliente() {
      try {
        const response = await this.$http.get(`/api/clientes/?cpf=${this.cpfCliente}`);
        this.cliente = response.data.results[0];
      } catch (error) {
        alert('Cliente não encontrado. Cadastre um novo cliente.');
      }
    },
    async finalizarVenda() {
      try {
        const vendaData = {
          itens: this.carrinho.map(item => ({
            produto: item.produto.id,
            quantidade: item.quantidade,
            preco_unitario: item.produto.preco_venda
          })),
          cliente: this.cliente ? this.cliente.id : null
        };
        
        const response = await this.$http.post('/api/vendas/', vendaData);
        this.cupomFiscal = this.gerarCupom(response.data);
        this.carrinho = [];
        this.cliente = null;
        this.cpfCliente = '';
      } catch (error) {
        alert('Erro ao finalizar venda: ' + error.message);
      }
    },
    gerarCupom(venda) {
      let cupom = `LOJA XYZ\n`;
      cupom += `CNPJ: 12.345.678/0001-99\n`;
      cupom += `CUPOM FISCAL: ${venda.cupom_fiscal}\n`;
      cupom += `DATA: ${new Date(venda.data).toLocaleString()}\n`;
      cupom += `--------------------------------\n`;
      
      venda.itens.forEach(item => {
        cupom += `${item.quantidade}x ${item.produto.nome}\n`;
        cupom += `R$ ${item.preco_unitario} = R$ ${(item.preco_unitario * item.quantidade).toFixed(2)}\n`;
      });
      
      cupom += `--------------------------------\n`;
      cupom += `TOTAL: R$ ${venda.total.toFixed(2)}\n`;
      cupom += `FORMA PAGAMENTO: ${venda.forma_pagamento}\n`;
      
      if (venda.cliente) {
        cupom += `CLIENTE: ${venda.cliente.nome} (CPF: ${venda.cliente.cpf})\n`;
        cupom += `PONTOS GANHOS: ${Math.floor(venda.total / 10)}\n`;
      }
      
      return cupom;
    },
    imprimirCupom() {
      // Implementação da impressão térmica
      window.print();
    }
  }
}
</script>
