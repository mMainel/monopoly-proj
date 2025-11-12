from typing import Optional
from modules.tituloCompanhia import TituloCompanhia
from modules.tituloEstacao import TituloEstacao

class Regras:
    """
    Centraliza as regras e validações do Monopoly
    Define constantes do jogo e métodos para validar ações
    """

    DINHEIRO_INICIAL: int = 1500
    SALARIO_VOLTA: int = 200
    FIANCA_CADEIA: int = 50
    MAX_CASAS: int = 4
    MAX_DUPLAS: int = 3

    def validar_compra(self, jogador: object, propriedade: object) -> bool:
        """
        Verifica se um jogador pode comprar uma propriedade

        espera:
            jogador: Jogador - jogador que deseja comprar
            propriedade: Titulo - propriedade a ser comprada
        retorna:
            bool - True se pode comprar, False caso contrário
        """
        if propriedade.proprietario is not None:
            return False

        if jogador.getSaldo() < propriedade.getPreco():
            return False

        return True

    def validar_construcao(self, jogador: object, propriedade: object) -> bool:
        """
        Verifica se pode construir casa/hotel em uma propriedade

        espera:
            jogador: Jogador - jogador que deseja construir
            propriedade: TituloPropriedade - propriedade onde construir
        retorna:
            bool - True se pode construir, False caso contrário
        """
        if propriedade.proprietario != jogador:
            return False

        if not hasattr(propriedade, 'num_casas'):
            return False

        if propriedade.num_casas >= self.MAX_CASAS:
            return False

        if jogador.getSaldo() < propriedade.getCustoCasa():
            return False

        return True

    def calcular_aluguel(self, propriedade: object, dados: object = None) -> int:
        """
        Calcula o valor do aluguel de uma propriedade

        espera:
            propriedade: Titulo - propriedade para calcular aluguel
            dados: Dados - instancia dos dados (necessario para Companhias)
        retorna:
            int - valor do aluguel
        """

        if propriedade.estaHipotecada():
            return 0

        if isinstance(propriedade, TituloCompanhia):
            if dados and hasattr(dados, 'soma_dados'):
                valor_dados = dados.soma_dados()
                return propriedade.calcularAluguel(valor_dados)
            return 0

        if isinstance(propriedade, TituloEstacao):
            return propriedade.calcularAluguel()

        return propriedade.calcularAluguel()

    def obter_saldo_inicial(self) -> int:
        """
        Retorna o saldo inicial de cada jogador

        espera:
            nenhum parâmetro
        retorna:
            int - saldo inicial
        """
        return self.DINHEIRO_INICIAL

    def obter_salario_inicio(self) -> int:
        """
        Retorna o valor recebido ao passar pelo Início

        espera:
            nenhum parâmetro
        retorna:
            int - valor do salário
        """
        return self.SALARIO_VOLTA

    def obter_valor_prisao(self) -> int:
        """
        Retorna o valor da fiança para sair da prisão

        espera:
            nenhum parâmetro
        retorna:
            int - valor da fiança
        """
        return self.FIANCA_CADEIA

    def obter_max_casas(self) -> int:
        """
        Retorna o número máximo de casas por propriedade

        espera:
            nenhum parâmetro
        retorna:
            int - máximo de casas
        """
        return self.MAX_CASAS

    def obter_max_duplas(self) -> int:
        """
        Retorna o número máximo de duplas consecutivas antes de ir preso

        espera:
            nenhum parâmetro
        retorna:
            int - máximo de duplas
        """
        return self.MAX_DUPLAS

    def _tem_conjunto_completo(self, jogador: object, cor: str) -> bool:
        """
        Verifica se jogador possui todas as propriedades de uma cor

        espera:
            jogador: Jogador - jogador a verificar
            cor: str - cor do grupo a verificar
        retorna:
            bool - True se possui monopolio, False caso contrário
        """
        grupos_propriedades = {
            "Marrom": 2,
            "Azul Claro": 3,
            "Rosa": 3,
            "Laranja": 3,
            "Vermelho": 3,
            "Amarelo": 3,
            "Verde": 3,
            "Azul Escuro": 2
        }

        if cor not in grupos_propriedades:
            return False

        total_necessario = grupos_propriedades[cor]
        propriedades_jogador = jogador.getPropriedades()

        propriedades_cor = [p for p in propriedades_jogador
                           if hasattr(p, 'cor') and p.cor == cor]

        return len(propriedades_cor) >= total_necessario

    def _total_propriedades_grupo(self, cor: str) -> int:
        """
        Retorna o número total de propriedades em um grupo de cor

        espera:
            cor: str - cor do grupo
        retorna:
            int - quantidade total de propriedades no grupo
        """
        grupos_propriedades = {
            "Marrom": 2,
            "Azul Claro": 3,
            "Rosa": 3,
            "Laranja": 3,
            "Vermelho": 3,
            "Amarelo": 3,
            "Verde": 3,
            "Azul Escuro": 2
        }
        return grupos_propriedades.get(cor, 0)