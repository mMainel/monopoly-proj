from abc import ABC, abstractmethod
from enum import Enum

class TipoCarta(Enum):
    """
    Tipos de carta disponíveis no jogo
    """
    SORTE = "SORTE"
    REVES = "REVES"

class Carta(ABC):
    """
    Classe abstrata que representa uma carta do jogo
    Cartas executam ações específicas quando sorteadas
    """

    def __init__(self, descricao: str):
        self.descricao = descricao

    @abstractmethod
    def executar(self, jogador) -> None:
        """
        Executa a ação da carta sobre o jogador

        espera:
            jogador: Jogador - jogador que sorteou a carta
        retorna:
            None
        """
        pass

    def getDescricao(self) -> str:
        """
        Retorna a descrição da carta

        espera:
            nenhum parâmetro
        retorna:
            str - texto descritivo da carta
        """
        return self.descricao

class CartaSorte(Carta):
    """
    Carta do tipo Sorte
    """

    def __init__(self, descricao: str, acao_callback=None):
        super().__init__(descricao)
        self.acao_callback = acao_callback

    def executar(self, jogador) -> None:
        """
        Executa a ação de sorte para o jogador

        espera:
            jogador: Jogador - jogador que sorteou a carta
        retorna:
            None
        """
        if self.acao_callback:
            self.acao_callback(jogador)

class CartaReves(Carta):
    """
    Carta do tipo Revés
    """

    def __init__(self, descricao: str, acao_callback=None):
        super().__init__(descricao)
        self.acao_callback = acao_callback

    def executar(self, jogador) -> None:
        """
        Executa a ação de revés para o jogador

        espera:
            jogador: Jogador - jogador que sorteou a carta
        retorna:
            None
        """
        if self.acao_callback:
            self.acao_callback(jogador)

class CartaSairCadeia(Carta):
    """
    Carta especial que permite sair da cadeia
    """

    def __init__(self, tipo: TipoCarta):
        descricao = "Você saiu da cadeia. Você pode guardar esta carta ou usá-la."
        super().__init__(descricao)
        self.tipo = tipo

    def executar(self, jogador) -> None:
        """
        Adiciona a carta ao inventário do jogador

        espera:
            jogador: Jogador - jogador que sorteou a carta
        retorna:
            None
        """
        jogador.adicionarCartaSairCadeia()

    def getTipo(self) -> TipoCarta:
        """
        Retorna o tipo da carta (Sorte ou Revés)

        espera:
            nenhum parâmetro
        retorna:
            TipoCarta - tipo da carta
        """
        return self.tipo