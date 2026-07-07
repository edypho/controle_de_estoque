from backend.database import conectar


def relatorio_estoque():
    conn = conectar()

    produtos = conn.execute(
        """
        SELECT *
        FROM produtos
        WHERE ativo = 1
        ORDER BY nome
        """
    ).fetchall()

    conn.close()

    lista = []

    for produto in produtos:
        lista.append({
            "id": produto["id"],
            "nome": produto["nome"],
            "quantidade": produto["quantidade"],
            "preco": produto["preco"],
            "valor_total": round(produto["quantidade"] * produto["preco"], 2),
            "estoque_minimo": produto["estoque_minimo"],
            "abaixo_do_minimo": produto["quantidade"] <= produto["estoque_minimo"],
        })

    return lista


def relatorio_movimentacoes():
    conn = conectar()

    movimentacoes = conn.execute(
        """
        SELECT *
        FROM movimentacoes
        ORDER BY data_hora DESC
        """
    ).fetchall()

    conn.close()

    lista = []

    for m in movimentacoes:
        lista.append({
            "id": m["id"],
            "produto_id": m["produto_id"],
            "tipo": m["tipo"],
            "quantidade": m["quantidade"],
            "observacao": m["observacao"],
            "data_hora": m["data_hora"],
            "saldo_anterior": m["saldo_anterior"],
            "saldo_atual": m["saldo_atual"],
        })

    return lista