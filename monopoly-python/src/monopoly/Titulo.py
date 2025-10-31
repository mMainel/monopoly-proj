from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Titulo import Titulo
    from .Jogador import Jogador
    from .Propriedade import Propriedade    
class Titulo(ABC):
    """Classe abstrata mínima para títulos (propriedades/companhias)."""
    def __init__(self, proprietario: Jogador, hipotecado: bool, valorHipoteca) -> None:
        self._proprietario = proprietario
        self._hipotecado = hipotecado
        self._valorHipoteca = valorHipoteca

    @abstractmethod
    def descricao(self) -> str:
        """Retorna descrição do título - obrigatória nas subclasses."""
        ...
    
    def __repr__(self) -> str:
        return f"Titulo(nome={self._proprietario!r}, preco={self._valorHipoteca!r})"
    
class TituloPropriedade(Titulo):
    
    def __init__(self, proprietario: Jogador, hipotecado: bool, valorHipoteca) -> None:
        super().__init__(proprietario, hipotecado, valorHipoteca)
        

class TituloCompanhia(Titulo):
    
    def __init__(self, proprietario: Jogador, hipotecado: bool, valorHipoteca) -> None:
        super().__init__(proprietario, hipotecado, valorHipoteca)