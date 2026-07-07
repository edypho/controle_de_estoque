# regra de negocio do sistema. e essa parte que o frontend vai chamar
# (o frontend nao deve mexer em repositories.py nem database.py direto)

# regra de negocio do sistema
# essa parte e o que o frontend vai chamar
# o frontend nao deve mexer em repositories.py nem database.py direto

from backend.models import Produto, Categoria, Movimentacao
from backend.repositories import (
    ProdutoRepository,
    CategoriaRepository,
    MovimentacaoRepository,
)
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

        categoria = Categoria(
            nome=nome.strip(),
            descricao=(descricao or "").strip()
        )

        return self._repo.salvar(categoria)

    def listar_categorias(self):
        return self._repo.listar_todas()


class ProdutoService:
    def __init__(self):
        self._repo = ProdutoRepository()
        self._repo_categoria = CategoriaRepository()

    def cadastrar_produto(
        self,
        nome,
        categoria_id,
        preco,
        quantidade_inicial=0,
        estoque_minimo=0
    ):
        if not nome or not nome.strip():
            raise DadosInvalidosError("nome do produto nao pode ser vazio")

        if preco < 0:
            raise DadosInvalidosError("preco nao pode ser negativo")

        if quantidade_inicial < 0 or estoque_minimo < 0:
            raise DadosInvalidosError(
                "quantidade e estoque minimo nao podem ser negativos"
            )

        if self._repo_categoria.buscar_por_id(categoria_id) is None:
            raise CategoriaNaoEncontradaError(
                f"categoria {categoria_id} nao existe"
            )

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
            raise ProdutoNaoEncontradoError(
                f"produto {produto_id} nao encontrado"
            )

        return produto

    def remover_produto(self, produto_id):
        self.buscar_produto(produto_id)
        self._repo.remover(produto_id)


class EstoqueService:
    # controla entrada/saida e calcula o saldo automaticamente

    def __init__(self):
        self._repo_produto = ProdutoRepository()
        self._repo_mov = MovimentacaoRepository()

    def registrar_entrada(self, produto_id, quantidade, observacao=""):
        if quantidade <= 0:
            raise DadosInvalidosError(
                "quantidade da entrada tem que ser maior que zero"
            )

        produto = self._buscar_produto_ou_erro(produto_id)

        saldo_anterior = produto.quantidade
        saldo_atual = saldo_anterior + quantidade

        movimentacao = Movimentacao(
            produto_id=produto_id,
            tipo="ENTRADA",
            quantidade=quantidade,
            observacao=observacao,
            saldo_anterior=saldo_anterior,
            saldo_atual=saldo_atual,
        )

        self._repo_mov.salvar(movimentacao)
        self._repo_produto.atualizar_quantidade(produto_id, saldo_atual)

        return movimentacao

    def registrar_saida(self, produto_id, quantidade, observacao=""):
        if quantidade <= 0:
            raise DadosInvalidosError(
                "quantidade da saida tem que ser maior que zero"
            )

        produto = self._buscar_produto_ou_erro(produto_id)

        if quantidade > produto.quantidade:
            raise EstoqueInsuficienteError(
                f"saldo insuficiente pra '{produto.nome}'. "
                f"disponivel: {produto.quantidade}, pedido: {quantidade}"
            )

        saldo_anterior = produto.quantidade
        saldo_atual = saldo_anterior - quantidade

        movimentacao = Movimentacao(
            produto_id=produto_id,
            tipo="SAIDA",
            quantidade=quantidade,
            observacao=observacao,
            saldo_anterior=saldo_anterior,
            saldo_atual=saldo_atual,
        )

        self._repo_mov.salvar(movimentacao)
        self._repo_produto.atualizar_quantidade(produto_id, saldo_atual)

        return movimentacao

    def consultar_saldo(self, produto_id):
        return self._buscar_produto_ou_erro(produto_id).quantidade

    def listar_produtos_abaixo_do_minimo(self):
        return [
            produto
            for produto in self._repo_produto.listar_todos()
            if produto.esta_abaixo_do_minimo()
        ]

    def historico_movimentacoes(self, produto_id):
        self._buscar_produto_ou_erro(produto_id)
        return self._repo_mov.listar_por_produto(produto_id)

    def _buscar_produto_ou_erro(self, produto_id):
        produto = self._repo_produto.buscar_por_id(produto_id)

        if produto is None:
            raise ProdutoNaoEncontradoError(
                f"produto {produto_id} nao encontrado"
            )

        return produto


class RelatorioService:
    def __init__(self):
        self._repo_produto = ProdutoRepository()
        self._repo_mov = MovimentacaoRepository()

    def relatorio_inventario_atual(self):
        produtos = self._repo_produto.listar_todos()
        resultado = []

        for produto in produtos:
            resultado.append({
                "id": produto.id,
                "nome": produto.nome,
                "quantidade": produto.quantidade,
                "preco_unitario": produto.preco,
                "valor_total": round(produto.quantidade * produto.preco, 2),
                "abaixo_do_minimo": produto.esta_abaixo_do_minimo(),
            })

        return resultado

    def relatorio_movimentacoes(self):
        movimentacoes = self._repo_mov.listar_todas()
        resultado = []

        for movimentacao in movimentacoes:
            resultado.append({
                "id": movimentacao.id,
                "produto_id": movimentacao.produto_id,
                "tipo": movimentacao.tipo,
                "quantidade": movimentacao.quantidade,
                "observacao": movimentacao.observacao,
                "data_hora": movimentacao.data_hora,
                "saldo_anterior": movimentacao.saldo_anterior,
                "saldo_atual": movimentacao.saldo_atual,
            })

        return resultado