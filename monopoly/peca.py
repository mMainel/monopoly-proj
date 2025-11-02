from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Peca:
    """Representa a peça física do jogador no tabuleiro."""

    identificador: str
    posicao: int = 0

    def mover_passos(self, passos: int, tamanho_tabuleiro: int | None = None) -> int:
        """
        Avança a peça uma quantidade de passos.

        Args:
            passos: Quantidade de casas a avançar (pode ser negativa).
            tamanho_tabuleiro: Número total de casas para calcular volta completa.

        Returns:
            A nova posição da peça após o movimento.
        """
        if tamanho_tabuleiro is not None and tamanho_tabuleiro <= 0:
            raise ValueError("tamanho_tabuleiro deve ser positivo")

        nova_posicao = self.posicao + passos
        if tamanho_tabuleiro:
            nova_posicao %= tamanho_tabuleiro

        self.posicionar(nova_posicao)
        return self.posicao

    def posicionar(self, posicao: int) -> None:
        """Posiciona a peça em uma casa específica do tabuleiro."""
        if posicao < 0:
            raise ValueError("posicao não pode ser negativa")

        self.posicao = posicao
