from backend.database import conectar


def cadastrar_categoria(nome, descricao=""):
    if nome.strip() == "":
        raise Exception("nome da categoria nao pode ser vazio")

    conn = conectar()

    cursor = conn.execute(
        "INSERT INTO categorias (nome, descricao) VALUES (?, ?)",
        (nome, descricao)
    )

    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    return novo_id


def listar_categorias():
    conn = conectar()

    linhas = conn.execute(
        """
        SELECT *
        FROM categorias
        WHERE ativo = 1
        ORDER BY nome
        """
    ).fetchall()

    conn.close()
    return linhas


def cadastrar_produto(nome, categoria_id, preco, quantidade=0, estoque_minimo=0):
    if nome.strip() == "":
        raise Exception("nome do produto nao pode ser vazio")

    if preco < 0:
        raise Exception("preco nao pode ser negativo")

    if quantidade < 0 or estoque_minimo < 0:
        raise Exception("quantidade nao pode ser negativa")

    conn = conectar()

    categoria = conn.execute(
        "SELECT id FROM categorias WHERE id = ? AND ativo = 1",
        (categoria_id,)
    ).fetchone()

    if categoria is None:
        conn.close()
        raise Exception("categoria nao encontrada")

    cursor = conn.execute(
        """
        INSERT INTO produtos (
            nome,
            categoria_id,
            preco,
            quantidade,
            estoque_minimo
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (nome, categoria_id, preco, quantidade, estoque_minimo)
    )

    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    return novo_id


def listar_produtos():
    conn = conectar()

    linhas = conn.execute(
        """
        SELECT *
        FROM produtos
        WHERE ativo = 1
        ORDER BY nome
        """
    ).fetchall()

    conn.close()
    return linhas


def buscar_produto(produto_id):
    conn = conectar()

    linha = conn.execute(
        """
        SELECT *
        FROM produtos
        WHERE id = ? AND ativo = 1
        """,
        (produto_id,)
    ).fetchone()

    conn.close()

    if linha is None:
        raise Exception("produto nao encontrado")

    return linha


def remover_produto(produto_id):
    buscar_produto(produto_id)

    conn = conectar()

    conn.execute(
        """
        UPDATE produtos
        SET ativo = 0
        WHERE id = ?
        """,
        (produto_id,)
    )

    conn.commit()
    conn.close()