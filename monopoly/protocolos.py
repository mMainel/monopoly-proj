from __future__ import annotations

from abc import abstractmethod
from typing import Iterable, Protocol, runtime_checkable


@runtime_checkable
class CartaSairCadeia(Protocol):
    """Contrato para cartas de sair da cadeia."""

    def usar(self, jogador: "Jogador") -> None:
        """Executa os efeitos da carta quando utilizada."""


@runtime_checkable
class Titulo(Protocol):
    """Contrato básico de um título negociável do jogo."""

    nome: str

    @property
    @abstractmethod
    def proprietario(self) -> "Jogador | None":
        """Retorna o proprietário atual do título."""

    @abstractmethod
    def pode_ser_comprado_por(self, jogador: "Jogador") -> bool:
        """Indica se o título pode ser adquirido pelo jogador informado."""

    @abstractmethod
    def registrar_compra(self, jogador: "Jogador") -> None:
        """Atualiza o título após a compra ser realizada."""

    @abstractmethod
    def esta_hipotecado(self) -> bool:
        """Retorna se o título está atualmente hipotecado."""


@runtime_checkable
class TituloPropriedade(Titulo, Protocol):
    """Contrato adicional para títulos de propriedades."""

    @abstractmethod
    def calcular_aluguel(self, jogador: "Jogador") -> int:
        """Calcula o valor de aluguel devido pelo jogador informado."""


@runtime_checkable
class TituloCompanhia(Titulo, Protocol):
    """Contrato adicional para títulos de companhias/utilidades."""

    multiplicador_base: int

    @abstractmethod
    def calcular_aluguel(self, multiplicador_dados: int) -> int:
        """Calcula o valor de aluguel baseado no resultado dos dados."""


class BancoInterface(Protocol):
    """Operações do banco utilizadas pelo jogador."""

    def debitar(self, jogador: "Jogador", valor: int) -> None:
        """Remove fundos da conta do jogador."""

    def creditar(self, jogador: "Jogador", valor: int) -> None:
        """Adiciona fundos à conta do jogador."""

    def obter_saldo(self, jogador: "Jogador") -> int:
        """Consulta o saldo disponível do jogador."""

    def transferir(self, pagador: "Jogador", recebedor: "Jogador", valor: int) -> None:
        """Realiza transferência entre jogadores."""

    def vender_titulo(self, jogador: "Jogador", titulo: Titulo, valor: int) -> None:
        """Processa a venda de um título para o jogador."""

    def hipotecar(self, jogador: "Jogador", titulo: Titulo, valor: int) -> None:
        """Processa a hipoteca de um título pertencente ao jogador."""

    def resgatar_hipoteca(self, jogador: "Jogador", titulo: Titulo, valor: int) -> None:
        """Processa o resgate de hipoteca de um título."""

    def iniciar_leilao(self, titulo: Titulo, participantes: Iterable["Jogador"]) -> None:
        """Inicia um leilão do título para os participantes fornecidos."""


class LeilaoInterface(Protocol):
    """Interface simplificada para leilões."""

    def registrar_participante(self, jogador: "Jogador") -> None:
        """Adiciona um jogador à lista de participantes."""

    def ofertar_lance(self, jogador: "Jogador", valor: int) -> bool:
        """Tenta registrar um lance e retorna se foi aceito."""


class TabuleiroInterface(Protocol):
    """Interface mínima para integração com o tabuleiro."""

    def mover_jogador(self, jogador: "Jogador", passos: int) -> int:
        """Move o jogador pelo número de passos e retorna a nova posição."""

    def posicionar_jogador(self, jogador: "Jogador", posicao: int) -> None:
        """Posiciona o jogador em uma casa específica."""
