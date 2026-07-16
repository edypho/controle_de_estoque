import sqlite3
import os

CAMINHO_BANCO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "estoque.db"
)

def conectar():
    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_tabelas():
    conn = conectar()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria_id INTEGER NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0,
            estoque_minimo INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (categoria_id) REFERENCES categorias (id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            observacao TEXT,
            data_hora TEXT NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_tabelas()
    print("banco criado")
