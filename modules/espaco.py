from abc import ABC, abstractmethod
from typing import Optional

class Espaco(ABC):
    """
    Classe abstrata que representa um espaço no tabuleiro
    Cada casa do tabuleiro é um tipo específico de espaço
    """

    def __init__(self, nome: str, posicao: int):
        self.nome = nome
        self.posicao = posicao

    @abstractmethod
    def acao(self, jogador, jogo) -> None:
        """
        Executa a ação quando um jogador cai neste espaço

        espera:
            jogador: Jogador - jogador que caiu no espaço
            jogo: Jogo - instância do jogo para acessar regras e banco
        retorna:
            None
        """
        pass

    def getNome(self) -> str:
        """
        Retorna o nome do espaço

        espera:
            nenhum parâmetro
        retorna:
            str - nome do espaço
        """
        return self.nome

    def getPosicao(self) -> int:
        """
        Retorna a posição do espaço no tabuleiro

        espera:
            nenhum parâmetro
        retorna:
            int - posição (0-39)
        """
        return self.posicao

class EspacoPropriedade(Espaco):
    """
    Espaço que contém uma propriedade comprável
    """

    def __init__(self, nome: str, posicao: int, titulo):
        super().__init__(nome, posicao)
        self.titulo = titulo

    def acao(self, jogador, jogo) -> None:
        """
        Verifica se propriedade tem dono e cobra aluguel ou oferece compra

        espera:
            jogador: Jogador - jogador que caiu aqui
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        if self.titulo.getProprietario() is None:
            jogo.propriedade_disponivel_compra = self.titulo
        elif self.titulo.getProprietario() != jogador:
            jogo.tratarPagamentoAluguel(jogador, self.titulo)

    def getTitulo(self):
        """
        Retorna o título associado a este espaço

        espera:
            nenhum parâmetro
        retorna:
            Titulo - título da propriedade
        """
        return self.titulo

class EspacoInicio(Espaco):
    """
    Espaço GO - início do tabuleiro (posição 0)
    """

    def __init__(self):
        super().__init__("GO", 0)

    def acao(self, jogador, jogo) -> None:
        """
        Não faz nada, pois o salário é pago ao passar pelo GO

        espera:
            jogador: Jogador - jogador
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        pass

class EspacoCadeia(Espaco):
    """
    Espaço da cadeia (posição 10) - apenas visitando
    """

    def __init__(self):
        super().__init__("Cadeia (Visitando)", 10)

    def acao(self, jogador, jogo) -> None:
        """
        Apenas visitando, não acontece nada

        espera:
            jogador: Jogador - jogador
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        pass

class EspacoVaParaCadeia(Espaco):
    """
    Espaço que envia o jogador para a cadeia (posição 30)
    """

    def __init__(self):
        super().__init__("Vá para Cadeia", 30)

    def acao(self, jogador, jogo) -> None:
        """
        Envia o jogador para a cadeia

        espera:
            jogador: Jogador - jogador a ser preso
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        jogador.entrarCadeia()

class EspacoEstacionamentoGratuito(Espaco):
    """
    Espaço de estacionamento gratuito (posição 20)
    """
    def __init__(self):
        super().__init__("Estacionamento Gratuito", 20)

    def acao(self, jogador, jogo) -> None:
        """
        Não faz nada - apenas descanso

        espera:
            jogador: Jogador - jogador
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        pass

class EspacoImposto(Espaco):
    """
    Espaço que cobra pedágio da ponte do jogador
    """

    def __init__(self, nome: str, posicao: int, valor: int):
        super().__init__(nome, posicao)
        self.valor = valor

    def acao(self, jogador, jogo) -> None:
        """
        Cobra pedágio da ponte do jogador

        espera:
            jogador: Jogador - jogador que deve pagar
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, self.valor, self.nome)
        else:
            jogador.pagarAoBanco(self.valor)

    def getValor(self) -> int:
        """
        Retorna o valor do pedágio da ponte

        espera:
            nenhum parâmetro
        retorna:
            int - valor do pedágio da ponte
        """
        return self.valor

class EspacoCarta(Espaco):
    """
    Espaço de carta Sorte ou Cofre
    """

    def __init__(self, nome: str, posicao: int, tipo_carta: str):
        super().__init__(nome, posicao)
        self.tipo_carta = tipo_carta

    def acao(self, jogador, jogo) -> None:
        """
        Sorteia e executa uma carta do baralho correspondente

        espera:
            jogador: Jogador - jogador
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        if hasattr(jogo, 'tabuleiro') and jogo.tabuleiro:
            baralho = jogo.tabuleiro.getBaralho(self.tipo_carta)
            if baralho and not baralho.estaVazio():
                carta = baralho.sacarCarta()
                if carta:
                    carta.executar(jogador)
                    baralho.retornarCarta(carta)

    def getTipoCarta(self) -> str:
        """
        Retorna o tipo de carta deste espaço

        espera:
            nenhum parâmetro
        retorna:
            str - tipo da carta ("Sorte" ou "Cofre")
        """
        return self.tipo_carta