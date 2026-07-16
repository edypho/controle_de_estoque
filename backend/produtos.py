import sqlite3

from backend.database import conectar
from backend.exceptions import (
    CategoriaDuplicadaError,
    CategoriaNaoEncontradaError,
    DadosInvalidosError,
    ProdutoComMovimentacaoError,
    ProdutoNaoEncontradoError,
)


def _inteiro_nao_negativo(valor, nome_campo):
    if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
        raise DadosInvalidosError(f"{nome_campo} deve ser um numero inteiro maior ou igual a zero")


def _numero_nao_negativo(valor, nome_campo):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor < 0:
        raise DadosInvalidosError(f"{nome_campo} deve ser um numero maior ou igual a zero")


def cadastrar_categoria(nome, descricao=""):
    if not isinstance(nome, str) or nome.strip() == "":
        raise DadosInvalidosError("nome da categoria nao pode ser vazio")
    if not isinstance(descricao, str):
        raise DadosInvalidosError("descricao da categoria deve ser um texto")

    conn = conectar()
    try:
        cursor = conn.execute(
            "INSERT INTO categorias (nome, descricao) VALUES (?, ?)",
            (nome.strip(), descricao.strip())
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.rollback()
        raise CategoriaDuplicadaError("ja existe uma categoria com esse nome")
    finally:
        conn.close()


def listar_categorias():
    conn = conectar()
    linhas = conn.execute("SELECT * FROM categorias ORDER BY nome").fetchall()
    conn.close()
    return linhas


def cadastrar_produto(nome, categoria_id, preco, quantidade=0, estoque_minimo=0):
    if not isinstance(nome, str) or nome.strip() == "":
        raise DadosInvalidosError("nome do produto nao pode ser vazio")
    if isinstance(categoria_id, bool) or not isinstance(categoria_id, int):
        raise DadosInvalidosError("categoria_id deve ser um numero inteiro")

    _numero_nao_negativo(preco, "preco")
    _inteiro_nao_negativo(quantidade, "quantidade")
    _inteiro_nao_negativo(estoque_minimo, "estoque_minimo")

    conn = conectar()
    categoria = conn.execute("SELECT id FROM categorias WHERE id = ?", (categoria_id,)).fetchone()
    if categoria is None:
        conn.close()
        raise CategoriaNaoEncontradaError("categoria nao encontrada")

    cursor = conn.execute(
        "INSERT INTO produtos (nome, categoria_id, preco, quantidade, estoque_minimo) VALUES (?, ?, ?, ?, ?)",
        (nome.strip(), categoria_id, preco, quantidade, estoque_minimo)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id


def listar_produtos():
    conn = conectar()
    linhas = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
    conn.close()
    return linhas


def buscar_produto(produto_id):
    conn = conectar()
    linha = conn.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,)).fetchone()
    conn.close()
    if linha is None:
        raise ProdutoNaoEncontradoError("produto nao encontrado")
    return linha


def remover_produto(produto_id):
    buscar_produto(produto_id)
    conn = conectar()
    total_movimentacoes = conn.execute(
        "SELECT COUNT(*) AS total FROM movimentacoes WHERE produto_id = ?",
        (produto_id,)
    ).fetchone()["total"]

    if total_movimentacoes > 0:
        conn.close()
        raise ProdutoComMovimentacaoError(
            "nao e possivel excluir um produto que possui movimentacoes"
        )

    conn.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()
