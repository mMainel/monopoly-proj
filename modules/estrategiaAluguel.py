from __future__ import annotations

from typing import Dict


class estrategiaAluguel():
    """Estratégia para cálculo de aluguel de propriedades."""
    @staticmethod
    def calcula(base: int, conteudo: Dict) -> int:
        """
        método estático para calcular o aluguel com base em parâmetros fornecidos.
        Args:
            base (int): Valor base para o cálculo do aluguel.
            conteudo (Dict): Dicionário contendo informações adicionais necessárias para o cálculo.
        example:
            modelo de conteúdo
            ```python
                conteudo = {
                    "casa": 2,
                    "hetel": 0,
                    "monopolio": Fase
                    }
            ```
        """
        valores_aluguel = [200, # 1 construção
                           600, # 2 construções
                           1400,# 3 construções
                           1700,# 4 construções
                           2000 # hotel
                          ]
        if conteudo.get('hotel', 0) > 0:
            return valores_aluguel[4]
        elif conteudo.get('casa', 0) > 0:
            casas = conteudo['casa']
            return valores_aluguel[casas - 1]
        aluguel = base
        if conteudo.get('monopolio', False):
            aluguel *= 2
        return aluguel
    

# if __name__ == "__main__":
#     print(estrategiaAluguel.calcula(20, {'casa':3})) # Exemplo de chamada do método estático