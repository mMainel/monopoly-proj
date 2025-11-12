from __future__ import annotations

from typing import Iterable, Tuple

import pygame

from .base import UIComponent
from .theme import Theme


def _ensure_font_initialized() -> None:
    if not pygame.font.get_init():
        pygame.font.init()


def _resolve_font(path: str | None, size: int) -> pygame.font.Font:
    _ensure_font_initialized()
    if path:
        try:
            return pygame.font.Font(path, size)
        except OSError:
            # Se a fonte personalizada falhar, usamos a padrão do sistema
            pass
    return pygame.font.SysFont("arial", size)


class PropertyCard(UIComponent):
    """
    Componente visual para cartas de propriedades.

    Exemplo de uso:
        card = PropertyCard(
            name="Copacabana",
            color=(0, 155, 215),
            price=260,
            rents=[22, 110, 330, 800],
        )
        card_surface = card.surface
    """

    def __init__(
        self,
        name: str = "Nome da Propriedade",
        color_band: Tuple[int, int, int] = (0, 120, 190),
        price: int = 100,
        rents: Iterable[int] | None = None,
        house_cost: int | None = None,
        hotel_cost: int | None = None,
        width: int = 220,
        height: int = 340,
        position: Tuple[int, int] = (0, 0),
        theme: Theme | None = None,
    ) -> None:
        super().__init__(width=width, height=height, position=position)
        self.name = name
        self.color_band = color_band
        self.price = price
        self.rents = tuple(rents) if rents is not None else (10, 30, 90, 250)
        self.house_cost = house_cost
        self.hotel_cost = hotel_cost
        self.theme = theme or Theme()

    def build(self) -> pygame.Surface:
        # Inicializa a surface base
        surface = super().build()
        surface.fill(self.theme.background)
        self._draw_outline(surface)
        self._draw_color_band(surface)
        self._draw_title(surface)
        self._draw_rents(surface)
        self._draw_footer(surface)
        return surface

    def _draw_outline(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.theme.outline, surface.get_rect(), width=2, border_radius=8)

    def _draw_color_band(self, surface: pygame.Surface) -> None:
        color_rect = pygame.Rect(0, 0, self.width, int(self.height * 0.2))
        pygame.draw.rect(surface, self.color_band, color_rect, border_radius=8)
        pygame.draw.rect(surface, self.theme.outline, color_rect, width=2, border_radius=8)

    def _draw_title(self, surface: pygame.Surface) -> None:
        font = _resolve_font(self.theme.card_font, 20)
        text = font.render(self.name.upper(), True, self.theme.text_primary)
        text_rect = text.get_rect(center=(self.width // 2, int(self.height * 0.28)))
        surface.blit(text, text_rect)

    def _draw_rents(self, surface: pygame.Surface) -> None:
        font = _resolve_font(self.theme.small_font or self.theme.card_font, 16)
        y = int(self.height * 0.38)
        for idx, rent in enumerate(self.rents, start=1):
            if idx == 1:
                description = "Aluguel base"
            elif idx <= 5:
                description = f"Com {idx - 1} casa(s)"
            else:
                description = "Com hotel"
            rent_label = font.render(description, True, self.theme.text_secondary)
            value_label = font.render(f"R$ {rent}", True, self.theme.text_primary)
            surface.blit(rent_label, (16, y))
            surface.blit(value_label, (self.width - value_label.get_width() - 16, y))
            y += rent_label.get_height() + 6

    def _draw_footer(self, surface: pygame.Surface) -> None:
        font = _resolve_font(self.theme.small_font or self.theme.card_font, 14)
        parts: list[str] = [f"Preço: R$ {self.price}"]
        if self.house_cost is not None:
            parts.append(f"Casa: R$ {self.house_cost}")
        if self.hotel_cost is not None:
            parts.append(f"Hotel: R$ {self.hotel_cost}")
        footer_text = " | ".join(parts)

        text_surface = font.render(footer_text, True, self.theme.text_secondary)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height - 28))
        surface.blit(text_surface, text_rect)
