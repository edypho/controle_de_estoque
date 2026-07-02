# regra de negocio do sistema. e essa parte que o frontend vai chamar
# (o frontend nao deve mexer em repositories.py nem database.py direto)

from backend.models import Produto, Categoria, Movimentacao
from backend.repositories import ProdutoRepository, CategoriaRepository, MovimentacaoRepository
from backend.exceptions import (
    ProdutoNaoEncontradoError,
    CategoriaNaoEncontradaError,
    EstoqueInsuficienteError,
    DadosInvalidosError,
)


class CategoriaService:

    def __init__(self):
        self._repo = CategoriaRepository()

    def cadastrar_categoria(self, nome, descricao=""):
        if not nome or not nome.strip():
            raise DadosInvalidosError("nome da categoria nao pode ser vazio")
        categoria = Categoria(nome=nome.strip(), descricao=descricao.strip())
        return self._repo.salvar(categoria)

    def listar_categorias(self):
        return self._repo.listar_todas()


class ProdutoService:

    def __init__(self):
        self._repo = ProdutoRepository()
        self._repo_categoria = CategoriaRepository()

    def cadastrar_produto(self, nome, categoria_id, preco, quantidade_inicial=0, estoque_minimo=0):
        if not nome or not nome.strip():
            raise DadosInvalidosError("nome do produto nao pode ser vazio")
        if preco < 0:
            raise DadosInvalidosError("preco nao pode ser negativo")
        if quantidade_inicial < 0 or estoque_minimo < 0:
            raise DadosInvalidosError("quantidade e estoque minimo nao podem ser negativos")
        if self._repo_categoria.buscar_por_id(categoria_id) is None:
            raise CategoriaNaoEncontradaError(f"categoria {categoria_id} nao existe")

        produto = Produto(
            nome=nome.strip(),
            categoria_id=categoria_id,
            preco=preco,
            quantidade=quantidade_inicial,
            estoque_minimo=estoque_minimo,
        )
        return self._repo.salvar(produto)

    def listar_produtos(self):
        return self._repo.listar_todos()

    def buscar_produto(self, produto_id):
        produto = self._repo.buscar_por_id(produto_id)
        if produto is None:
            raise ProdutoNaoEncontradoError(f"produto {produto_id} nao encontrado")
        return produto

    def remover_produto(self, produto_id):
        self.buscar_produto(produto_id)  # so pra estourar erro se nao existir
        self._repo.remover(produto_id)


class EstoqueService:
    # controla entrada/saida e calcula o saldo automaticamente

    def __init__(self):
        self._repo_produto = ProdutoRepository()
        self._repo_mov = MovimentacaoRepository()

    def registrar_entrada(self, produto_id, quantidade, observacao=""):
        if quantidade <= 0:
            raise DadosInvalidosError("quantidade da entrada tem que ser maior que zero")

        produto = self._buscar_produto_ou_erro(produto_id)

        movimentacao = Movimentacao(produto_id=produto_id, tipo="ENTRADA", quantidade=quantidade, observacao=observacao)
        self._repo_mov.salvar(movimentacao)

        novo_saldo = produto.quantidade + quantidade
        self._repo_produto.atualizar_quantidade(produto_id, novo_saldo)

        return movimentacao

    def registrar_saida(self, produto_id, quantidade, observacao=""):
        if quantidade <= 0:
            raise DadosInvalidosError("quantidade da saida tem que ser maior que zero")

        produto = self._buscar_produto_ou_erro(produto_id)

        if quantidade > produto.quantidade:
            # nao deixa o saldo ficar negativo
            raise EstoqueInsuficienteError(
                f"saldo insuficiente pra '{produto.nome}'. disponivel: {produto.quantidade}, pedido: {quantidade}"
            )

        movimentacao = Movimentacao(produto_id=produto_id, tipo="SAIDA", quantidade=quantidade, observacao=observacao)
        self._repo_mov.salvar(movimentacao)

        novo_saldo = produto.quantidade - quantidade
        self._repo_produto.atualizar_quantidade(produto_id, novo_saldo)

        return movimentacao

    def consultar_saldo(self, produto_id):
        return self._buscar_produto_ou_erro(produto_id).quantidade

    def listar_produtos_abaixo_do_minimo(self):
        # o "alerta" e so isso: filtrar quem ja bateu no minimo. o frontend decide como mostrar
        return [p for p in self._repo_produto.listar_todos() if p.esta_abaixo_do_minimo()]

    def historico_movimentacoes(self, produto_id):
        return self._repo_mov.listar_por_produto(produto_id)

    def _buscar_produto_ou_erro(self, produto_id):
        produto = self._repo_produto.buscar_por_id(produto_id)
        if produto is None:
            raise ProdutoNaoEncontradoError(f"produto {produto_id} nao encontrado")
        return produto


class RelatorioService:

    def __init__(self):
        self._repo_produto = ProdutoRepository()
        self._repo_mov = MovimentacaoRepository()

    def relatorio_inventario_atual(self):
        # devolve uma lista de dict, da pra jogar direto numa Treeview do tkinter
        produtos = self._repo_produto.listar_todos()
        resultado = []
        for p in produtos:
            resultado.append({
                "id": p.id,
                "nome": p.nome,
                "quantidade": p.quantidade,
                "preco_unitario": p.preco,
                "valor_total": round(p.quantidade * p.preco, 2),
                "abaixo_do_minimo": p.esta_abaixo_do_minimo(),
            })
        return resultado

    def relatorio_movimentacoes(self):
        movimentacoes = self._repo_mov.listar_todas()
        resultado = []
        for m in movimentacoes:
            resultado.append({
                "id": m.id,
                "produto_id": m.produto_id,
                "tipo": m.tipo,
                "quantidade": m.quantidade,
                "observacao": m.observacao,
                "data_hora": m.data_hora,
            })
        return resultado
