# Modelagem do Banco de Dados

Este documento descreve a estrutura do banco de dados do sistema de controle de estoque.

O sistema utiliza SQLite e foi modelado para controlar produtos, categorias e movimentações de estoque, mantendo histórico das entradas e saídas realizadas.

---

## Tabelas do sistema

### categorias

A tabela `categorias` armazena os grupos usados para organizar os produtos.

Campos principais:

- `id`: identificador único da categoria;
- `nome`: nome da categoria;
- `descricao`: descrição opcional;
- `ativo`: indica se a categoria está ativa;
- `criado_em`: data de criação do registro.

---

### produtos

A tabela `produtos` armazena os produtos cadastrados no estoque.

Campos principais:

- `id`: identificador único do produto;
- `nome`: nome do produto;
- `descricao`: descrição opcional;
- `sku`: código interno do produto;
- `fornecedor`: fornecedor do produto;
- `categoria_id`: categoria relacionada ao produto;
- `preco`: preço unitário;
- `quantidade`: quantidade atual em estoque;
- `estoque_minimo`: quantidade mínima recomendada;
- `ativo`: indica se o produto está ativo;
- `criado_em`: data de criação do registro.

O campo `categoria_id` é uma chave estrangeira que referencia a tabela `categorias`.

---

### movimentacoes

A tabela `movimentacoes` registra todas as entradas e saídas de estoque.

Campos principais:

- `id`: identificador único da movimentação;
- `produto_id`: produto movimentado;
- `tipo`: tipo da movimentação, podendo ser `ENTRADA` ou `SAIDA`;
- `quantidade`: quantidade movimentada;
- `observacao`: observação opcional;
- `data_hora`: data e hora da movimentação;
- `saldo_anterior`: quantidade do produto antes da movimentação;
- `saldo_atual`: quantidade do produto depois da movimentação.

O campo `produto_id` é uma chave estrangeira que referencia a tabela `produtos`.

---

## Regras de negócio

- Todo produto deve pertencer a uma categoria ativa.
- O preço do produto não pode ser negativo.
- A quantidade inicial do produto não pode ser negativa.
- O estoque mínimo não pode ser negativo.
- Toda entrada de estoque aumenta a quantidade atual do produto.
- Toda saída de estoque diminui a quantidade atual do produto.
- Não é permitido realizar saída maior que o saldo disponível.
- Toda entrada ou saída gera um registro na tabela `movimentacoes`.
- Cada movimentação salva o saldo anterior e o saldo atual.
- Produtos não são apagados fisicamente do banco.
- Quando um produto é removido, ele é apenas inativado usando o campo `ativo = 0`.
- Produtos inativos não aparecem nas listagens normais.
- O histórico de movimentações é preservado mesmo após a inativação do produto.
- Produtos com quantidade menor ou igual ao estoque mínimo aparecem como estoque baixo.

---

## Diagrama simplificado

```mermaid
erDiagram
    CATEGORIAS ||--o{ PRODUTOS : possui
    PRODUTOS ||--o{ MOVIMENTACOES : gera

    CATEGORIAS {
        int id
        string nome
        string descricao
        int ativo
        string criado_em
    }

    PRODUTOS {
        int id
        string nome
        string descricao
        string sku
        string fornecedor
        int categoria_id
        float preco
        int quantidade
        int estoque_minimo
        int ativo
        string criado_em
    }

    MOVIMENTACOES {
        int id
        int produto_id
        string tipo
        int quantidade
        string observacao
        string data_hora
        int saldo_anterior
        int saldo_atual
    }