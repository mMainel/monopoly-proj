from enum import Enum, auto
from typing import Any
from datetime import datetime
from dataclasses import dataclass

class TipoEvento(Enum):
    """
    Classe com os enums dos eventos do jogo
    o auto é só pra não termos que ficar definindo numeros para os eventos
    """
    TURNO_INICIADO = auto()
    TURNO_FINALIZADO = auto()
    DADOS_LANCADOS = auto()
    DUPLA_LANCADA = auto()
    JOGADOR_MOVEU = auto()
    PASSOU_INICIO = auto()
    PROPRIEDADE_COMPRADA = auto()
    ALUGUEL_PAGO = auto()
    CONSTRUCAO_FEITA = auto()
    CONSTRUCAO_VENDIDA = auto()
    JOGADOR_PRESO = auto()
    SAIU_CADEIA = auto()
    JOGADOR_FALIU = auto()
    PROPRIEDADE_HIPOTECADA = auto()
    PROPRIEDADE_DESHIPOTECADA = auto()
    LEILAO_INICIADO = auto()
    LEILAO_LANCE_DADO = auto()
    LEILAO_FINALIZADO = auto()
    LEILAO_SEM_VENCEDOR = auto()
    
    CARTA_SORTE_PEGA = auto()
    CARTA_COFRE_PEGA = auto()
    JOGADOR_RECEBEU_DINHEIRO = auto()
    JOGADOR_PAGOU_TAXA = auto()
    JOGADOR_RECEBEU_CARTA_SAIR_CADEIA = auto()

@dataclass(frozen=True)
class EventoJogo:
    """
    passando o '@dataclass', agnt inicializa automaticamente e gera já os construtores __repr__ e __eq__
    o frozen é apenas para definirmos que essa classe é imutável, ou seja, depois que a gente criar ela, n da pra gente modificar os atributos (so coloco um 'bypass' no timestamp com o __setattr__) 
    """
    tipo: TipoEvento
    dados: dict[str, Any]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            object.__setattr__(self, 'timestamp', datetime.now())