from titulo import Titulo

class TituloEstacao(Titulo):
    """
    Representa um título de estação ferroviária
    O aluguel aumenta conforme o número de estações que o proprietário possui
    """

    def __init__(self, nome: str, preco: int):
        super().__init__(nome, preco)
        self.tipo = "Estacao"
        self.aluguel_base = 25
        self.alugueis = [25, 50, 100, 200]

    def calcularAluguel(self) -> int:
        """
        Calcula o aluguel baseado no número de estações do proprietário

        espera:
            nenhum parâmetro
        retorna:
            int - valor do aluguel calculado
        """
        if self.hipotecada:
            return 0

        if self.proprietario is None:
            return 0

        num_estacoes = self.contarEstacoesProprietario()

        if num_estacoes <= 0 or num_estacoes > 4:
            return 0

        return self.alugueis[num_estacoes - 1]

    def contarEstacoesProprietario(self) -> int:
        """
        Conta quantas estações o proprietário possui

        espera:
            nenhum parâmetro
        retorna:
            int - número de estações do proprietário
        """
        if self.proprietario is None:
            return 0

        estacoes = self.proprietario.getPropriedadesPorTipo(TituloEstacao)
        return len(estacoes)

    def setAlugueis(self, alugueis: list) -> None:
        """
        Define os valores de aluguel para 1, 2, 3 e 4 estações

        espera:
            alugueis: list - lista com 4 valores de aluguel
        retorna:
            None
        """
        if len(alugueis) == 4:
            self.alugueis = alugueis.copy()

    # GETTERS

    def getAluguelBase(self) -> int:
        """
        Retorna o aluguel base com uma estação

        espera:
            nenhum parâmetro
        retorna:
            int - aluguel base
        """
        return self.aluguel_base

    def getAlugueis(self) -> list:
        """
        Retorna a lista de alugueis por número de estações

        espera:
            nenhum parâmetro
        retorna:
            list - lista com valores para 1, 2, 3 e 4 estações
        """
        return self.alugueis.copy()

    def getTipo(self) -> str:
        """
        Retorna o tipo do título

        espera:
            nenhum parâmetro
        retorna:
            str - tipo do título
        """
        return self.tipo