"""
Pacote com componentes visuais reutilizáveis do Monopoly em Pygame.

Cada componente expõe uma interface simples para construir superfícies
(`pygame.Surface`) que podem ser reutilizadas pelo jogo principal.
"""

from .base import UIComponent
from .property_card import PropertyCard
from .event_card import EventCard
from .house_token import HouseToken
from .board import GameBoard
from .theme import Theme

__all__ = [
    "UIComponent",
    "PropertyCard",
    "EventCard",
    "HouseToken",
    "GameBoard",
    "Theme",
]
