from __future__ import annotations

from typing import Tuple

import pygame

from .base import UIComponent
from .theme import Theme


class HouseToken(UIComponent):
    """
    Marcador simples para casas/hotéis utilizados no tabuleiro.
    """

    def __init__(
        self,
        color: Tuple[int, int, int] = (20, 140, 20),
        width: int = 28,
        height: int = 28,
        position: Tuple[int, int] = (0, 0),
        theme: Theme | None = None,
        hotel: bool = False,
    ) -> None:
        super().__init__(width=width, height=height, position=position, transparent=True)
        self.color = color
        self.theme = theme or Theme()
        self.hotel = hotel

    def build(self) -> pygame.Surface:
        surface = super().build()
        surface.fill((0, 0, 0, 0))

        base_rect = pygame.Rect(0, self.height // 4, self.width, self.height - self.height // 4)
        pygame.draw.rect(surface, self.color, base_rect, border_radius=4)
        pygame.draw.rect(surface, self.theme.outline, base_rect, width=2, border_radius=4)

        roof_height = int(self.height * (0.5 if not self.hotel else 0.65))
        roof_points = [
            (0, self.height // 4),
            (self.width // 2, self.height // 4 - roof_height // 2),
            (self.width, self.height // 4),
        ]
        pygame.draw.polygon(surface, self.color, roof_points)
        pygame.draw.lines(surface, self.theme.outline, False, roof_points, width=2)

        if self.hotel:
            door_rect = pygame.Rect(self.width // 2 - 6, self.height // 2, 12, self.height // 3)
            pygame.draw.rect(surface, self.theme.background, door_rect, border_radius=2)
            pygame.draw.rect(surface, self.theme.outline, door_rect, width=2, border_radius=2)

        return surface
