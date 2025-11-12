from typing import List, Optional
from modules.espaco import (
    Espaco, EspacoInicio, EspacoCadeia, EspacoVaParaCadeia,
    EspacoEstacionamentoGratuito, EspacoImposto, EspacoCarta,
    EspacoPropriedade
)
from modules.tituloPropriedade import TituloPropriedade
from modules.tituloCompanhia import TituloCompanhia
from modules.tituloEstacao import TituloEstacao
from modules.baralhoCartas import BaralhoCartas
from modules.carta import CartaSairCadeia, TipoCarta
from modules.cartasJogo import criar_cartas_sorte, criar_cartas_cofre

class Tabuleiro:
    """
    Representa o tabuleiro do Monopoly
    Gerencia os espaços, propriedades e baralhos de cartas do jogo
    """

    def __init__(self):
        self.espacos: List[Espaco] = []
        self.baralho_sorte: Optional[BaralhoCartas] = None
        self.baralho_cofre: Optional[BaralhoCartas] = None
        self._inicializar_tabuleiro()
        self._inicializar_baralhos()

    def _inicializar_tabuleiro(self) -> None:
        """
        Cria os 40 espaços do tabuleiro

        espera:
            nenhum parâmetro
        retorna:
            None
        """
        self.espacos = [None] * 40

        self.espacos[0] = EspacoInicio()

        prop1 = TituloPropriedade("Arquivologia", 60, "Marrom", 2, [2, 10, 30, 90, 160, 250], 50)
        self.espacos[1] = EspacoPropriedade("Arquivologia", 1, prop1)

        self.espacos[2] = EspacoCarta("Cofre", 2, "Cofre")

        prop3 = TituloPropriedade("Artes", 60, "Marrom", 4, [4, 20, 60, 180, 320, 450], 50)
        self.espacos[3] = EspacoPropriedade("Artes", 3, prop3)

        self.espacos[4] = EspacoImposto("Pedágio da Ponte", 4, 200)

        estacao1 = TituloEstacao("Bandejão Gragoatá", 200)
        self.espacos[5] = EspacoPropriedade("Bandejão Gragoatá", 5, estacao1)

        prop6 = TituloPropriedade("Física", 100, "Azul Claro", 6, [6, 30, 90, 270, 400, 550], 50)
        self.espacos[6] = EspacoPropriedade("Física", 6, prop6)

        self.espacos[7] = EspacoCarta("Sorte", 7, "Sorte")

        prop8 = TituloPropriedade("Pedagogia", 100, "Azul Claro", 6, [6, 30, 90, 270, 400, 550], 50)
        self.espacos[8] = EspacoPropriedade("Pedagogia", 8, prop8)

        prop9 = TituloPropriedade("História", 120, "Azul Claro", 8, [8, 40, 100, 300, 450, 600], 50)
        self.espacos[9] = EspacoPropriedade("História", 9, prop9)

        self.espacos[10] = EspacoCadeia()

        prop11 = TituloPropriedade("Química", 140, "Rosa", 10, [10, 50, 150, 450, 625, 750], 100)
        self.espacos[11] = EspacoPropriedade("Química", 11, prop11)

        comp12 = TituloCompanhia("Centro de Artes UFF", 150)
        self.espacos[12] = EspacoPropriedade("Centro de Artes UFF", 12, comp12)

        prop13 = TituloPropriedade("Engenharia Civil", 140, "Rosa", 10, [10, 50, 150, 450, 625, 750], 100)
        self.espacos[13] = EspacoPropriedade("Engenharia Civil", 13, prop13)

        prop14 = TituloPropriedade("Nutrição", 160, "Rosa", 12, [12, 60, 180, 500, 700, 900], 100)
        self.espacos[14] = EspacoPropriedade("Nutrição", 14, prop14)

        estacao15 = TituloEstacao("Bandejão Veterinária", 200)
        self.espacos[15] = EspacoPropriedade("Bandejão Veterinária", 15, estacao15)

        prop16 = TituloPropriedade("Ciências Contábeis", 180, "Laranja", 14, [14, 70, 200, 550, 750, 950], 100)
        self.espacos[16] = EspacoPropriedade("Ciências Contábeis", 16, prop16)

        self.espacos[17] = EspacoCarta("Cofre", 17, "Cofre")

        prop18 = TituloPropriedade("Direito", 180, "Laranja", 14, [14, 70, 200, 550, 750, 950], 100)
        self.espacos[18] = EspacoPropriedade("Direito", 18, prop18)

        prop19 = TituloPropriedade("Enfermagem", 200, "Laranja", 16, [16, 80, 220, 600, 800, 1000], 100)
        self.espacos[19] = EspacoPropriedade("Enfermagem", 19, prop19)

        self.espacos[20] = EspacoEstacionamentoGratuito()

        prop21 = TituloPropriedade("Ciências Econômicas", 220, "Vermelho", 18, [18, 90, 250, 700, 875, 1050], 150)
        self.espacos[21] = EspacoPropriedade("Ciências Econômicas", 21, prop21)

        self.espacos[22] = EspacoCarta("Sorte", 22, "Sorte")

        prop23 = TituloPropriedade("Biomedicina", 220, "Vermelho", 18, [18, 90, 250, 700, 875, 1050], 150)
        self.espacos[23] = EspacoPropriedade("Biomedicina", 23, prop23)

        prop24 = TituloPropriedade("Psicologia", 240, "Vermelho", 20, [20, 100, 300, 750, 925, 1100], 150)
        self.espacos[24] = EspacoPropriedade("Psicologia", 24, prop24)

        estacao25 = TituloEstacao("Bandejão Reitoria", 200)
        self.espacos[25] = EspacoPropriedade("Bandejão Reitoria", 25, estacao25)

        prop26 = TituloPropriedade("Engenharia Elétrica", 260, "Amarelo", 22, [22, 110, 330, 800, 975, 1150], 150)
        self.espacos[26] = EspacoPropriedade("Engenharia Elétrica", 26, prop26)

        prop27 = TituloPropriedade("Engenharia de Produção", 260, "Amarelo", 22, [22, 110, 330, 800, 975, 1150], 150)
        self.espacos[27] = EspacoPropriedade("Engenharia de Produção", 27, prop27)

        comp28 = TituloCompanhia("MAC", 150)
        self.espacos[28] = EspacoPropriedade("MAC", 28, comp28)

        prop29 = TituloPropriedade("Arquitetura e Urbanismo", 280, "Amarelo", 24, [24, 120, 360, 850, 1025, 1200], 150)
        self.espacos[29] = EspacoPropriedade("Arquitetura e Urbanismo", 29, prop29)

        self.espacos[30] = EspacoVaParaCadeia()

        prop31 = TituloPropriedade("Cinema e Audiovisual", 300, "Verde", 26, [26, 130, 390, 900, 1100, 1275], 200)
        self.espacos[31] = EspacoPropriedade("Cinema e Audiovisual", 31, prop31)

        prop32 = TituloPropriedade("Engenharia Mecânica", 300, "Verde", 26, [26, 130, 390, 900, 1100, 1275], 200)
        self.espacos[32] = EspacoPropriedade("Engenharia Mecânica", 32, prop32)

        self.espacos[33] = EspacoCarta("Cofre", 33, "Cofre")

        prop34 = TituloPropriedade("Odontologia", 320, "Verde", 28, [28, 150, 450, 1000, 1200, 1400], 200)
        self.espacos[34] = EspacoPropriedade("Odontologia", 34, prop34)

        estacao35 = TituloEstacao("Bandejão Praia Vermelha", 200)
        self.espacos[35] = EspacoPropriedade("Bandejão Praia Vermelha", 35, estacao35)

        self.espacos[36] = EspacoCarta("Sorte", 36, "Sorte")

        prop37 = TituloPropriedade("Ciência da Computação", 350, "Azul Escuro", 35, [35, 175, 500, 1100, 1300, 1500], 200)
        self.espacos[37] = EspacoPropriedade("Ciência da Computação", 37, prop37)

        self.espacos[38] = EspacoImposto("Pedágio da Ponte", 38, 200)

        prop39 = TituloPropriedade("Medicina", 400, "Azul Escuro", 50, [50, 200, 600, 1400, 1700, 2000], 200)
        self.espacos[39] = EspacoPropriedade("Medicina", 39, prop39)

    def getEspaco(self, posicao: int) -> Optional[Espaco]:
        """
        Retorna o espaço em uma posição específica

        espera:
            posicao: int - posição no tabuleiro (0-39)
        retorna:
            Espaco - espaço na posição ou None se inválida
        """
        if 0 <= posicao < 40:
            return self.espacos[posicao]
        return None

    def getPropriedades(self) -> List:
        """
        Retorna lista de todos os espaços que são propriedades

        espera:
            nenhum parâmetro
        retorna:
            List[EspacoPropriedade] - propriedades do tabuleiro
        """
        return [e for e in self.espacos if isinstance(e, EspacoPropriedade)]

    def executarAcaoEspaco(self, posicao: int, jogador, jogo) -> None:
        """
        Executa a ação do espaço onde o jogador está

        espera:
            posicao: int - posição atual
            jogador: Jogador - jogador que caiu no espaço
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        espaco = self.getEspaco(posicao)
        if espaco:
            espaco.acao(jogador, jogo)

    def getTodosEspacos(self) -> List[Espaco]:
        """
        Retorna todos os espaços do tabuleiro

        espera:
            nenhum parâmetro
        retorna:
            List[Espaco] - lista com os 40 espaços
        """
        return self.espacos.copy()

    def _inicializar_baralhos(self) -> None:
        """
        Inicializa os baralhos de cartas Sorte e Cofre

        espera:
            nenhum parâmetro
        retorna:
            None
        """

        self.baralho_sorte = BaralhoCartas(TipoCarta.SORTE)
        self.baralho_cofre = BaralhoCartas(TipoCarta.COFRE)

        carta_sair_sorte = CartaSairCadeia(TipoCarta.SORTE)
        self.baralho_sorte.adicionarCarta(carta_sair_sorte)

        carta_sair_cofre = CartaSairCadeia(TipoCarta.COFRE)
        self.baralho_cofre.adicionarCarta(carta_sair_cofre)

        self.baralho_sorte.embaralhar()
        self.baralho_cofre.embaralhar()

    def getBaralho(self, tipo: str) -> Optional[BaralhoCartas]:
        """
        Retorna o baralho correspondente ao tipo especificado

        espera:
            tipo: str - tipo do baralho ("Sorte" ou "Cofre")
        retorna:
            BaralhoCartas - baralho correspondente ou None se tipo inválido
        """
        if tipo == "Sorte":
            return self.baralho_sorte
        elif tipo == "Cofre":
            return self.baralho_cofre
        return None

    def inicializar_cartas_completas(self, jogo) -> None:
        """
        Inicializa os baralhos com todas as cartas do jogo

        espera:
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        self.baralho_sorte = BaralhoCartas(TipoCarta.SORTE)
        self.baralho_cofre = BaralhoCartas(TipoCarta.COFRE)

        cartas_sorte = criar_cartas_sorte(jogo)
        for carta in cartas_sorte:
            self.baralho_sorte.adicionarCarta(carta)

        cartas_cofre = criar_cartas_cofre(jogo)
        for carta in cartas_cofre:
            self.baralho_cofre.adicionarCarta(carta)

        self.baralho_sorte.embaralhar()
        self.baralho_cofre.embaralhar()