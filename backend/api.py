import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.database import criar_tabelas
from backend import produtos, movimentacoes, relatorios
from backend.exceptions import (
    CategoriaDuplicadaError,
    CategoriaNaoEncontradaError,
    DadosInvalidosError,
    EstoqueInsuficienteError,
    ProdutoNaoEncontradoError,
)

PASTA_FRONTEND = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "frontend"
)

app = Flask(
    __name__,
    static_folder=PASTA_FRONTEND,
    static_url_path=""
)
CORS(app)

criar_tabelas()


def linha_para_dict(linha):
    return dict(linha)


def ler_json():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise DadosInvalidosError("envie os dados no formato JSON")
    return dados


@app.errorhandler(DadosInvalidosError)
@app.errorhandler(CategoriaDuplicadaError)
@app.errorhandler(CategoriaNaoEncontradaError)
@app.errorhandler(EstoqueInsuficienteError)
def erro_dados_invalidos(erro):
    return jsonify({"erro": str(erro)}), 400


@app.errorhandler(ProdutoNaoEncontradoError)
def erro_nao_encontrado(erro):
    return jsonify({"erro": str(erro)}), 404


@app.route("/")
def pagina_inicial():
    return app.send_static_file("index.html")


@app.route("/categorias", methods=["GET"])
def get_categorias():
    linhas = produtos.listar_categorias()
    return jsonify([linha_para_dict(l) for l in linhas])


@app.route("/categorias", methods=["POST"])
def post_categoria():
    dados = ler_json()
    novo_id = produtos.cadastrar_categoria(dados.get("nome", ""), dados.get("descricao", ""))
    return jsonify({"id": novo_id}), 201


@app.route("/produtos", methods=["GET"])
def get_produtos():
    linhas = produtos.listar_produtos()
    return jsonify([linha_para_dict(l) for l in linhas])


@app.route("/produtos/<int:produto_id>", methods=["GET"])
def get_produto(produto_id):
    linha = produtos.buscar_produto(produto_id)
    return jsonify(linha_para_dict(linha))


@app.route("/produtos", methods=["POST"])
def post_produto():
    dados = ler_json()
    novo_id = produtos.cadastrar_produto(
        nome=dados.get("nome", ""),
        categoria_id=dados.get("categoria_id"),
        preco=dados.get("preco", 0),
        quantidade=dados.get("quantidade", 0),
        estoque_minimo=dados.get("estoque_minimo", 0),
    )
    return jsonify({"id": novo_id}), 201


@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def delete_produto(produto_id):
    produtos.remover_produto(produto_id)
    return jsonify({"mensagem": "produto removido"})


@app.route("/produtos/<int:produto_id>/entrada", methods=["POST"])
def post_entrada(produto_id):
    dados = ler_json()
    movimentacoes.registrar_entrada(produto_id, dados.get("quantidade", 0), dados.get("observacao", ""))
    return jsonify({"saldo": movimentacoes.consultar_saldo(produto_id)})


@app.route("/produtos/<int:produto_id>/saida", methods=["POST"])
def post_saida(produto_id):
    dados = ler_json()
    movimentacoes.registrar_saida(produto_id, dados.get("quantidade", 0), dados.get("observacao", ""))
    return jsonify({"saldo": movimentacoes.consultar_saldo(produto_id)})


@app.route("/produtos/<int:produto_id>/saldo", methods=["GET"])
def get_saldo(produto_id):
    return jsonify({"saldo": movimentacoes.consultar_saldo(produto_id)})


@app.route("/produtos/<int:produto_id>/historico", methods=["GET"])
def get_historico(produto_id):
    linhas = movimentacoes.historico_produto(produto_id)
    return jsonify([linha_para_dict(l) for l in linhas])


@app.route("/produtos-estoque-baixo", methods=["GET"])
def get_estoque_baixo():
    linhas = movimentacoes.produtos_estoque_baixo()
    return jsonify([linha_para_dict(l) for l in linhas])

@app.route("/dashboard", methods=["GET"])
def get_dashboard():
    return jsonify(movimentacoes.resumo_movimentacoes())

@app.route("/relatorio/estoque", methods=["GET"])
def get_relatorio_estoque():
    return jsonify(relatorios.relatorio_estoque())


@app.route("/relatorio/movimentacoes", methods=["GET"])
def get_relatorio_movimentacoes():
    return jsonify(relatorios.relatorio_movimentacoes())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
