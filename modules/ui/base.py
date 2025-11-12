from __future__ import annotations

from typing import Optional, Tuple

import pygame


class UIComponent:
    """
    Classe base para componentes visuais reutilizáveis.

    Cada componente possui uma superfície própria e sabe como desenhá-la.
    A renderização acontece através do método `draw`, que blita a superfície
    interna em uma superfície alvo fornecida (por exemplo, a tela principal).
    """

    def __init__(
        self,
        width: int,
        height: int,
        position: Tuple[int, int] = (0, 0),
        transparent: bool = False,
    ) -> None:
        self.width = width
        self.height = height
        self.position = position
        self.transparent = transparent
        self._surface: Optional[pygame.Surface] = None

    def build(self) -> pygame.Surface:
        """
        Gera a superfície interna do componente.

        Subclasses devem sobrescrever este método para personalizar o desenho.
        """
        flags = pygame.SRCALPHA if self.transparent else 0
        surface = pygame.Surface((self.width, self.height), flags=flags)
        return surface

    @property
    def surface(self) -> pygame.Surface:
        """
        Retorna a superfície do componente, reconstruindo-a se necessário.
        """
        if self._surface is None:
            self._surface = self.build()
        return self._surface

    def invalidate(self) -> None:
        """
        Marca a superfície como desatualizada, forçando rebuild no próximo acesso.
        """
        self._surface = None

    def draw(self, target: pygame.Surface) -> None:
        """
        Blita a superfície do componente na superfície alvo.
        """
        target.blit(self.surface, self.position)
