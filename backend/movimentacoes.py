from datetime import datetime
from backend.database import conectar
from backend.exceptions import (
    DadosInvalidosError,
    EstoqueInsuficienteError,
    ProdutoNaoEncontradoError,
)


def _validar_quantidade(quantidade):
    if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade <= 0:
        raise DadosInvalidosError("quantidade deve ser um numero inteiro maior que zero")


def _buscar_produto(conn, produto_id):
    produto = conn.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (produto_id,)
    ).fetchone()
    if produto is None:
        raise ProdutoNaoEncontradoError("produto nao encontrado")
    return produto


def registrar_entrada(produto_id, quantidade, observacao=""):
    _validar_quantidade(quantidade)
    if not isinstance(observacao, str):
        raise DadosInvalidosError("observacao deve ser um texto")
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = conectar()
    try:
        produto = _buscar_produto(conn, produto_id)
        novo_saldo = produto["quantidade"] + quantidade
        conn.execute(
            "INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao, data_hora) VALUES (?, ?, ?, ?, ?)",
            (produto_id, "ENTRADA", quantidade, observacao.strip(), data_hora)
        )
        conn.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_saldo, produto_id))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def registrar_saida(produto_id, quantidade, observacao=""):
    _validar_quantidade(quantidade)
    if not isinstance(observacao, str):
        raise DadosInvalidosError("observacao deve ser um texto")
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = conectar()
    try:
        produto = _buscar_produto(conn, produto_id)
        if quantidade > produto["quantidade"]:
            raise EstoqueInsuficienteError("estoque insuficiente")

        novo_saldo = produto["quantidade"] - quantidade
        conn.execute(
            "INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao, data_hora) VALUES (?, ?, ?, ?, ?)",
            (produto_id, "SAIDA", quantidade, observacao.strip(), data_hora)
        )
        conn.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_saldo, produto_id))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def consultar_saldo(produto_id):
    conn = conectar()
    try:
        return _buscar_produto(conn, produto_id)["quantidade"]
    finally:
        conn.close()


def produtos_estoque_baixo():
    conn = conectar()
    linhas = conn.execute("SELECT * FROM produtos").fetchall()
    conn.close()

    resultado = []
    for produto in linhas:
        if produto["quantidade"] <= produto["estoque_minimo"]:
            resultado.append(produto)
    return resultado


def historico_produto(produto_id):
    conn = conectar()
    try:
        _buscar_produto(conn, produto_id)
        return conn.execute(
            "SELECT * FROM movimentacoes WHERE produto_id = ? ORDER BY data_hora DESC",
            (produto_id,)
        ).fetchall()
    finally:
        conn.close()


def resumo_movimentacoes():
    conn = conectar()

    entradas = conn.execute("""
        SELECT COUNT(*) AS total
        FROM movimentacoes
        WHERE tipo = 'ENTRADA'
    """).fetchone()["total"]

    saidas = conn.execute("""
        SELECT COUNT(*) AS total
        FROM movimentacoes
        WHERE tipo = 'SAIDA'
    """).fetchone()["total"]

    conn.close()

    return {
        "entradas": entradas,
        "saidas": saidas
    }
