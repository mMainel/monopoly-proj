from typing import Optional

"""
Stub mínimo da classe Jogador para o jogo Monopoly.
Local: monopoly/Jogador.py
"""



class Jogador:
    """
    Representa um jogador no jogo.
    A implementação aqui é mínima e pode ser estendida conforme a lógica do jogo.
    """

    def __init__(self, nome: str, saldo: int = 1500, posicao: int = 0):
        self.nome: str = nome
