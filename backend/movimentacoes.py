from datetime import datetime

from backend.database import conectar
from backend.produtos import buscar_produto


def registrar_entrada(produto_id, quantidade, observacao=""):
    if quantidade <= 0:
        raise Exception("quantidade tem que ser maior que zero")

    produto = buscar_produto(produto_id)

    saldo_anterior = produto["quantidade"]
    saldo_atual = saldo_anterior + quantidade

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = conectar()

    conn.execute(
        """
        INSERT INTO movimentacoes (
            produto_id,
            tipo,
            quantidade,
            observacao,
            data_hora,
            saldo_anterior,
            saldo_atual
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            produto_id,
            "ENTRADA",
            quantidade,
            observacao,
            data_hora,
            saldo_anterior,
            saldo_atual,
        ),
    )

    conn.execute(
        "UPDATE produtos SET quantidade = ? WHERE id = ?",
        (saldo_atual, produto_id),
    )

    conn.commit()
    conn.close()


def registrar_saida(produto_id, quantidade, observacao=""):
    if quantidade <= 0:
        raise Exception("quantidade tem que ser maior que zero")

    produto = buscar_produto(produto_id)

    if quantidade > produto["quantidade"]:
        raise Exception("estoque insuficiente")

    saldo_anterior = produto["quantidade"]
    saldo_atual = saldo_anterior - quantidade

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = conectar()

    conn.execute(
        """
        INSERT INTO movimentacoes (
            produto_id,
            tipo,
            quantidade,
            observacao,
            data_hora,
            saldo_anterior,
            saldo_atual
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            produto_id,
            "SAIDA",
            quantidade,
            observacao,
            data_hora,
            saldo_anterior,
            saldo_atual,
        ),
    )

    conn.execute(
        "UPDATE produtos SET quantidade = ? WHERE id = ?",
        (saldo_atual, produto_id),
    )

    conn.commit()
    conn.close()


def consultar_saldo(produto_id):
    produto = buscar_produto(produto_id)
    return produto["quantidade"]


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

    linhas = conn.execute(
        """
        SELECT *
        FROM movimentacoes
        WHERE produto_id = ?
        ORDER BY data_hora DESC
        """,
        (produto_id,),
    ).fetchall()

    conn.close()
    return linhas