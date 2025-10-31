from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .Titulo import Titulo
    from .Jogador import Jogador

class Propriedade:
    """Stub mínimo para integração com Banco / Tabuleiro / Jogador."""
    def __init__(self, titulo: "Titulo") -> None:
        self.titulo: "Titulo" = titulo
        self.proprietario: Optional["Jogador"] = None

    def executar_acao(self, jogador: "Jogador") -> None:
        """Ação simplificada: se há proprietário diferente, cobra aluguel stub."""
        pass