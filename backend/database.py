import os
import sqlite3


CAMINHO_BANCO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "estoque.db"
)


def conectar():
    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def coluna_existe(conn, tabela, coluna):
    colunas = conn.execute(f"PRAGMA table_info({tabela})").fetchall()
    return coluna in [linha["name"] for linha in colunas]


def adicionar_coluna_se_nao_existir(conn, tabela, coluna, definicao):
    if not coluna_existe(conn, tabela, coluna):
        conn.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {definicao}")


def criar_tabelas():
    conn = conectar()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT,
            ativo INTEGER NOT NULL DEFAULT 1,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            sku TEXT,
            fornecedor TEXT,
            categoria_id INTEGER NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0,
            estoque_minimo INTEGER NOT NULL DEFAULT 0,
            ativo INTEGER NOT NULL DEFAULT 1,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
            saldo_anterior INTEGER NOT NULL DEFAULT 0,
            saldo_atual INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    """)

    # adiciona os campos novos sem apagar bancos que ja existem
    adicionar_coluna_se_nao_existir(conn, "categorias", "ativo", "INTEGER NOT NULL DEFAULT 1")
    adicionar_coluna_se_nao_existir(conn, "categorias", "criado_em", "TEXT")
    adicionar_coluna_se_nao_existir(conn, "produtos", "descricao", "TEXT")
    adicionar_coluna_se_nao_existir(conn, "produtos", "sku", "TEXT")
    adicionar_coluna_se_nao_existir(conn, "produtos", "fornecedor", "TEXT")
    adicionar_coluna_se_nao_existir(conn, "produtos", "ativo", "INTEGER NOT NULL DEFAULT 1")
    adicionar_coluna_se_nao_existir(conn, "produtos", "criado_em", "TEXT")
    adicionar_coluna_se_nao_existir(conn, "movimentacoes", "saldo_anterior", "INTEGER NOT NULL DEFAULT 0")
    adicionar_coluna_se_nao_existir(conn, "movimentacoes", "saldo_atual", "INTEGER NOT NULL DEFAULT 0")

    conn.commit()
    conn.close()


def inicializar_banco():
    criar_tabelas()


if __name__ == "__main__":
    inicializar_banco()
    print("banco criado")
