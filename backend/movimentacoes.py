from datetime import datetime

from backend.database import conectar
from backend.exceptions import (
    DadosInvalidosError,
    EstoqueInsuficienteError,
    ProdutoNaoEncontradoError,
)


def _validar_quantidade(quantidade):
    if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade <= 0:
        raise DadosInvalidosError(
            "quantidade deve ser um numero inteiro maior que zero"
        )


def _buscar_produto(conn, produto_id):
    produto = conn.execute(
        "SELECT * FROM produtos WHERE id = ? AND ativo = 1",
        (produto_id,)
    ).fetchone()
    if produto is None:
        raise ProdutoNaoEncontradoError("produto nao encontrado")
    return produto


def _registrar_movimentacao(produto_id, tipo, quantidade, observacao):
    _validar_quantidade(quantidade)
    if not isinstance(observacao, str):
        raise DadosInvalidosError("observacao deve ser um texto")

    conn = conectar()
    try:
        produto = _buscar_produto(conn, produto_id)
        saldo_anterior = produto["quantidade"]

        if tipo == "SAIDA" and quantidade > saldo_anterior:
            raise EstoqueInsuficienteError("estoque insuficiente")

        if tipo == "ENTRADA":
            saldo_atual = saldo_anterior + quantidade
        else:
            saldo_atual = saldo_anterior - quantidade

        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn.execute(
            """
            INSERT INTO movimentacoes (
                produto_id, tipo, quantidade, observacao, data_hora,
                saldo_anterior, saldo_atual
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                produto_id,
                tipo,
                quantidade,
                observacao.strip(),
                data_hora,
                saldo_anterior,
                saldo_atual,
            )
        )
        conn.execute(
            "UPDATE produtos SET quantidade = ? WHERE id = ?",
            (saldo_atual, produto_id)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def registrar_entrada(produto_id, quantidade, observacao=""):
    _registrar_movimentacao(produto_id, "ENTRADA", quantidade, observacao)


def registrar_saida(produto_id, quantidade, observacao=""):
    _registrar_movimentacao(produto_id, "SAIDA", quantidade, observacao)


def consultar_saldo(produto_id):
    conn = conectar()
    try:
        return _buscar_produto(conn, produto_id)["quantidade"]
    finally:
        conn.close()


def produtos_estoque_baixo():
    conn = conectar()
    linhas = conn.execute(
        "SELECT * FROM produtos WHERE ativo = 1"
    ).fetchall()
    conn.close()

    return [
        produto
        for produto in linhas
        if produto["quantidade"] <= produto["estoque_minimo"]
    ]


def historico_produto(produto_id):
    conn = conectar()
    try:
        _buscar_produto(conn, produto_id)
        return conn.execute(
            """
            SELECT * FROM movimentacoes
            WHERE produto_id = ?
            ORDER BY data_hora DESC, id DESC
            """,
            (produto_id,)
        ).fetchall()
    finally:
        conn.close()


def resumo_movimentacoes():
    conn = conectar()
    entradas = conn.execute(
        "SELECT COUNT(*) AS total FROM movimentacoes WHERE tipo = 'ENTRADA'"
    ).fetchone()["total"]
    saidas = conn.execute(
        "SELECT COUNT(*) AS total FROM movimentacoes WHERE tipo = 'SAIDA'"
    ).fetchone()["total"]
    conn.close()

    return {"entradas": entradas, "saidas": saidas}
