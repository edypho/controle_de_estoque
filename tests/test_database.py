import os
import sqlite3
import unittest

import backend.database as database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        database.CAMINHO_BANCO = os.path.join(
            os.path.dirname(__file__),
            "estoque_migracao_teste.db"
        )
        if os.path.exists(database.CAMINHO_BANCO):
            os.remove(database.CAMINHO_BANCO)

    def tearDown(self):
        if os.path.exists(database.CAMINHO_BANCO):
            os.remove(database.CAMINHO_BANCO)

    def test_atualiza_banco_antigo_sem_apagar_dados(self):
        conn = sqlite3.connect(database.CAMINHO_BANCO)
        conn.executescript("""
            CREATE TABLE categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT
            );

            CREATE TABLE produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0,
                estoque_minimo INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                observacao TEXT,
                data_hora TEXT NOT NULL
            );

            INSERT INTO categorias (nome) VALUES ('Bebidas');
        """)
        conn.commit()
        conn.close()

        database.criar_tabelas()

        conn = database.conectar()
        categoria = conn.execute(
            "SELECT nome, ativo FROM categorias WHERE id = 1"
        ).fetchone()
        colunas_produtos = {
            linha["name"]
            for linha in conn.execute("PRAGMA table_info(produtos)").fetchall()
        }
        colunas_movimentacoes = {
            linha["name"]
            for linha in conn.execute("PRAGMA table_info(movimentacoes)").fetchall()
        }
        conn.close()

        self.assertEqual(categoria["nome"], "Bebidas")
        self.assertEqual(categoria["ativo"], 1)
        self.assertIn("sku", colunas_produtos)
        self.assertIn("ativo", colunas_produtos)
        self.assertIn("saldo_anterior", colunas_movimentacoes)
        self.assertIn("saldo_atual", colunas_movimentacoes)


if __name__ == "__main__":
    unittest.main()
