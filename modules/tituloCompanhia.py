from titulo import Titulo

class TituloCompanhia(Titulo):
    """
    Representa um título de companhia de utilidades
    O aluguel é calculado com base no resultado dos dados multiplicado por um fator
    """

    def __init__(self, nome: str, preco: int):
        super().__init__(nome, preco)
        self.tipo = "Companhia"
        self.fator_uma_companhia = 4
        self.fator_duas_companhias = 10

    def calcularAluguel(self, valor_dados: int = 0) -> int:
        """
        Calcula o aluguel baseado no valor dos dados e quantas companhias o proprietário possui

        espera:
            valor_dados: int - soma dos dados rolados pelo jogador
        retorna:
            int - valor do aluguel calculado
        """
        if self.hipotecada:
            return 0

        if self.proprietario is None:
            return 0

        if valor_dados <= 0:
            return 0

        num_companhias = self.contarCompanhiasProprietario()

        if num_companhias >= 2:
            return valor_dados * self.fator_duas_companhias
        elif num_companhias == 1:
            return valor_dados * self.fator_uma_companhia

        return 0

    def contarCompanhiasProprietario(self) -> int:
        """
        Conta quantas companhias o proprietário possui

        espera:
            nenhum parâmetro
        retorna:
            int - número de companhias do proprietário
        """
        if self.proprietario is None:
            return 0

        companhias = self.proprietario.getPropriedadesPorTipo(TituloCompanhia)
        return len(companhias)

    def setFatorAluguel(self, fator_uma: int, fator_duas: int) -> None:
        """
        Define os fatores multiplicadores de aluguel

        espera:
            fator_uma: int - multiplicador com uma companhia
            fator_duas: int - multiplicador com duas companhias
        retorna:
            None
        """
        if fator_uma > 0:
            self.fator_uma_companhia = fator_uma
        if fator_duas > 0:
            self.fator_duas_companhias = fator_duas

    # GETTERS

    def getFatorUmaCompanhia(self) -> int:
        """
        Retorna o fator multiplicador quando possui uma companhia

        espera:
            nenhum parâmetro
        retorna:
            int - fator multiplicador
        """
        return self.fator_uma_companhia

    def getFatorDuasCompanhias(self) -> int:
        """
        Retorna o fator multiplicador quando possui duas companhias

        espera:
            nenhum parâmetro
        retorna:
            int - fator multiplicador
        """
        return self.fator_duas_companhias

    def getTipo(self) -> str:
        """
        Retorna o tipo do título

        espera:
            nenhum parâmetro
        retorna:
            str - tipo do título
        """
        return self.tipo