# Documentacao do backend

O backend foi dividido em arquivos dentro da pasta backend, cada um
cuidando de uma parte do sistema.

database.py cria o banco SQLite e as tabelas categorias, produtos e
movimentacoes. Tem a funcao conectar() que abre uma conexao nova toda vez
que alguma outra funcao precisa mexer no banco, e criar_tabelas() que
precisa ser chamada uma vez quando o programa abre.

produtos.py tem as funcoes de cadastro: cadastrar_categoria,
listar_categorias, cadastrar_produto, listar_produtos, buscar_produto e
remover_produto. Antes de cadastrar um produto ele confere se a categoria
existe e se os valores (preco, quantidade) fazem sentido.

movimentacoes.py cuida de entrada e saida de produto no estoque.
registrar_entrada soma a quantidade no saldo do produto, registrar_saida
subtrai (e nao deixa subtrair mais do que tem disponivel, da erro se
tentar). consultar_saldo devolve a quantidade atual e
produtos_estoque_baixo devolve os produtos que ja bateram no estoque
minimo cadastrado.

relatorios.py tem duas funcoes que devolvem os dados prontos em formato
de dicionario: relatorio_estoque (situacao atual de cada produto, com
valor total em estoque) e relatorio_movimentacoes (historico de tudo que
entrou e saiu).

api.py e a camada nova, adicionada quando o grupo decidiu que o frontend
ia ser em HTML/CSS. Ela usa Flask pra transformar as funcoes dos outros
arquivos em rotas HTTP, entao o frontend consegue chamar o backend com
fetch() do JavaScript em vez de importar Python direto. Cada rota so
chama a funcao correspondente e devolve o resultado em JSON; quem da
erro (produto nao encontrado, estoque insuficiente) volta como
`{"erro": "..."}` com status 400 ou 404.

## Tabelas do banco

categorias: id, nome, descricao

produtos: id, nome, categoria_id, preco, quantidade, estoque_minimo

movimentacoes: id, produto_id, tipo (ENTRADA ou SAIDA), quantidade,
observacao, data_hora

## Regras que o sistema segue

Nao deixa cadastrar produto com nome vazio, preco negativo ou
quantidade/estoque minimo negativo. Nao deixa registrar movimentacao com
quantidade zero ou negativa. Uma saida nunca pode deixar o saldo
negativo. O saldo e recalculado toda vez que tem uma movimentacao nova.
Um produto fica em alerta quando a quantidade e menor ou igual ao
estoque minimo cadastrado pra ele.

## Rodando

Backend sozinho, sem API (pra testar a logica):

python main_exemplo.py

Testes:

python -m unittest discover tests -v

API pro frontend consumir:

python -m backend.api

Isso sobe o servidor em http://localhost:5000. As rotas disponiveis
estao listadas no README.md da raiz do projeto.
