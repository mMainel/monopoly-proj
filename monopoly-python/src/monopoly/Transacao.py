"""_summary_ Class Transacao e TipoTransacao <<Abstrata>>
_description_
This module contains the Transacao class and the TipoTransacao enumeration used in the Monopoly game.
"""
from enum import Enum
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Titulo import Titulo
    from .Jogador import Jogador
    from .Propriedade import Propriedade

class TipoTransacao(Enum):
    ALUGUEL = 1
    COMPRA_PROPRIEDADE = 2
    SALARIO = 3
    TAXA = 4
    CARTA = 5
    CONSTRUCAO = 6
    HIPOTECA = 7
    LEILAO = 8
    

class Transacao:
    def __init__(self, origem: Jogador, destino: Jogador, valor: int, tipo: TipoTransacao, descricao: str) -> None:
        self._origem: Jogador = origem
        self._destino: Jogador = destino
        self._valor: int = valor
        self._tipo: TipoTransacao = tipo
    
    def getOrigem(self) -> Jogador:
        return self._origem
    def getDestino(self) -> Jogador:
        return self._destino
    def getValor(self) -> int:
        return self._valor  
    def getTipo(self) -> TipoTransacao:
        return self._tipo 
    def getDescricao(self) -> str:
        return self._tipo.name
    def __repr__(self) -> str:
        return f"Transacao(origem={self._origem.nome}, destino={self._destino.nome}, valor={self._valor}, tipo={self._tipo.name})"