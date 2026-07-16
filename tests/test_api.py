import os
import unittest

import backend.database as database
from backend.api import app


class TestApi(unittest.TestCase):

    def setUp(self):
        database.CAMINHO_BANCO = os.path.join(
            os.path.dirname(__file__),
            "estoque_api_teste.db"
        )
        if os.path.exists(database.CAMINHO_BANCO):
            os.remove(database.CAMINHO_BANCO)

        database.criar_tabelas()
        app.config["TESTING"] = True
        self.cliente = app.test_client()

    def tearDown(self):
        if os.path.exists(database.CAMINHO_BANCO):
            os.remove(database.CAMINHO_BANCO)

    def criar_produto(self):
        resposta_categoria = self.cliente.post(
            "/categorias",
            json={"nome": "Bebidas"}
        )
        categoria_id = resposta_categoria.get_json()["id"]

        resposta_produto = self.cliente.post(
            "/produtos",
            json={
                "nome": "Agua",
                "categoria_id": categoria_id,
                "preco": 3.5,
                "quantidade": 0,
                "estoque_minimo": 2,
            }
        )
        return resposta_produto.get_json()["id"]

    def test_cadastra_categoria_e_produto(self):
        produto_id = self.criar_produto()

        resposta = self.cliente.get(f"/produtos/{produto_id}")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["nome"], "Agua")

    def test_pagina_inicial_carrega_frontend(self):
        resposta = self.cliente.get("/")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"Controle de Estoque", resposta.data)
        resposta.close()

    def test_arquivo_css_carrega(self):
        resposta = self.cliente.get("/css/style.css")

        self.assertEqual(resposta.status_code, 200)
        resposta.close()

    def test_rejeita_requisicao_sem_json(self):
        resposta = self.cliente.post("/categorias")

        self.assertEqual(resposta.status_code, 400)
        self.assertIn("erro", resposta.get_json())

    def test_entrada_saida_historico_e_dashboard(self):
        produto_id = self.criar_produto()

        entrada = self.cliente.post(
            f"/produtos/{produto_id}/entrada",
            json={"quantidade": 10, "observacao": "compra"}
        )
        saida = self.cliente.post(
            f"/produtos/{produto_id}/saida",
            json={"quantidade": 3, "observacao": "venda"}
        )
        historico = self.cliente.get(f"/produtos/{produto_id}/historico")
        dashboard = self.cliente.get("/dashboard")

        self.assertEqual(entrada.get_json()["saldo"], 10)
        self.assertEqual(saida.get_json()["saldo"], 7)
        self.assertEqual(len(historico.get_json()), 2)
        self.assertEqual(dashboard.get_json(), {"entradas": 1, "saidas": 1})

    def test_historico_de_produto_inexistente_retorna_404(self):
        resposta = self.cliente.get("/produtos/999/historico")

        self.assertEqual(resposta.status_code, 404)
        self.assertIn("erro", resposta.get_json())

    def test_exclui_produto_e_preserva_historico(self):
        produto_id = self.criar_produto()
        self.cliente.post(
            f"/produtos/{produto_id}/entrada",
            json={"quantidade": 1}
        )

        resposta = self.cliente.delete(f"/produtos/{produto_id}")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(self.cliente.get(f"/produtos/{produto_id}").status_code, 404)

        historico = self.cliente.get("/relatorio/movimentacoes").get_json()
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico[0]["produto_id"], produto_id)


if __name__ == "__main__":
    unittest.main()
