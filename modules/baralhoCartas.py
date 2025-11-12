import random
from typing import List
from modules.carta import Carta, TipoCarta

class BaralhoCartas:
    """
    Gerencia um baralho de cartas do jogo
    Permite embaralhar, sacar e retornar cartas ao baralho
    """

    def __init__(self, tipo: TipoCarta):
        self.cartas: List[Carta] = []
        self.tipo = tipo

    def embaralhar(self) -> None:
        """
        Embaralha as cartas do baralho aleatoriamente

        espera:
            nenhum parâmetro
        retorna:
            None
        """
        random.shuffle(self.cartas)

    def sacarCarta(self) -> Carta:
        """
        Remove e retorna a carta do topo do baralho
        Se o baralho estiver vazio, retorna None

        espera:
            nenhum parâmetro
        retorna:
            Carta - carta do topo ou None se vazio
        """
        if len(self.cartas) > 0:
            carta = self.cartas.pop(0)
            return carta
        return None

    def retornarCarta(self, carta: Carta) -> None:
        """
        Retorna uma carta ao final do baralho

        espera:
            carta: Carta - carta a ser devolvida
        retorna:
            None
        """
        if carta is not None:
            self.cartas.append(carta)

    def adicionarCarta(self, carta: Carta) -> None:
        """
        Adiciona uma nova carta ao baralho

        espera:
            carta: Carta - carta a ser adicionada
        retorna:
            None
        """
        if carta is not None:
            self.cartas.append(carta)

    def getTipo(self) -> TipoCarta:
        """
        Retorna o tipo do baralho

        espera:
            nenhum parâmetro
        retorna:
            TipoCarta - tipo do baralho (SORTE ou REVES)
        """
        return self.tipo

    def getTamanho(self) -> int:
        """
        Retorna o número de cartas no baralho

        espera:
            nenhum parâmetro
        retorna:
            int - quantidade de cartas
        """
        return len(self.cartas)

    def estaVazio(self) -> bool:
        """
        Verifica se o baralho está vazio

        espera:
            nenhum parâmetro
        retorna:
            bool - True se vazio, False caso contrário
        """
        return len(self.cartas) == 0