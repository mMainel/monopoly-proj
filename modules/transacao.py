"""_summary_ Class Transacao e TipoTransacao <<Abstrata>>
_description_
This module contains the Transacao class and the TipoTransacao enumeration used in the Monopoly game.
"""
from enum import Enum, auto
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from modules.titulo import titulo

class tipoTransacao(Enum):
    """Define os tipos de transações possíveis no jogo."""
    ALUGUEL = auto()
    COMPRA_PROPRIEDADE = auto()
    SALARIO = auto()
    TAXA = auto()
    CARTA = auto()
    CONSTRUCAO = auto()
    HIPOTECA = auto()
    LEILAO = auto()
    

class transacao:
    """Registro das transações feitas pelo banco."""
    
    def __init__(self, origem: object, destino: object, valor: int, tipo: tipoTransacao, descricao: str) -> None:
        self.origem = origem
        self.destino = destino
        self.valor = valor
        self.tipo = tipo
        self.descricao = descricao
        self.time_stamp = datetime.now()    
    
    def __repr__(self) -> str:
        return f"Transacao(origem={self.origem.nome}, destino={self.destino.nome}, valor={self.valor}, tipo={self.tipo.name})"
