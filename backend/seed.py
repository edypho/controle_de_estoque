from datetime import datetime

from backend.database import conectar, inicializar_banco


TAG_SEED = "[SEED-INFO-GAMER]"


def buscar_colunas(conn, tabela):
    linhas = conn.execute(f"PRAGMA table_info({tabela})").fetchall()
    return [linha["name"] for linha in linhas]


def obter_ou_criar_categoria(conn, nome, descricao):
    categoria = conn.execute(
        "SELECT id FROM categorias WHERE nome = ?",
        (nome,)
    ).fetchone()

    if categoria:
        conn.execute(
            """
            UPDATE categorias
            SET descricao = ?, ativo = 1
            WHERE id = ?
            """,
            (descricao, categoria["id"])
        )
        return categoria["id"]

    cursor = conn.execute(
        """
        INSERT INTO categorias (nome, descricao, ativo)
        VALUES (?, ?, 1)
        """,
        (nome, descricao)
    )

    return cursor.lastrowid


def obter_ou_criar_produto(
    conn,
    nome,
    categoria_id,
    preco,
    estoque_minimo,
    descricao,
    sku,
    fornecedor
):
    colunas = buscar_colunas(conn, "produtos")

    produto = conn.execute(
        "SELECT id FROM produtos WHERE sku = ?",
        (sku,)
    ).fetchone()

    if produto:
        conn.execute(
            """
            UPDATE produtos
            SET
                nome = ?,
                categoria_id = ?,
                preco = ?,
                estoque_minimo = ?,
                descricao = ?,
                fornecedor = ?,
                ativo = 1
            WHERE id = ?
            """,
            (
                nome,
                categoria_id,
                preco,
                estoque_minimo,
                descricao,
                fornecedor,
                produto["id"]
            )
        )
        return produto["id"]

    campos = [
        "nome",
        "categoria_id",
        "preco",
        "quantidade",
        "estoque_minimo",
        "ativo"
    ]

    valores = [
        nome,
        categoria_id,
        preco,
        0,
        estoque_minimo,
        1
    ]

    if "descricao" in colunas:
        campos.append("descricao")
        valores.append(descricao)

    if "sku" in colunas:
        campos.append("sku")
        valores.append(sku)

    if "fornecedor" in colunas:
        campos.append("fornecedor")
        valores.append(fornecedor)

    placeholders = ", ".join(["?"] * len(campos))
    campos_sql = ", ".join(campos)

    cursor = conn.execute(
        f"""
        INSERT INTO produtos ({campos_sql})
        VALUES ({placeholders})
        """,
        valores
    )

    return cursor.lastrowid


def registrar_movimentacao(conn, produto_id, tipo, quantidade, observacao):
    produto = conn.execute(
        "SELECT quantidade FROM produtos WHERE id = ?",
        (produto_id,)
    ).fetchone()

    saldo_anterior = produto["quantidade"]

    if tipo == "ENTRADA":
        saldo_atual = saldo_anterior + quantidade
    elif tipo == "SAIDA":
        saldo_atual = saldo_anterior - quantidade
    else:
        raise ValueError("tipo de movimentacao invalido")

    if saldo_atual < 0:
        raise ValueError("movimentacao deixaria o estoque negativo")

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn.execute(
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
            produto_id,
            tipo,
            quantidade,
            observacao,
            data_hora,
            saldo_anterior,
            saldo_atual
        )
    )

    conn.execute(
        "UPDATE produtos SET quantidade = ? WHERE id = ?",
        (saldo_atual, produto_id)
    )


def seed():
    inicializar_banco()

    conn = conectar()

    qtd_seed = conn.execute(
        """
        SELECT COUNT(*) AS total
        FROM movimentacoes
        WHERE observacao LIKE ?
        """,
        (f"{TAG_SEED}%",)
    ).fetchone()["total"]

    if qtd_seed > 0:
        print("Seed de informatica/gamer ja foi executado antes. Nenhuma movimentacao nova foi criada.")
        conn.close()
        return

    categorias = {
        "Periféricos Gamer": obter_ou_criar_categoria(
            conn,
            "Periféricos Gamer",
            "Mouses, teclados, mousepads e controles para setup gamer"
        ),
        "Hardware": obter_ou_criar_categoria(
            conn,
            "Hardware",
            "Peças internas para montagem e manutenção de computadores"
        ),
        "Monitores e Vídeo": obter_ou_criar_categoria(
            conn,
            "Monitores e Vídeo",
            "Monitores, cabos de vídeo e acessórios de imagem"
        ),
        "Rede e Conectividade": obter_ou_criar_categoria(
            conn,
            "Rede e Conectividade",
            "Roteadores, adaptadores e cabos de rede"
        ),
        "Armazenamento": obter_ou_criar_categoria(
            conn,
            "Armazenamento",
            "SSDs, HDs, pendrives e dispositivos de armazenamento"
        ),
        "Home Office": obter_ou_criar_categoria(
            conn,
            "Home Office",
            "Produtos para trabalho, estudo e organização de setup"
        ),
        "Manutenção": obter_ou_criar_categoria(
            conn,
            "Manutenção",
            "Itens para limpeza, reparo e manutenção de computadores"
        ),
        "Áudio e Streaming": obter_ou_criar_categoria(
            conn,
            "Áudio e Streaming",
            "Headsets, microfones, webcams e acessórios para chamadas e lives"
        ),
    }

    produtos = {
        "mouse_gamer": obter_ou_criar_produto(
            conn,
            "Mouse gamer RGB",
            categorias["Periféricos Gamer"],
            129.90,
            5,
            "Mouse gamer com iluminação RGB e sensor de alta precisão",
            "GAM-MOUSE-001",
            "TechZone Distribuidora"
        ),
        "teclado_mecanico": obter_ou_criar_produto(
            conn,
            "Teclado mecânico ABNT2",
            categorias["Periféricos Gamer"],
            249.90,
            4,
            "Teclado mecânico com layout ABNT2 e switches mecânicos",
            "GAM-TECLADO-001",
            "TechZone Distribuidora"
        ),
        "mousepad": obter_ou_criar_produto(
            conn,
            "Mousepad gamer extra grande",
            categorias["Periféricos Gamer"],
            59.90,
            8,
            "Mousepad grande para teclado e mouse",
            "GAM-MOUSEPAD-001",
            "SetupPro"
        ),
        "controle_pc": obter_ou_criar_produto(
            conn,
            "Controle USB para PC",
            categorias["Periféricos Gamer"],
            119.90,
            3,
            "Controle com conexão USB para jogos no computador",
            "GAM-CONTROLE-001",
            "SetupPro"
        ),
        "headset": obter_ou_criar_produto(
            conn,
            "Headset gamer com microfone",
            categorias["Áudio e Streaming"],
            189.90,
            5,
            "Headset gamer com microfone ajustável",
            "AUD-HEADSET-001",
            "AudioMax"
        ),
        "microfone": obter_ou_criar_produto(
            conn,
            "Microfone condensador USB",
            categorias["Áudio e Streaming"],
            299.90,
            2,
            "Microfone USB para chamadas, gravações e streaming",
            "AUD-MIC-001",
            "AudioMax"
        ),
        "webcam": obter_ou_criar_produto(
            conn,
            "Webcam Full HD",
            categorias["Áudio e Streaming"],
            159.90,
            4,
            "Webcam Full HD para reuniões, aulas e transmissões",
            "AUD-WEBCAM-001",
            "OfficeTech"
        ),
        "monitor_24": obter_ou_criar_produto(
            conn,
            "Monitor 24 polegadas 75Hz",
            categorias["Monitores e Vídeo"],
            699.90,
            3,
            "Monitor LED 24 polegadas para trabalho e jogos casuais",
            "VID-MONITOR-001",
            "DisplayCenter"
        ),
        "monitor_144": obter_ou_criar_produto(
            conn,
            "Monitor gamer 144Hz",
            categorias["Monitores e Vídeo"],
            1199.90,
            2,
            "Monitor gamer com taxa de atualização de 144Hz",
            "VID-MONITOR-144",
            "DisplayCenter"
        ),
        "cabo_hdmi": obter_ou_criar_produto(
            conn,
            "Cabo HDMI 2 metros",
            categorias["Monitores e Vídeo"],
            34.90,
            10,
            "Cabo HDMI para conexão de vídeo e áudio",
            "VID-HDMI-001",
            "CaboNet"
        ),
        "ssd_480": obter_ou_criar_produto(
            conn,
            "SSD 480GB SATA",
            categorias["Armazenamento"],
            229.90,
            4,
            "SSD SATA de 480GB para upgrade de computadores e notebooks",
            "ARM-SSD-480",
            "StoragePlus"
        ),
        "ssd_nvme": obter_ou_criar_produto(
            conn,
            "SSD NVMe 1TB",
            categorias["Armazenamento"],
            449.90,
            3,
            "SSD NVMe de 1TB para alta velocidade de leitura e gravação",
            "ARM-NVME-1TB",
            "StoragePlus"
        ),
        "pendrive": obter_ou_criar_produto(
            conn,
            "Pendrive 64GB",
            categorias["Armazenamento"],
            39.90,
            12,
            "Pendrive USB 64GB para transporte de arquivos",
            "ARM-PENDRIVE-64",
            "StoragePlus"
        ),
        "memoria_ram": obter_ou_criar_produto(
            conn,
            "Memória RAM 8GB DDR4",
            categorias["Hardware"],
            159.90,
            5,
            "Módulo de memória RAM DDR4 de 8GB",
            "HARD-RAM-8DDR4",
            "PC Parts Brasil"
        ),
        "fonte": obter_ou_criar_produto(
            conn,
            "Fonte 600W 80 Plus",
            categorias["Hardware"],
            329.90,
            3,
            "Fonte de alimentação 600W com certificação 80 Plus",
            "HARD-FONTE-600",
            "PC Parts Brasil"
        ),
        "cooler": obter_ou_criar_produto(
            conn,
            "Cooler 120mm RGB",
            categorias["Hardware"],
            49.90,
            6,
            "Cooler de gabinete 120mm com iluminação RGB",
            "HARD-COOLER-120",
            "PC Parts Brasil"
        ),
        "roteador": obter_ou_criar_produto(
            conn,
            "Roteador Wi-Fi dual band",
            categorias["Rede e Conectividade"],
            249.90,
            3,
            "Roteador dual band para redes domésticas e pequenos escritórios",
            "REDE-ROTEADOR-001",
            "CaboNet"
        ),
        "cabo_rede": obter_ou_criar_produto(
            conn,
            "Cabo de rede Cat6 3 metros",
            categorias["Rede e Conectividade"],
            24.90,
            15,
            "Cabo de rede Cat6 para conexões cabeadas",
            "REDE-CAT6-003",
            "CaboNet"
        ),
        "adaptador_wifi": obter_ou_criar_produto(
            conn,
            "Adaptador Wi-Fi USB",
            categorias["Rede e Conectividade"],
            69.90,
            5,
            "Adaptador USB para conexão Wi-Fi em computadores",
            "REDE-WIFI-USB",
            "CaboNet"
        ),
        "cadeira": obter_ou_criar_produto(
            conn,
            "Cadeira de escritório ergonômica",
            categorias["Home Office"],
            699.90,
            2,
            "Cadeira ergonômica para estudo, trabalho e setup",
            "HOME-CADEIRA-001",
            "OfficeTech"
        ),
        "suporte_notebook": obter_ou_criar_produto(
            conn,
            "Suporte para notebook",
            categorias["Home Office"],
            89.90,
            6,
            "Suporte ajustável para notebook",
            "HOME-SUPORTE-NOTE",
            "OfficeTech"
        ),
        "hub_usb": obter_ou_criar_produto(
            conn,
            "Hub USB 4 portas",
            categorias["Home Office"],
            59.90,
            8,
            "Hub USB com quatro portas para expansão de conexões",
            "HOME-HUB-USB",
            "OfficeTech"
        ),
        "pasta_termica": obter_ou_criar_produto(
            conn,
            "Pasta térmica",
            categorias["Manutenção"],
            29.90,
            10,
            "Pasta térmica para manutenção de processadores",
            "MAN-PASTA-TERMICA",
            "Manutec"
        ),
        "alcool_iso": obter_ou_criar_produto(
            conn,
            "Álcool isopropílico",
            categorias["Manutenção"],
            34.90,
            8,
            "Álcool isopropílico para limpeza de componentes eletrônicos",
            "MAN-ALCOOL-ISO",
            "Manutec"
        ),
        "kit_limpeza": obter_ou_criar_produto(
            conn,
            "Kit limpeza de teclado",
            categorias["Manutenção"],
            39.90,
            7,
            "Kit com escova, pincel e soprador manual para limpeza de periféricos",
            "MAN-KIT-LIMPEZA",
            "Manutec"
        ),
    }

    movimentacoes = [
        (produtos["mouse_gamer"], "ENTRADA", 25, "Compra inicial de mouses gamer"),
        (produtos["mouse_gamer"], "SAIDA", 8, "Venda de mouses gamer"),

        (produtos["teclado_mecanico"], "ENTRADA", 15, "Compra inicial de teclados mecânicos"),
        (produtos["teclado_mecanico"], "SAIDA", 4, "Venda de teclados mecânicos"),

        (produtos["mousepad"], "ENTRADA", 30, "Compra inicial de mousepads"),
        (produtos["mousepad"], "SAIDA", 12, "Venda de mousepads"),

        (produtos["controle_pc"], "ENTRADA", 10, "Compra inicial de controles USB"),
        (produtos["controle_pc"], "SAIDA", 3, "Venda de controles USB"),

        (produtos["headset"], "ENTRADA", 18, "Compra inicial de headsets"),
        (produtos["headset"], "SAIDA", 7, "Venda de headsets"),

        (produtos["microfone"], "ENTRADA", 6, "Compra inicial de microfones"),
        (produtos["microfone"], "SAIDA", 4, "Venda de microfones"),

        (produtos["webcam"], "ENTRADA", 14, "Compra inicial de webcams"),
        (produtos["webcam"], "SAIDA", 5, "Venda de webcams"),

        (produtos["monitor_24"], "ENTRADA", 8, "Compra inicial de monitores 24 polegadas"),
        (produtos["monitor_24"], "SAIDA", 3, "Venda de monitores 24 polegadas"),

        (produtos["monitor_144"], "ENTRADA", 5, "Compra inicial de monitores 144Hz"),
        (produtos["monitor_144"], "SAIDA", 3, "Venda de monitores gamer 144Hz"),

        (produtos["cabo_hdmi"], "ENTRADA", 40, "Compra inicial de cabos HDMI"),
        (produtos["cabo_hdmi"], "SAIDA", 18, "Venda de cabos HDMI"),

        (produtos["ssd_480"], "ENTRADA", 12, "Compra inicial de SSDs SATA"),
        (produtos["ssd_480"], "SAIDA", 5, "Venda de SSDs SATA"),

        (produtos["ssd_nvme"], "ENTRADA", 8, "Compra inicial de SSDs NVMe"),
        (produtos["ssd_nvme"], "SAIDA", 5, "Venda de SSDs NVMe"),

        (produtos["pendrive"], "ENTRADA", 50, "Compra inicial de pendrives"),
        (produtos["pendrive"], "SAIDA", 22, "Venda de pendrives"),

        (produtos["memoria_ram"], "ENTRADA", 20, "Compra inicial de memórias RAM"),
        (produtos["memoria_ram"], "SAIDA", 9, "Venda de memórias RAM"),

        (produtos["fonte"], "ENTRADA", 7, "Compra inicial de fontes"),
        (produtos["fonte"], "SAIDA", 4, "Venda de fontes"),

        (produtos["cooler"], "ENTRADA", 25, "Compra inicial de coolers"),
        (produtos["cooler"], "SAIDA", 11, "Venda de coolers"),

        (produtos["roteador"], "ENTRADA", 9, "Compra inicial de roteadores"),
        (produtos["roteador"], "SAIDA", 4, "Venda de roteadores"),

        (produtos["cabo_rede"], "ENTRADA", 60, "Compra inicial de cabos de rede"),
        (produtos["cabo_rede"], "SAIDA", 25, "Venda de cabos de rede"),

        (produtos["adaptador_wifi"], "ENTRADA", 20, "Compra inicial de adaptadores Wi-Fi"),
        (produtos["adaptador_wifi"], "SAIDA", 9, "Venda de adaptadores Wi-Fi"),

        (produtos["cadeira"], "ENTRADA", 4, "Compra inicial de cadeiras ergonômicas"),
        (produtos["cadeira"], "SAIDA", 2, "Venda de cadeiras ergonômicas"),

        (produtos["suporte_notebook"], "ENTRADA", 18, "Compra inicial de suportes para notebook"),
        (produtos["suporte_notebook"], "SAIDA", 6, "Venda de suportes para notebook"),

        (produtos["hub_usb"], "ENTRADA", 25, "Compra inicial de hubs USB"),
        (produtos["hub_usb"], "SAIDA", 10, "Venda de hubs USB"),

        (produtos["pasta_termica"], "ENTRADA", 35, "Compra inicial de pastas térmicas"),
        (produtos["pasta_termica"], "SAIDA", 15, "Venda de pastas térmicas"),

        (produtos["alcool_iso"], "ENTRADA", 22, "Compra inicial de álcool isopropílico"),
        (produtos["alcool_iso"], "SAIDA", 10, "Venda de álcool isopropílico"),

        (produtos["kit_limpeza"], "ENTRADA", 18, "Compra inicial de kits de limpeza"),
        (produtos["kit_limpeza"], "SAIDA", 8, "Venda de kits de limpeza"),
    ]

    for produto_id, tipo, quantidade, observacao in movimentacoes:
        registrar_movimentacao(
            conn,
            produto_id,
            tipo,
            quantidade,
            f"{TAG_SEED} {observacao}"
        )

    conn.commit()
    conn.close()

    print("Banco populado com produtos de informatica, gamer, hardware e home office.")


if __name__ == "__main__":
    seed()