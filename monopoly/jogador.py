from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .peca import Peca
from .protocolos import (
    BancoInterface,
    CartaSairCadeia,
    LeilaoInterface,
    TabuleiroInterface,
    Titulo,
    TituloCompanhia,
    TituloPropriedade,
)


@dataclass(slots=True, eq=False)
class Jogador:
    """Entidade principal que representa um jogador de Monopoly."""

    nome: str
    peca: Peca
    banco: BancoInterface
    saldo_inicial: int = 0
    _titulos: list[Titulo] = field(default_factory=list, init=False, repr=False)
    _esta_preso: bool = field(default=False, init=False, repr=False)
    _turnos_preso: int = field(default=0, init=False, repr=False)
    _cartas_sair_cadeia: list[CartaSairCadeia] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.saldo_inicial < 0:
            raise ValueError("saldo_inicial não pode ser negativo")

        if self.saldo_inicial:
            self.banco.creditar(self, self.saldo_inicial)

    @property
    def esta_preso(self) -> bool:
        """Retorna se o jogador encontra-se preso."""
        return self._esta_preso

    @property
    def turnos_preso(self) -> int:
        """Quantidade de turnos consecutivos na cadeia."""
        return self._turnos_preso

    @property
    def titulos(self) -> tuple[Titulo, ...]:
        """Lista imutável de títulos sob posse do jogador."""
        return tuple(self._titulos)

    def obter_saldo(self) -> int:
        """Consulta o saldo atual do jogador no banco."""
        return self.banco.obter_saldo(self)

    def receber_dinheiro(self, valor: int) -> None:
        """Credita dinheiro vindo do banco."""
        self._validar_valor_positivo(valor)
        self.banco.creditar(self, valor)

    def pagar_ao_banco(self, valor: int) -> None:
        """Debita dinheiro do jogador para o banco."""
        self._validar_valor_positivo(valor)
        self.banco.debitar(self, valor)

    def pagar_a_jogador(self, destinatario: "Jogador", valor: int) -> None:
        """Realiza transferência direta para outro jogador."""
        if destinatario is self:
            raise ValueError("destinatario não pode ser o próprio jogador")

        self._validar_valor_positivo(valor)
        self.banco.transferir(self, destinatario, valor)

    def comprar_titulo(self, titulo: Titulo, valor: int) -> bool:
        """
        Efetua a tentativa de compra de um título.

        Returns:
            bool: Indica se a compra foi concretizada.
        """
        self._validar_valor_positivo(valor)

        if titulo in self._titulos:
            return False

        if not titulo.pode_ser_comprado_por(self):
            return False

        self.banco.vender_titulo(self, titulo, valor)
        titulo.registrar_compra(self)
        self._titulos.append(titulo)
        return True

    def hipotecar_titulo(self, titulo: Titulo, valor: int) -> bool:
        """Hipoteca um título possuído pelo jogador."""
        self._validar_valor_positivo(valor)

        if titulo not in self._titulos:
            return False

        if titulo.esta_hipotecado():
            return False

        self.banco.hipotecar(self, titulo, valor)
        return True

    def resgatar_hipoteca(self, titulo: Titulo, valor: int) -> bool:
        """Resgata a hipoteca de um título possuído."""
        self._validar_valor_positivo(valor)

        if titulo not in self._titulos:
            return False

        if not titulo.esta_hipotecado():
            return False

        self.banco.resgatar_hipoteca(self, titulo, valor)
        return True

    def pagar_aluguel(self, titulo: Titulo, multiplicador_companhia: int | None = None) -> int:
        """
        Paga aluguel ao proprietário do título informado.

        Args:
            titulo: Título causador do pagamento.
            multiplicador_companhia: Resultado dos dados para companhias/utilidades.

        Returns:
            Valor efetivamente pago. Retorna 0 quando não há pagamento.
        """
        proprietario = titulo.proprietario
        if proprietario is None or proprietario is self:
            return 0

        valor = 0
        if hasattr(titulo, "multiplicador_base"):
            if multiplicador_companhia is None:
                raise ValueError("multiplicador_companhia é obrigatório para TituloCompanhia")
            valor = titulo.calcular_aluguel(multiplicador_companhia)
        elif isinstance(titulo, TituloPropriedade):
            valor = titulo.calcular_aluguel(self)
        else:
            raise TypeError("Tipo de título desconhecido para cálculo de aluguel")

        if valor <= 0:
            return 0

        self.banco.transferir(self, proprietario, valor)
        return valor

    def remover_titulo(self, titulo: Titulo) -> bool:
        """Remove um título da posse do jogador."""
        if titulo not in self._titulos:
            return False

        self._titulos.remove(titulo)
        return True

    def registrar_carta_sair_cadeia(self, carta: CartaSairCadeia) -> None:
        """Adiciona uma carta de sair da cadeia ao inventário."""
        self._cartas_sair_cadeia.append(carta)

    def possui_carta_sair_cadeia(self) -> bool:
        """Indica se o jogador possui uma carta de sair da cadeia."""
        return bool(self._cartas_sair_cadeia)

    def usar_carta_sair_cadeia(self) -> bool:
        """Utiliza uma carta de sair da cadeia, caso disponível."""
        if not self._cartas_sair_cadeia:
            return False

        carta = self._cartas_sair_cadeia.pop(0)
        carta.usar(self)
        self.liberar_da_cadeia()
        return True

    def entrar_na_cadeia(
        self,
        posicao: int | None = None,
        tabuleiro: TabuleiroInterface | None = None,
    ) -> None:
        """Marca o jogador como preso e reposiciona a peça."""
        self._esta_preso = True
        self._turnos_preso = 0

        if tabuleiro:
            if posicao is None:
                raise ValueError("posicao deve ser informada ao usar tabuleiro")
            tabuleiro.posicionar_jogador(self, posicao)
        elif posicao is not None:
            self.peca.posicionar(posicao)

    def registrar_turno_preso(self) -> None:
        """Incrementa a contagem de turnos que o jogador permanece preso."""
        if not self._esta_preso:
            raise RuntimeError("jogador não está preso")

        self._turnos_preso += 1

    def pagar_fianca(self, valor: int) -> None:
        """Paga uma fiança ao banco para sair da cadeia."""
        if not self._esta_preso:
            raise RuntimeError("jogador não está preso")

        self.pagar_ao_banco(valor)
        self.liberar_da_cadeia()

    def liberar_da_cadeia(self) -> None:
        """Libera o jogador da cadeia e zera a contagem."""
        self._esta_preso = False
        self._turnos_preso = 0

    def mover(self, passos: int, tabuleiro: TabuleiroInterface | None = None, tamanho_tabuleiro: int | None = None) -> int:
        """
        Move o jogador no tabuleiro, respeitando o estado de prisão.

        Returns:
            A nova posição ocupada pela peça.
        """
        if self._esta_preso:
            raise RuntimeError("jogador preso não pode se mover")

        if tabuleiro:
            return tabuleiro.mover_jogador(self, passos)

        return self.peca.mover_passos(passos, tamanho_tabuleiro)

    def participar_de_leilao(self, leilao: LeilaoInterface, lance: int) -> bool:
        """Registra a participação do jogador em um leilão com determinado lance."""
        self._validar_valor_positivo(lance)
        leilao.registrar_participante(self)
        return leilao.ofertar_lance(self, lance)

    def propor_participantes_para_leilao(
        self,
        titulo: Titulo,
        participantes: Iterable["Jogador"],
    ) -> None:
        """
        Encaminha ao banco a realização de um leilão com os participantes informados.
        """
        self.banco.iniciar_leilao(titulo, participantes)

    @staticmethod
    def _validar_valor_positivo(valor: int) -> None:
        if valor <= 0:
            raise ValueError("valor deve ser positivo")
