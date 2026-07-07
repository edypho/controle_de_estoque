# aqui fica o codigo que mexe direto no banco (SQL)
# separei do services.py pra nao misturar "regra de negocio" com "comando SQL"

from backend.database import criar_conexao
from backend.models import Categoria, Produto, Movimentacao


class CategoriaRepository:
    def salvar(self, categoria):
        conexao = criar_conexao()

        cursor = conexao.execute(
            "INSERT INTO categorias (nome, descricao) VALUES (?, ?)",
            (categoria.nome, categoria.descricao)
        )

        categoria.id = cursor.lastrowid

        conexao.commit()
        conexao.close()

        return categoria

    def buscar_por_id(self, categoria_id):
        conexao = criar_conexao()

        linha = conexao.execute(
            """
            SELECT *
            FROM categorias
            WHERE id = ? AND ativo = 1
            """,
            (categoria_id,)
        ).fetchone()

        conexao.close()

        if linha is None:
            return None

        return Categoria(
            id=linha["id"],
            nome=linha["nome"],
            descricao=linha["descricao"]
        )

    def listar_todas(self):
        conexao = criar_conexao()

        linhas = conexao.execute(
            """
            SELECT *
            FROM categorias
            WHERE ativo = 1
            ORDER BY nome
            """
        ).fetchall()

        conexao.close()

        return [
            Categoria(
                id=l["id"],
                nome=l["nome"],
                descricao=l["descricao"]
            )
            for l in linhas
        ]


class ProdutoRepository:
    def salvar(self, produto):
        conexao = criar_conexao()

        cursor = conexao.execute(
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
            (
                produto.nome,
                produto.categoria_id,
                produto.preco,
                produto.quantidade,
                produto.estoque_minimo
            )
        )

        produto.id = cursor.lastrowid

        conexao.commit()
        conexao.close()

        return produto

    def buscar_por_id(self, produto_id):
        conexao = criar_conexao()

        linha = conexao.execute(
            """
            SELECT *
            FROM produtos
            WHERE id = ? AND ativo = 1
            """,
            (produto_id,)
        ).fetchone()

        conexao.close()

        return self._linha_para_produto(linha) if linha else None

    def listar_todos(self):
        conexao = criar_conexao()

        linhas = conexao.execute(
            """
            SELECT *
            FROM produtos
            WHERE ativo = 1
            ORDER BY nome
            """
        ).fetchall()

        conexao.close()

        return [self._linha_para_produto(l) for l in linhas]

    def atualizar_quantidade(self, produto_id, nova_quantidade):
        conexao = criar_conexao()

        conexao.execute(
            """
            UPDATE produtos
            SET quantidade = ?
            WHERE id = ? AND ativo = 1
            """,
            (nova_quantidade, produto_id)
        )

        conexao.commit()
        conexao.close()

    def remover(self, produto_id):
        conexao = criar_conexao()

        conexao.execute(
            """
            UPDATE produtos
            SET ativo = 0
            WHERE id = ?
            """,
            (produto_id,)
        )

        conexao.commit()
        conexao.close()

    def _linha_para_produto(self, linha):
        return Produto(
            id=linha["id"],
            nome=linha["nome"],
            categoria_id=linha["categoria_id"],
            preco=linha["preco"],
            quantidade=linha["quantidade"],
            estoque_minimo=linha["estoque_minimo"],
        )


class MovimentacaoRepository:
    def salvar(self, movimentacao):
        conexao = criar_conexao()

        cursor = conexao.execute(
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
                movimentacao.produto_id,
                movimentacao.tipo,
                movimentacao.quantidade,
                movimentacao.observacao,
                movimentacao.data_hora,
                movimentacao.saldo_anterior,
                movimentacao.saldo_atual
            )
        )

        movimentacao.id = cursor.lastrowid

        conexao.commit()
        conexao.close()

        return movimentacao

    def listar_por_produto(self, produto_id):
        conexao = criar_conexao()

        linhas = conexao.execute(
            """
            SELECT *
            FROM movimentacoes
            WHERE produto_id = ?
            ORDER BY data_hora DESC
            """,
            (produto_id,)
        ).fetchall()

        conexao.close()

        return [self._linha_para_movimentacao(l) for l in linhas]

    def listar_todas(self):
        conexao = criar_conexao()

        linhas = conexao.execute(
            """
            SELECT *
            FROM movimentacoes
            ORDER BY data_hora DESC
            """
        ).fetchall()

        conexao.close()

        return [self._linha_para_movimentacao(l) for l in linhas]

    def _linha_para_movimentacao(self, linha):
        return Movimentacao(
            id=linha["id"],
            produto_id=linha["produto_id"],
            tipo=linha["tipo"],
            quantidade=linha["quantidade"],
            observacao=linha["observacao"],
            data_hora=linha["data_hora"],
            saldo_anterior=linha["saldo_anterior"],
            saldo_atual=linha["saldo_atual"],
        )