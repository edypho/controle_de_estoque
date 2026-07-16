# Sistema para Controle de Estoque

Projeto acadêmico desenvolvido para a disciplina de Análise e Desenvolvimento de Sistemas (ADS). O sistema permite cadastrar produtos e categorias, controlar entradas e saídas e acompanhar o saldo disponível em estoque.

## Objetivo do projeto

Desenvolver um sistema que apresente:

- Cadastro de produtos e categorias;
- Controle de movimentações de entrada e saída;
- Cálculo automático do saldo;
- Alerta lógico de estoque mínimo;
- Relatórios de inventário e movimentações;
- Persistência dos dados em banco de dados.

## Tecnologias utilizadas

- **Python:** regras do sistema e API;
- **Flask:** comunicação entre o frontend e o backend;
- **SQLite:** armazenamento dos dados;
- **HTML:** estrutura das páginas;
- **CSS:** aparência e organização visual;
- **JavaScript:** interação com as páginas e consumo da API.

O funcionamento geral é:

```text
HTML/CSS/JavaScript -> API Flask/Python -> SQLite
```

## Funcionalidades

- Cadastro e listagem de categorias;
- Cadastro, listagem e inativação de produtos;
- Pesquisa de produtos e categorias;
- Registro de entradas e saídas;
- Proteção contra saída maior que o saldo disponível;
- Atualização automática da quantidade em estoque;
- Registro do saldo anterior e do saldo atual de cada movimentação;
- Identificação de produtos com estoque baixo;
- Histórico individual de cada produto;
- Dashboard com totais de produtos, entradas, saídas e estoque baixo;
- Relatório do inventário atual;
- Relatório geral de movimentações;
- Preservação do histórico quando um produto é removido.

## Requisitos

Antes de executar o projeto, é necessário ter instalado:

- Python 3;
- Git, caso o projeto seja clonado do GitHub;
- Um navegador atualizado.

O SQLite não precisa ser instalado separadamente, pois já faz parte do Python.

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/edypho/controle_de_estoque.git
cd controle_de_estoque
```

Crie um ambiente virtual.

No Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

No Linux ou macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Com o ambiente virtual ativado, execute:

```bash
python -m backend.api
```

Depois, acesse no navegador:

```text
http://127.0.0.1:5000
```

O Flask entrega as páginas do frontend e também responde às requisições da API.

## Dados para demonstração

O projeto possui um arquivo que cadastra categorias, produtos e movimentações de exemplo. Para utilizá-lo, execute:

```bash
python -m backend.seed
```

O seed pode ser executado novamente. Os dados de demonstração são identificados para evitar a repetição das mesmas movimentações.

Depois, inicie o sistema normalmente:

```bash
python -m backend.api
```

## Telas do sistema

- **Dashboard:** apresenta os totais e os produtos recentes;
- **Produtos:** permite cadastrar, pesquisar, movimentar e remover produtos;
- **Categorias:** permite cadastrar, listar e pesquisar categorias;
- **Relatórios:** apresenta o inventário e o histórico geral de movimentações;
- **Histórico:** pode ser aberto pelo botão disponível em cada produto.

## Regras de negócio

- O nome da categoria e do produto não pode ficar vazio;
- O preço, a quantidade inicial e o estoque mínimo não podem ser negativos;
- As quantidades movimentadas precisam ser números inteiros maiores que zero;
- Uma saída não pode ser maior que o saldo disponível;
- Toda movimentação registra saldo anterior e saldo atual;
- Um produto está com estoque baixo quando sua quantidade é menor ou igual ao estoque mínimo;
- Produtos removidos são apenas inativados e deixam de aparecer nas listagens;
- O histórico de um produto inativado permanece salvo no banco.

## Estrutura do projeto

```text
controle_de_estoque/
|-- backend/
|   |-- api.py              # Rotas Flask e entrega do frontend
|   |-- database.py         # Conexão, tabelas e atualização do banco
|   |-- exceptions.py       # Erros conhecidos do sistema
|   |-- movimentacoes.py    # Entradas, saídas, saldo e histórico
|   |-- produtos.py         # Categorias e produtos
|   |-- relatorios.py       # Relatórios do sistema
|   `-- seed.py             # Dados para demonstração
|-- frontend/
|   |-- css/style.css       # Estilos e cores
|   |-- js/                 # Comunicação com a API e ações das páginas
|   |-- index.html          # Dashboard
|   |-- produtos.html       # Produtos e movimentações
|   |-- categorias.html     # Categorias
|   `-- relatorios.html     # Relatórios
|-- tests/
|   |-- test_api.py         # Testes das rotas e do frontend
|   |-- test_database.py    # Teste de atualização do banco
|   `-- test_estoque.py     # Testes das regras de estoque
|-- docs/                   # Documentação complementar
|-- requirements.txt        # Dependências Python
`-- README.md
```

## Banco de dados

O arquivo `estoque.db` é criado automaticamente na primeira execução. O sistema utiliza três tabelas principais:

- `categorias`;
- `produtos`;
- `movimentacoes`.

Quando uma versão antiga do banco é encontrada, as novas colunas são adicionadas sem apagar os registros existentes.

A modelagem completa está em [docs/modelagem_banco.md](docs/modelagem_banco.md).

## Rotas da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Abre o dashboard |
| GET | `/categorias` | Lista as categorias ativas |
| POST | `/categorias` | Cadastra uma categoria |
| GET | `/produtos` | Lista os produtos ativos |
| GET | `/produtos/<id>` | Busca um produto |
| POST | `/produtos` | Cadastra um produto |
| DELETE | `/produtos/<id>` | Inativa um produto |
| POST | `/produtos/<id>/entrada` | Registra uma entrada |
| POST | `/produtos/<id>/saida` | Registra uma saída |
| GET | `/produtos/<id>/saldo` | Consulta o saldo atual |
| GET | `/produtos/<id>/historico` | Lista o histórico do produto |
| GET | `/produtos-estoque-baixo` | Lista produtos com estoque baixo |
| GET | `/dashboard` | Retorna os totais do dashboard |
| GET | `/relatorio/estoque` | Retorna o inventário atual |
| GET | `/relatorio/movimentacoes` | Retorna todas as movimentações |

### Exemplos de requisições

Cadastro de categoria:

```json
{
  "nome": "Periféricos",
  "descricao": "Teclados, mouses e acessórios"
}
```

Cadastro de produto:

```json
{
  "nome": "Teclado Mecânico",
  "categoria_id": 1,
  "preco": 199.90,
  "quantidade": 10,
  "estoque_minimo": 3
}
```

Entrada ou saída:

```json
{
  "quantidade": 5,
  "observacao": "Compra do fornecedor"
}
```

Quando ocorre um erro conhecido, a API retorna uma resposta semelhante a:

```json
{
  "erro": "mensagem explicando o problema"
}
```

## Testes

Para executar todos os testes:

```bash
python -m unittest discover tests -v
```

Os testes verificam:

- Cadastro de categorias e produtos;
- Entradas, saídas e cálculo do saldo;
- Estoque insuficiente e dados inválidos;
- Inativação e preservação do histórico;
- Rotas da API e entrega do frontend;
- Migração de uma versão antiga do banco.

## Documentação complementar

- [Documentação do backend](docs/documentacao_backend.md)
- [Modelagem do banco de dados](docs/modelagem_banco.md)
