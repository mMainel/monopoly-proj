from abc import ABC, abstractmethod

class EstrategiaAluguel(ABC):
    """
    Classe abstrata que define o contrato para estratégias de cálculo de aluguel
    """

    @abstractmethod
    def calcular(self, titulo, valor_dados: int = 0) -> int:
        """
        Calcula o aluguel de um título baseado em suas características

        espera:
            titulo: Titulo - título para calcular aluguel
            valor_dados: int - soma dos dados (usado por companhias)
        retorna:
            int - valor do aluguel
        """
        pass

class EstrategiaAluguelPropriedade(EstrategiaAluguel):
    """
    Estratégia para calcular aluguel de propriedades com casas/hotéis
    """

    def calcular(self, titulo) -> int:
        """
        Calcula aluguel baseado em casas, hotéis e monopolio

        espera:
            titulo: TituloPropriedade - propriedade
        retorna:
            int - valor do aluguel
        """
        if titulo.estaHipotecada():
            return 0

        if titulo.tem_hotel:
            return titulo.alugueis[5] if len(titulo.alugueis) > 5 else titulo.alugueis[-1]

        if titulo.num_casas > 0:
            return titulo.alugueis[titulo.num_casas]

        if titulo.proprietario and titulo.proprietario.possuiMonopolio(titulo.cor):
            return titulo.aluguel_base * 2

        return titulo.aluguel_base

class EstrategiaAluguelEstacao(EstrategiaAluguel):
    """
    Estratégia para calcular aluguel de estações ferroviárias
    """

    def calcular(self, titulo, valor_dados: int = 0) -> int:
        """
        Calcula aluguel baseado no número de estações do proprietário

        espera:
            titulo: TituloEstacao - estação
            valor_dados: int - não utilizado
        retorna:
            int - valor do aluguel
        """
        if titulo.estaHipotecada():
            return 0

        if titulo.proprietario is None:
            return 0

        num_estacoes = titulo.contarEstacoesProprietario()

        if num_estacoes <= 0 or num_estacoes > 4:
            return 0

        return titulo.alugueis[num_estacoes - 1]

class EstrategiaAluguelCompanhia(EstrategiaAluguel):
    """
    Estratégia para calcular aluguel de companhias de utilidades
    """

    def calcular(self, titulo, valor_dados: int = 0) -> int:
        """
        Calcula aluguel baseado nos dados e quantidade de companhias

        espera:
            titulo: TituloCompanhia - companhia
            valor_dados: int - soma dos dados rolados
        retorna:
            int - valor do aluguel
        """
        if titulo.estaHipotecada():
            return 0

        if titulo.proprietario is None:
            return 0

        if valor_dados <= 0:
            return 0

        num_companhias = titulo.contarCompanhiasProprietario()

        if num_companhias >= 2:
            return valor_dados * titulo.fator_duas_companhias
        elif num_companhias == 1:
            return valor_dados * titulo.fator_uma_companhia

        return 0
