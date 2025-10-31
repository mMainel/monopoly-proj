from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Titulo import Titulo
    from .Jogador import Jogador
    from .Propriedade import Propriedade    

class Banco:

    def __init__(self):
        self._casasDisponiveis: int = 32
        self._hoteisDisponiveis: int = 12
        self._propriedadesDisponiveis: List[Titulo] = []
    
    def venderPropriedade(self, titulo: Titulo, jogador: Jogador) -> None:
        self._propriedadesDisponiveis.append(titulo)
    
    def VenderCasa(self, propriedade: Propriedade) -> None:
        if self._casasDisponiveis > 0:
            self._casasDisponiveis -= 1
            
    def venderHotel(self, propriedade: Propriedade) -> None:
        if self._hoteisDisponiveis > 0:
            self._hoteisDisponiveis -= 1
    
    def comprarConstrucao(self, tipo:str, propriedade: Propriedade) -> None:
        if tipo == "casa":
            self._casasDisponiveis += 1
        elif tipo == "hotel":
            self._hoteisDisponiveis += 1
        
    def pagarSalario(self, jogador: Jogador) -> None:
        pass
    
    def cobrarTaxa(self, jogador: Jogador, valor: int) -> None:
        pass
    
    def hipotecar(self, titulo: Titulo)-> None:
        pass
    
    def resgatarHipoteca(self, titulo: Titulo) -> None:
        pass
    
    def realizarLeilao(self, propriedade: Propriedade, jogadores: List[Jogador]) -> None:
        pass
        