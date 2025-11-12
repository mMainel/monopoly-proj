from __future__ import annotations

from typing import Iterable, Tuple

import pygame

from .base import UIComponent
from .theme import Theme


class GameBoard(UIComponent):
    """
    Tabuleiro básico 11x11 (estilo Monopoly) com tiles simples.

    Parâmetros:
        tile_size: tamanho de cada quadrado lateral
        labels: nomes curtos exibidos nas casas; deve conter 40 itens (perímetro)
    """

    def __init__(
        self,
        tile_size: int = 64,
        labels: Iterable[str] | None = None,
        position: Tuple[int, int] = (0, 0),
        theme: Theme | None = None,
    ) -> None:
        board_size = tile_size * 11
        super().__init__(width=board_size, height=board_size, position=position)
        self.tile_size = tile_size
        self.labels = list(labels or [])
        self.theme = theme or Theme()

    def build(self) -> pygame.Surface:
        surface = super().build()
        surface.fill(self.theme.board_base)
        self._draw_border(surface)
        self._draw_tiles(surface)
        self._draw_center(surface)
        return surface

    def _draw_border(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.theme.board_border, surface.get_rect(), width=6)

    def _draw_tiles(self, surface: pygame.Surface) -> None:
        tile = self.tile_size
        font = self._resolve_font(tile)

        perimeter_positions = self._perimeter_positions()

        for index, (x, y, orientation) in enumerate(perimeter_positions):
            rect = pygame.Rect(x, y, tile, tile)
            pygame.draw.rect(surface, self.theme.board_tile, rect, border_radius=4)
            pygame.draw.rect(surface, self.theme.board_border, rect, width=2, border_radius=4)

            label = self._label_for_index(index)
            if label:
                self._draw_label(surface, rect, label, font, orientation)

    def _draw_center(self, surface: pygame.Surface) -> None:
        center_rect = surface.get_rect().inflate(-self.tile_size * 4, -self.tile_size * 4)
        pygame.draw.rect(surface, self.theme.background, center_rect, border_radius=16)
        pygame.draw.rect(surface, self.theme.board_border, center_rect, width=4, border_radius=16)

        font = self._resolve_font(int(self.tile_size * 0.9))
        title = font.render("MONOPOLY", True, self.theme.text_primary)
        text_rect = title.get_rect(center=center_rect.center)
        surface.blit(title, text_rect)

    def _perimeter_positions(self) -> list[tuple[int, int, str]]:
        tile = self.tile_size
        size = self.width
        positions: list[tuple[int, int, str]] = []

        # Linha inferior (0-10)
        for i in range(11):
            x = size - tile * (i + 1)
            y = size - tile
            positions.append((x, y, "up"))

        # Coluna esquerda (11-20)
        for i in range(1, 11):
            x = 0
            y = size - tile * (i + 1)
            positions.append((x, y, "right"))

        # Linha superior (21-30)
        for i in range(1, 11):
            x = tile * (i - 1)
            y = 0
            positions.append((x, y, "down"))

        # Coluna direita (31-40)
        for i in range(1, 10):
            x = size - tile
            y = tile * i
            positions.append((x, y, "left"))

        return positions

    def _label_for_index(self, index: int) -> str:
        if index < len(self.labels):
            return self.labels[index]
        return ""

    def _resolve_font(self, size: int) -> pygame.font.Font:
        if not pygame.font.get_init():
            pygame.font.init()

        font_path = self.theme.small_font or self.theme.card_font
        if font_path:
            try:
                return pygame.font.Font(font_path, int(size * 0.18))
            except OSError:
                pass

        return pygame.font.SysFont("arial", int(size * 0.18))

    def _draw_label(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        label: str,
        font: pygame.font.Font,
        orientation: str,
    ) -> None:
        text = font.render(label, True, self.theme.text_secondary)
        text_rect = text.get_rect()

        if orientation == "up":
            text_rect.midtop = (rect.centerx, rect.bottom - text_rect.height - 4)
        elif orientation == "down":
            text_rect.midbottom = (rect.centerx, rect.y + text_rect.height + 4)
        elif orientation == "left":
            text_rect.midleft = (rect.x + 6, rect.centery)
        else:  # right
            text_rect.midright = (rect.right - 6, rect.centery)

        surface.blit(text, text_rect)
