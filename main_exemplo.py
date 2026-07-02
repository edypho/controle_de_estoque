from backend.database import criar_tabelas
from backend import produtos, movimentacoes, relatorios

criar_tabelas()

categoria_id = produtos.cadastrar_categoria("Mercearia", "produtos de mercearia em geral")
print("categoria criada, id:", categoria_id)

produto_id = produtos.cadastrar_produto(
    nome="Arroz 5kg",
    categoria_id=categoria_id,
    preco=25.90,
    quantidade=0,
    estoque_minimo=10,
)
print("produto criado, id:", produto_id)

movimentacoes.registrar_entrada(produto_id, 50, "compra inicial")
movimentacoes.registrar_saida(produto_id, 45, "venda balcao")

print("saldo atual:", movimentacoes.consultar_saldo(produto_id))

try:
    movimentacoes.registrar_saida(produto_id, 1000)
except Exception as erro:
    print("deu erro como esperado:", erro)

baixo = movimentacoes.produtos_estoque_baixo()
print("produtos em alerta:", [p["nome"] for p in baixo])

print()
print("relatorio de estoque:")
for item in relatorios.relatorio_estoque():
    print(item)

print()
print("relatorio de movimentacoes:")
for item in relatorios.relatorio_movimentacoes():
    print(item)
