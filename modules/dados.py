from random import randint
from typing import List

class Dados:
    """
    Representa um par de dados de seis faces
    """
    def __init__(self):
        self.ultimo_lancamento: tuple[int, int] | None = None
    
    def lancar(self) -> List[int]:
        resultado_1 = randint(1,6)
        resultado_2 = randint(1,6)
        self.ultimo_lancamento = (resultado_1, resultado_2)
        return self.ultimo_lancamento
    
    def isDupla(self) -> bool:
        if self.ultimo_lancamento is None:
            raise ValueError("Nenhum lançamento foi realizado")
        return self.ultimo_lancamento[0] == self.ultimo_lancamento[1]
    
    def soma_dados(self) -> int:
        if self.ultimo_lancamento is None:
            raise ValueError("Nenhum lançamento foi realizado")
        return self.ultimo_lancamento[0] + self.ultimo_lancamento[1]

