# classes que representam os dados do sistema
# uma classe pra cada "tabela" do banco

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Categoria:
    nome: str
    descricao: str = ""
    id: Optional[int] = None


@dataclass
class Produto:
    nome: str
    categoria_id: int
    preco: float
    quantidade: int = 0
    estoque_minimo: int = 0
    id: Optional[int] = None

    def esta_abaixo_do_minimo(self):
        # se o saldo já bateu ou passou do minimo, ta em alerta
        return self.quantidade <= self.estoque_minimo


@dataclass
class Movimentacao:
    produto_id: int
    tipo: str  # "ENTRADA" ou "SAIDA"
    quantidade: int
    observacao: str = ""
    data_hora: str = ""
    id: Optional[int] = None

    def __post_init__(self):
        if not self.data_hora:
            self.data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
