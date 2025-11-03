from random import randint
from typing import List

class Dados:
    """
    Representa um par de dados de seis faces
    Armazena o resultado do último lançamento e permite verificar duplas
    """

    def __init__(self):
        self.ultimo_lancamento: tuple[int, int] | None = None

    def lancar(self) -> List[int]:
        """
        Lança os dois dados e armazena o resultado

        espera:
            nenhum parâmetro
        retorna:
            List[int] - tupla com os valores dos dois dados
        """
        resultado_1 = randint(1, 6)
        resultado_2 = randint(1, 6)
        self.ultimo_lancamento = (resultado_1, resultado_2)
        return self.ultimo_lancamento

    def isDupla(self) -> bool:
        """
        Verifica se o último lançamento foi uma dupla

        espera:
            nenhum parâmetro
        retorna:
            bool - True se ambos os dados têm o mesmo valor
        """
        if self.ultimo_lancamento is None:
            raise ValueError("Nenhum lançamento foi realizado")
        return self.ultimo_lancamento[0] == self.ultimo_lancamento[1]

    def soma_dados(self) -> int:
        """
        Retorna a soma dos valores do último lançamento

        espera:
            nenhum parâmetro
        retorna:
            int - soma dos dois dados
        """
        if self.ultimo_lancamento is None:
            raise ValueError("Nenhum lançamento foi realizado")
        return self.ultimo_lancamento[0] + self.ultimo_lancamento[1]

