"""
Roda uma prévia simples dos componentes visuais em uma janela Pygame.

Execute: `python -m modules.ui.demo`

Use este arquivinho apenas como referência rápida para visualizar o layout.
"""

from __future__ import annotations

import pygame

from . import EventCard, GameBoard, HouseToken, PropertyCard, Theme


def init_window(width: int, height: int) -> pygame.Surface:
    pygame.init()
    pygame.display.set_caption("Preview UI Monopoly")
    return pygame.display.set_mode((width, height))


def main() -> None:
    theme = Theme()
    screen = init_window(1024, 768)
    clock = pygame.time.Clock()

    property_card = PropertyCard(
        name="Copacabana",
        color_band=(80, 160, 255),
        price=260,
        rents=(22, 110, 330, 800, 975),
        house_cost=150,
        hotel_cost=200,
        position=(40, 40),
        theme=theme,
    )

    chance_card = EventCard(
        title="SORTE",
        body="Avance até o início e receba R$ 200.\nSe passar novamente, receba mais R$ 200.",
        accent_color=theme.outline,
        position=(320, 60),
        theme=theme,
    )

    reves_card = EventCard(
        title="COFRE",
        body="Lanche na engenharia.\nPague M$15.",
        accent_color=theme.outline,
        position=(540, 60),
        theme=theme,
    )

    board = GameBoard(
        tile_size=48,
        labels=_load_default_labels(),
        position=(350, 260),
        theme=theme,
    )

    house = HouseToken(position=(80, 420))
    hotel = HouseToken(color=(200, 20, 20), position=(120, 420), hotel=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((32, 34, 36))
        screen.blit(property_card.surface, property_card.position)
        screen.blit(chance_card.surface, chance_card.position)
        screen.blit(reves_card.surface, reves_card.position)
        screen.blit(board.surface, board.position)
        house.draw(screen)
        hotel.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def _load_default_labels() -> list[str]:
    return [
        "Início",
        "Leblon",
        "Sorte",
        "Av. Pres",
        "Copacabana",
        "Imposto",
        "Companhia",
        "Av. Paulista",
        "Revés",
        "Ipanema",
        "Prisão",
        "Botafogo",
        "Companhia",
        "Flamengo",
        "Sorte",
        "Centro",
        "Eventos",
        "Lapa",
        "Revés",
        "Glória",
        "Estacionar",
        "Moema",
        "Sorte",
        "Jardins",
        "Higienópolis",
        "Companhia",
        "Itaim",
        "Sorte",
        "Pinheiros",
        "Prisões",
        "Vila Olímpia",
        "Revés",
        "Morumbi",
        "Companhia",
        "Brooklin",
        "Sorte",
        "Berrini",
        "Imposto",
        "Aeroporto",
        "Início",
    ]


if __name__ == "__main__":
    main()
