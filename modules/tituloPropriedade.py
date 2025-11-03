from typing import List
from titulo import Titulo
from regras import Regras

class TituloPropriedade(Titulo):
    """
    Representa um título de propriedade de lote colorido
    Permite construção de casas e hotéis com aluguel variável baseado em desenvolvimento
    """

    def __init__(self, nome: str, preco: int, cor: str, aluguel_base: int,
                 alugueis: List[int], custo_casa: int):
        super().__init__(nome, preco)
        self.cor = cor
        self.aluguel_base = aluguel_base
        self.alugueis = alugueis
        self.custo_casa = custo_casa
        self.num_casas = 0
        self.tem_hotel = False

    def calcularAluguel(self) -> int:
        """
        Calcula o aluguel baseado no número de casas/hotel e monopolio

        espera:
            nenhum parâmetro
        retorna:
            int - valor do aluguel atual
        """
        if self.hipotecada:
            return 0

        if self.tem_hotel:
            return self.alugueis[5] if len(self.alugueis) > 5 else self.alugueis[-1]

        if self.num_casas > 0:
            return self.alugueis[self.num_casas]

        if self.proprietario and self.proprietario.possuiMonopolio(self.cor):
            return self.aluguel_base * 2

        return self.aluguel_base

    def construirCasa(self) -> bool:
        """
        Constrói uma casa na propriedade se regras permitirem

        espera:
            nenhum parâmetro
        retorna:
            bool - True se construiu, False se não pode
        """
        if self.tem_hotel:
            return False

        if self.hipotecada:
            return False

        if self.proprietario is None:
            return False

        if not self.proprietario.possuiMonopolio(self.cor):
            return False

        regras = Regras()
        if self.num_casas >= regras.obter_max_casas():
            return False

        if self.proprietario.getSaldo() < self.custo_casa:
            return False

        if self.proprietario.pagarAoBanco(self.custo_casa):
            self.num_casas += 1
            return True

        return False

    def construirHotel(self) -> bool:
        """
        Constrói um hotel substituindo 4 casas

        espera:
            nenhum parâmetro
        retorna:
            bool - True se construiu hotel, False se não pode
        """
        if self.tem_hotel:
            return False

        if self.hipotecada:
            return False

        if self.proprietario is None:
            return False

        regras = Regras()
        if self.num_casas < regras.obter_max_casas():
            return False

        if self.proprietario.getSaldo() < self.custo_casa:
            return False

        if self.proprietario.pagarAoBanco(self.custo_casa):
            self.num_casas = 0
            self.tem_hotel = True
            return True

        return False

    def venderCasa(self) -> bool:
        """
        Vende uma casa recebendo metade do valor de volta

        espera:
            nenhum parâmetro
        retorna:
            bool - True se vendeu, False se não havia casas
        """
        if self.num_casas > 0:
            self.num_casas -= 1
            valor_venda = self.custo_casa // 2
            if self.proprietario:
                self.proprietario.receberDinheiro(valor_venda)
            return True

        return False

    def venderHotel(self) -> bool:
        """
        Vende o hotel recebendo metade do valor e transformando em 4 casas

        espera:
            nenhum parâmetro
        retorna:
            bool - True se vendeu hotel, False se não havia
        """
        if self.tem_hotel:
            self.tem_hotel = False
            regras = Regras()
            self.num_casas = regras.obter_max_casas()
            valor_venda = self.custo_casa // 2
            if self.proprietario:
                self.proprietario.receberDinheiro(valor_venda)
            return True

        return False

    def podeHipotecar(self) -> bool:
        """
        Verifica se a propriedade pode ser hipotecada

        espera:
            nenhum parâmetro
        retorna:
            bool - True se pode hipotecar, False se tem construções
        """
        return self.num_casas == 0 and not self.tem_hotel

    def hipotecar(self) -> int:
        """
        Hipoteca a propriedade se não houver construções

        espera:
            nenhum parâmetro
        retorna:
            int - valor recebido pela hipoteca ou 0 se não pode
        """
        if not self.podeHipotecar():
            return 0

        return super().hipotecar()

    # GETTERS

    def getCor(self) -> str:
        """
        Retorna a cor/grupo da propriedade

        espera:
            nenhum parâmetro
        retorna:
            str - nome da cor
        """
        return self.cor

    def getNumCasas(self) -> int:
        """
        Retorna o número de casas construídas

        espera:
            nenhum parâmetro
        retorna:
            int - quantidade de casas
        """
        return self.num_casas

    def temHotel(self) -> bool:
        """
        Verifica se há hotel construído

        espera:
            nenhum parâmetro
        retorna:
            bool - True se tem hotel, False caso contrário
        """
        return self.tem_hotel

    def getCustoCasa(self) -> int:
        """
        Retorna o custo para construir casa/hotel

        espera:
            nenhum parâmetro
        retorna:
            int - custo de construção
        """
        return self.custo_casa

    def getAluguelBase(self) -> int:
        """
        Retorna o aluguel base sem casas ou monopolio

        espera:
            nenhum parâmetro
        retorna:
            int - aluguel base
        """
        return self.aluguel_base

    def getAlugueis(self) -> List[int]:
        """
        Retorna a lista de alugueis por número de casas

        espera:
            nenhum parâmetro
        retorna:
            List[int] - lista de valores de aluguel
        """
        return self.alugueis.copy()