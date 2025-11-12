from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    """
    Coleção centralizada de cores e fontes utilizadas pelos componentes.

    Os valores são fornecidos em RGB. Ajuste os tons conforme a identidade visual
    do projeto. Fontes podem ser definidas via caminhos do sistema operacional.
    """

    background: tuple[int, int, int] = (255, 255, 255)
    text_primary: tuple[int, int, int] = (20, 20, 20)
    text_secondary: tuple[int, int, int] = (80, 80, 80)
    outline: tuple[int, int, int] = (0, 0, 0)
    section_header: tuple[int, int, int] = (230, 110, 40)
    chance_color: tuple[int, int, int] = (255, 140, 0)
    community_color: tuple[int, int, int] = (0, 160, 200)
    board_base: tuple[int, int, int] = (235, 235, 210)
    board_border: tuple[int, int, int] = (50, 50, 50)
    board_tile: tuple[int, int, int] = (220, 220, 220)

    card_font: str | None = None
    small_font: str | None = None
