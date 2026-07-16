# Sistema para Controle de Estoque

Trabalho da faculdade em Python para gerenciar entrada, saida e saldo de
produtos em estoque.

## Divisao do grupo

- Backend (banco de dados, regras do sistema e API): *(seu nome)* - pasta `backend/`
- Frontend (HTML/CSS, consome a API): *(nome do colega)*
- *(terceira pessoa, se tiver)*: *(nome)*

## O que o sistema faz

- Cadastro de produtos e categorias
- Controle de movimentacoes (entrada/saida)
- Calculo automatico de saldo
- Alerta de estoque minimo
- Relatorio de inventario e movimentacao
- Persistencia em banco de dados (SQLite)

## Tecnologias

- Python 3
- SQLite (ja vem com o python)
- Flask, pra expor o backend como API pro frontend consumir
- HTML/CSS + JavaScript no frontend

## Como rodar o backend

```bash
git clone <url-do-repo>
cd estoque-backend

python3 -m venv venv
source venv/bin/activate   # windows: venv\Scripts\activate

pip install -r requirements.txt

python -m backend.api
```

O sistema sobe em `http://localhost:5000`. Deixa rodando nesse terminal
e abre esse endereco no navegador. O Flask entrega o frontend e tambem
responde as requisicoes da API.

Pra testar sem o frontend, roda os testes:

```bash
python -m unittest discover tests -v
```

## Estrutura

```
estoque-backend/
├── backend/
│   ├── database.py       -> cria e conecta no banco
│   ├── produtos.py       -> cadastro de categoria e produto
│   ├── movimentacoes.py  -> entrada, saida, saldo, alerta de estoque
│   ├── relatorios.py     -> relatorio de estoque e de movimentacoes
│   └── api.py            -> rotas Flask que o frontend consome
├── tests/
│   └── test_estoque.py
├── main_exemplo.py
├── requirements.txt
└── README.md
```

`produtos.py`, `movimentacoes.py` e `relatorios.py` tem so funcoes Python
normais, sem depender de Flask. O `api.py` e a unica camada que sabe que
existe HTTP - ele só chama essas funcoes e devolve o resultado em JSON.
Isso facilita pra testar a logica sozinha (é o que o `main_exemplo.py` e
os testes fazem) sem precisar da API rodando.

## Rotas da API

| Metodo | Rota | O que faz |
|---|---|---|
| GET | /categorias | lista categorias |
| POST | /categorias | cria categoria `{nome, descricao}` |
| GET | /produtos | lista produtos |
| GET | /produtos/\<id> | busca um produto |
| POST | /produtos | cria produto `{nome, categoria_id, preco, quantidade, estoque_minimo}` |
| DELETE | /produtos/\<id> | remove produto |
| POST | /produtos/\<id>/entrada | registra entrada `{quantidade, observacao}` |
| POST | /produtos/\<id>/saida | registra saida `{quantidade, observacao}` |
| GET | /produtos/\<id>/saldo | saldo atual |
| GET | /produtos/\<id>/historico | movimentacoes daquele produto |
| GET | /produtos-estoque-baixo | produtos em alerta |
| GET | /dashboard | totais de entradas e saidas |
| GET | /relatorio/estoque | relatorio de inventario |
| GET | /relatorio/movimentacoes | relatorio de movimentacoes |

Em erro (produto nao encontrado, estoque insuficiente, dado invalido),
a API responde com status 400, 404 ou 409 e um JSON `{"erro": "mensagem"}`.
Um produto que ja possui movimentacoes nao pode ser excluido, pois seu
historico precisa continuar salvo.

## Exemplo de como o frontend chama a API

```javascript
fetch("http://localhost:5000/produtos")
  .then(res => res.json())
  .then(produtos => console.log(produtos));

fetch("http://localhost:5000/produtos/1/entrada", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ quantidade: 10, observacao: "compra" })
})
  .then(res => res.json())
  .then(dados => {
    if (dados.erro) {
      alert(dados.erro);
    } else {
      console.log("novo saldo:", dados.saldo);
    }
  });
```
