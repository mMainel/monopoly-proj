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
            pass
    return pygame.font.SysFont("arial", size)


class EventCard(UIComponent):
    """
    Carta de evento no formato clássico de Sorte/Cofre.

    O corpo da carta pode ser informado como string (com quebras de linha opcionais)
    ou como uma sequência de linhas. O layout segue o cartão horizontal com moldura dupla,
    título superior e texto centralizado.
    """

    def __init__(
        self,
        title: str = "SORTE",
        body: str | Iterable[str] | None = None,
        footer: str = "UFFOPOLY",
        accent_color: Tuple[int, int, int] | None = None,
        width: int = 480,
        height: int = 300,
        position: Tuple[int, int] = (0, 0),
        theme: Theme | None = None,
    ) -> None:
        super().__init__(width=width, height=height, position=position)
        self.title = title.upper()
        self.body_lines = self._normalize_body(body)
        self.footer = footer.upper()
        self.accent_color = accent_color
        self.theme = theme or Theme()

    def build(self) -> pygame.Surface:
        surface = super().build()
        surface.fill(self.theme.background)
        self._draw_border(surface)
        self._draw_title(surface)
        self._draw_body(surface)
        self._draw_footer(surface)
        return surface

    def _draw_border(self, surface: pygame.Surface) -> None:
        outer_rect = surface.get_rect()
        pygame.draw.rect(surface, self.theme.outline, outer_rect, width=2)

        inset = 24
        inner_rect = outer_rect.inflate(-inset, -inset)
        pygame.draw.rect(surface, self.theme.outline, inner_rect, width=1)

        self._outer_rect = outer_rect
        self._inner_rect = inner_rect

    def _draw_title(self, surface: pygame.Surface) -> None:
        font = _resolve_font(self.theme.card_font, 36)
        text = font.render(self.title, True, self.theme.text_primary)
        text_rect = text.get_rect()
        text_rect.centerx = self.width // 2
        text_rect.top = self._inner_rect.top + 20
        surface.blit(text, text_rect)

    def _draw_body(self, surface: pygame.Surface) -> None:
        font = _resolve_font(self.theme.small_font or self.theme.card_font, 22)
        max_width = self._inner_rect.width - 60
        wrapped_lines = self._wrap_lines(self.body_lines, font, max_width=max_width)

        if not wrapped_lines:
            return

        total_height = sum(font.size(line)[1] for line in wrapped_lines) + (len(wrapped_lines) - 1) * 6
        start_y = self._inner_rect.centery - total_height // 2

        for line in wrapped_lines:
            text = font.render(line, True, self.theme.text_secondary)
            text_rect = text.get_rect(center=(self.width // 2, start_y + text.get_height() // 2))
            surface.blit(text, text_rect)
            start_y += text.get_height() + 6

    def _draw_footer(self, surface: pygame.Surface) -> None:
        font = _resolve_font(self.theme.small_font or self.theme.card_font, 18)
        text = font.render(self.footer, True, self.theme.text_primary)
        text_rect = text.get_rect(center=(self.width // 2, self._inner_rect.bottom - 28))

        line_color = self.accent_color or self.theme.outline
        line_y = text_rect.centery
        gap = 18
        margin = self._inner_rect.left + 6
        right_margin = self._inner_rect.right - 6

        left_start = (margin, line_y)
        left_end = (max(text_rect.left - gap, margin), line_y)
        right_start = (min(text_rect.right + gap, right_margin), line_y)
        right_end = (right_margin, line_y)

        if left_end[0] > left_start[0]:
            pygame.draw.line(surface, line_color, left_start, left_end, width=2)
        if right_end[0] > right_start[0]:
            pygame.draw.line(surface, line_color, right_start, right_end, width=2)

        surface.blit(text, text_rect)

    def _normalize_body(self, body: str | Iterable[str] | None) -> list[str]:
        if body is None:
            return ["VOCÊ RECEBEU UM BÔNUS DE R$ 50."]
        if isinstance(body, str):
            split_lines = body.splitlines() or [body]
            return [line.strip().upper() for line in split_lines if line.strip()]
        return [str(line).strip().upper() for line in body if str(line).strip()]

    def _wrap_lines(
        self,
        lines: Iterable[str],
        font: pygame.font.Font,
        max_width: int,
    ) -> list[str]:
        wrapped: list[str] = []
        for line in lines:
            wrapped.extend(self._wrap_text(line, font, max_width))
        return wrapped

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current: list[str] = []

        for word in words:
            test_line = " ".join(current + [word])
            if font.size(test_line)[0] <= max_width:
                current.append(word)
                continue

            if current:
                lines.append(" ".join(current))
            current = [word]

        if current:
            lines.append(" ".join(current))

        return lines
