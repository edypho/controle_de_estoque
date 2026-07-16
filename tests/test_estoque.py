import unittest
import os
import backend.database as database
from backend import produtos, movimentacoes
from backend.exceptions import (
    DadosInvalidosError,
    EstoqueInsuficienteError,
    ProdutoComMovimentacaoError,
)


class TestEstoque(unittest.TestCase):

    def setUp(self):
        database.CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), "estoque_teste.db")
        if os.path.exists(database.CAMINHO_BANCO):
            os.remove(database.CAMINHO_BANCO)
        database.criar_tabelas()

        categoria_id = produtos.cadastrar_categoria("Bebidas")
        self.produto_id = produtos.cadastrar_produto(
            nome="Refrigerante 2L", categoria_id=categoria_id,
            preco=8.5, quantidade=0, estoque_minimo=5
        )

    def tearDown(self):
        if os.path.exists(database.CAMINHO_BANCO):
            os.remove(database.CAMINHO_BANCO)

    def test_entrada_aumenta_saldo(self):
        movimentacoes.registrar_entrada(self.produto_id, 20)
        self.assertEqual(movimentacoes.consultar_saldo(self.produto_id), 20)

    def test_saida_diminui_saldo(self):
        movimentacoes.registrar_entrada(self.produto_id, 20)
        movimentacoes.registrar_saida(self.produto_id, 8)
        self.assertEqual(movimentacoes.consultar_saldo(self.produto_id), 12)

    def test_saida_maior_que_saldo_da_erro(self):
        movimentacoes.registrar_entrada(self.produto_id, 5)
        with self.assertRaises(EstoqueInsuficienteError):
            movimentacoes.registrar_saida(self.produto_id, 100)

    def test_quantidade_negativa_da_erro(self):
        with self.assertRaises(DadosInvalidosError):
            movimentacoes.registrar_entrada(self.produto_id, -5)

    def test_quantidade_decimal_da_erro(self):
        with self.assertRaises(DadosInvalidosError):
            movimentacoes.registrar_entrada(self.produto_id, 1.5)

    def test_nao_remove_produto_com_historico(self):
        movimentacoes.registrar_entrada(self.produto_id, 5)
        with self.assertRaises(ProdutoComMovimentacaoError):
            produtos.remover_produto(self.produto_id)

    def test_alerta_estoque_minimo(self):
        baixo = movimentacoes.produtos_estoque_baixo()
        ids = [p["id"] for p in baixo]
        self.assertIn(self.produto_id, ids)

        movimentacoes.registrar_entrada(self.produto_id, 50)
        baixo = movimentacoes.produtos_estoque_baixo()
        ids = [p["id"] for p in baixo]
        self.assertNotIn(self.produto_id, ids)


if __name__ == "__main__":
    unittest.main()
