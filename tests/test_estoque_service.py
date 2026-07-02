# testes do backend usando unittest (ja vem com o python)
# roda com: python -m unittest discover tests -v

import unittest
import os
import backend.database as database
from backend.services import CategoriaService, ProdutoService, EstoqueService
from backend.exceptions import EstoqueInsuficienteError, DadosInvalidosError


class TestEstoqueService(unittest.TestCase):

    def setUp(self):
        # usa um banco separado pra nao bagunçar o banco de verdade
        database.CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), "estoque_teste.db")
        if os.path.exists(database.CAMINHO_BANCO):
            os.remove(database.CAMINHO_BANCO)
        database.inicializar_banco()

        self.categoria_service = CategoriaService()
        self.produto_service = ProdutoService()
        self.estoque_service = EstoqueService()

        categoria = self.categoria_service.cadastrar_categoria("Bebidas")
        self.produto = self.produto_service.cadastrar_produto(
            nome="Refrigerante 2L", categoria_id=categoria.id,
            preco=8.5, quantidade_inicial=0, estoque_minimo=5
        )

    def tearDown(self):
        if os.path.exists(database.CAMINHO_BANCO):
            os.remove(database.CAMINHO_BANCO)

    def test_entrada_aumenta_saldo(self):
        self.estoque_service.registrar_entrada(self.produto.id, 20)
        self.assertEqual(self.estoque_service.consultar_saldo(self.produto.id), 20)

    def test_saida_diminui_saldo(self):
        self.estoque_service.registrar_entrada(self.produto.id, 20)
        self.estoque_service.registrar_saida(self.produto.id, 8)
        self.assertEqual(self.estoque_service.consultar_saldo(self.produto.id), 12)

    def test_saida_maior_que_saldo_gera_erro(self):
        self.estoque_service.registrar_entrada(self.produto.id, 5)
        with self.assertRaises(EstoqueInsuficienteError):
            self.estoque_service.registrar_saida(self.produto.id, 100)

    def test_quantidade_negativa_gera_erro(self):
        with self.assertRaises(DadosInvalidosError):
            self.estoque_service.registrar_entrada(self.produto.id, -5)

    def test_alerta_estoque_minimo(self):
        criticos = self.estoque_service.listar_produtos_abaixo_do_minimo()
        self.assertIn(self.produto.id, [p.id for p in criticos])

        self.estoque_service.registrar_entrada(self.produto.id, 50)
        criticos = self.estoque_service.listar_produtos_abaixo_do_minimo()
        self.assertNotIn(self.produto.id, [p.id for p in criticos])


if __name__ == "__main__":
    unittest.main()
