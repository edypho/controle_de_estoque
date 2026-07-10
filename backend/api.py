from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.database import criar_tabelas
from backend import produtos, movimentacoes, relatorios

app = Flask(__name__)
CORS(app)

criar_tabelas()


def linha_para_dict(linha):
    return dict(linha)


@app.route("/categorias", methods=["GET"])
def get_categorias():
    linhas = produtos.listar_categorias()
    return jsonify([linha_para_dict(l) for l in linhas])


@app.route("/categorias", methods=["POST"])
def post_categoria():
    dados = request.get_json()
    try:
        novo_id = produtos.cadastrar_categoria(dados.get("nome", ""), dados.get("descricao", ""))
        return jsonify({"id": novo_id}), 201
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 400


@app.route("/produtos", methods=["GET"])
def get_produtos():
    linhas = produtos.listar_produtos()
    return jsonify([linha_para_dict(l) for l in linhas])


@app.route("/produtos/<int:produto_id>", methods=["GET"])
def get_produto(produto_id):
    try:
        linha = produtos.buscar_produto(produto_id)
        return jsonify(linha_para_dict(linha))
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 404


@app.route("/produtos", methods=["POST"])
def post_produto():
    dados = request.get_json()
    try:
        novo_id = produtos.cadastrar_produto(
            nome=dados.get("nome", ""),
            categoria_id=dados.get("categoria_id"),
            preco=dados.get("preco", 0),
            quantidade=dados.get("quantidade", 0),
            estoque_minimo=dados.get("estoque_minimo", 0),
        )
        return jsonify({"id": novo_id}), 201
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 400


@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def delete_produto(produto_id):
    try:
        produtos.remover_produto(produto_id)
        return jsonify({"mensagem": "produto removido"})
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 404


@app.route("/produtos/<int:produto_id>/entrada", methods=["POST"])
def post_entrada(produto_id):
    dados = request.get_json()
    try:
        movimentacoes.registrar_entrada(produto_id, dados.get("quantidade", 0), dados.get("observacao", ""))
        return jsonify({"saldo": movimentacoes.consultar_saldo(produto_id)})
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 400


@app.route("/produtos/<int:produto_id>/saida", methods=["POST"])
def post_saida(produto_id):
    dados = request.get_json()
    try:
        movimentacoes.registrar_saida(produto_id, dados.get("quantidade", 0), dados.get("observacao", ""))
        return jsonify({"saldo": movimentacoes.consultar_saldo(produto_id)})
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 400


@app.route("/produtos/<int:produto_id>/saldo", methods=["GET"])
def get_saldo(produto_id):
    try:
        return jsonify({"saldo": movimentacoes.consultar_saldo(produto_id)})
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 404


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
