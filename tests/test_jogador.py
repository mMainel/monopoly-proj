from __future__ import annotations

from typing import Iterable

import pytest

from monopoly.jogador import Jogador
from monopoly.peca import Peca
from monopoly.protocolos import (
    BancoInterface,
    CartaSairCadeia,
    LeilaoInterface,
    TabuleiroInterface,
    Titulo,
    TituloCompanhia,
    TituloPropriedade,
)


class BancoFalso(BancoInterface):
    def __init__(self) -> None:
        self.saldos: dict[Jogador, int] = {}
        self.debitos: list[tuple[Jogador, int]] = []
        self.creditos: list[tuple[Jogador, int]] = []
        self.transferencias: list[tuple[Jogador, Jogador, int]] = []
        self.vendas: list[tuple[Jogador, Titulo, int]] = []
        self.hipotecas: list[tuple[Jogador, Titulo, int]] = []
        self.resgates: list[tuple[Jogador, Titulo, int]] = []
        self.leiloes: list[tuple[Titulo, tuple[Jogador, ...]]] = []

    def _garantir_conta(self, jogador: Jogador) -> None:
        self.saldos.setdefault(jogador, 0)

    def debitar(self, jogador: Jogador, valor: int) -> None:
        self._garantir_conta(jogador)
        if self.saldos[jogador] < valor:
            raise ValueError("saldo insuficiente")
        self.saldos[jogador] -= valor
        self.debitos.append((jogador, valor))

    def creditar(self, jogador: Jogador, valor: int) -> None:
        self._garantir_conta(jogador)
        self.saldos[jogador] += valor
        self.creditos.append((jogador, valor))

    def obter_saldo(self, jogador: Jogador) -> int:
        self._garantir_conta(jogador)
        return self.saldos[jogador]

    def transferir(self, pagador: Jogador, recebedor: Jogador, valor: int) -> None:
        self.debitar(pagador, valor)
        self.creditar(recebedor, valor)
        self.transferencias.append((pagador, recebedor, valor))

    def vender_titulo(self, jogador: Jogador, titulo: Titulo, valor: int) -> None:
        self.debitar(jogador, valor)
        self.vendas.append((jogador, titulo, valor))

    def hipotecar(self, jogador: Jogador, titulo: Titulo, valor: int) -> None:
        self.creditar(jogador, valor)
        if isinstance(titulo, TituloBaseFalso):
            titulo._hipotecado = True  # noqa: SLF001 - atributo interno controlado pelo teste
        self.hipotecas.append((jogador, titulo, valor))

    def resgatar_hipoteca(self, jogador: Jogador, titulo: Titulo, valor: int) -> None:
        self.debitar(jogador, valor)
        if isinstance(titulo, TituloBaseFalso):
            titulo._hipotecado = False  # noqa: SLF001 - atributo interno controlado pelo teste
        self.resgates.append((jogador, titulo, valor))

    def iniciar_leilao(self, titulo: Titulo, participantes: Iterable[Jogador]) -> None:
        self.leiloes.append((titulo, tuple(participantes)))


class TituloBaseFalso:
    def __init__(self, nome: str = "Título") -> None:
        self.nome = nome
        self._proprietario: Jogador | None = None
        self._hipotecado = False

    @property
    def proprietario(self) -> Jogador | None:
        return self._proprietario

    def pode_ser_comprado_por(self, jogador: Jogador) -> bool:
        return self._proprietario is None or self._proprietario is jogador

    def registrar_compra(self, jogador: Jogador) -> None:
        self._proprietario = jogador

    def esta_hipotecado(self) -> bool:
        return self._hipotecado


class TituloPropriedadeFalso(TituloBaseFalso, TituloPropriedade):
    def __init__(self, aluguel: int = 50, nome: str = "Propriedade") -> None:
        super().__init__(nome)
        self.aluguel = aluguel
        self.jogadores_consultados: list[Jogador] = []

    def calcular_aluguel(self, jogador: Jogador) -> int:
        self.jogadores_consultados.append(jogador)
        return self.aluguel


class TituloCompanhiaFalso(TituloBaseFalso, TituloCompanhia):
    def __init__(self, fator: int = 10, nome: str = "Companhia") -> None:
        super().__init__(nome)
        self.multiplicador_base = fator
        self.multiplicadores: list[int] = []

    def calcular_aluguel(self, multiplicador_dados: int) -> int:
        self.multiplicadores.append(multiplicador_dados)
        return self.multiplicador_base * multiplicador_dados


class CartaSairCadeiaFalsa(CartaSairCadeia):
    def __init__(self) -> None:
        self.usos: list[Jogador] = []

    def usar(self, jogador: Jogador) -> None:
        self.usos.append(jogador)


class LeilaoFalso(LeilaoInterface):
    def __init__(self) -> None:
        self.participantes: list[Jogador] = []
        self.lances: list[tuple[Jogador, int]] = []
        self.maior_lance: int = 0

    def registrar_participante(self, jogador: Jogador) -> None:
        if jogador not in self.participantes:
            self.participantes.append(jogador)

    def ofertar_lance(self, jogador: Jogador, valor: int) -> bool:
        self.lances.append((jogador, valor))
        if valor > self.maior_lance:
            self.maior_lance = valor
            return True
        return False


class TabuleiroFalso(TabuleiroInterface):
    def __init__(self) -> None:
        self.movimentos: list[tuple[Jogador, int, int]] = []
        self.posicionamentos: list[tuple[Jogador, int]] = []
        self.posicoes: dict[Jogador, int] = {}

    def mover_jogador(self, jogador: Jogador, passos: int) -> int:
        posicao_atual = self.posicoes.get(jogador, jogador.peca.posicao)
        nova_posicao = posicao_atual + passos
        self.posicoes[jogador] = nova_posicao
        self.movimentos.append((jogador, passos, nova_posicao))
        jogador.peca.posicionar(nova_posicao)
        return nova_posicao

    def posicionar_jogador(self, jogador: Jogador, posicao: int) -> None:
        self.posicoes[jogador] = posicao
        self.posicionamentos.append((jogador, posicao))
        jogador.peca.posicionar(posicao)


def criar_jogador(nome: str = "Lucas", saldo: int = 0) -> tuple[Jogador, BancoFalso]:
    banco = BancoFalso()
    jogador = Jogador(nome=nome, peca=Peca(f"{nome}-peca"), banco=banco, saldo_inicial=saldo)
    return jogador, banco


def test_credita_saldo_inicial() -> None:
    jogador, banco = criar_jogador(saldo=200)
    assert banco.obter_saldo(jogador) == 200
    assert banco.creditos == [(jogador, 200)]


def test_pagamento_ao_banco_debita_saldo() -> None:
    jogador, banco = criar_jogador(saldo=300)
    jogador.pagar_ao_banco(150)
    assert banco.obter_saldo(jogador) == 150
    assert banco.debitos == [(jogador, 150)]


def test_transferencia_para_outro_jogador() -> None:
    pagador, banco = criar_jogador(saldo=300)
    recebedor = Jogador(nome="Maria", peca=Peca("maria"), banco=banco, saldo_inicial=100)
    pagador.pagar_a_jogador(recebedor, 120)

    assert banco.obter_saldo(pagador) == 180
    assert banco.obter_saldo(recebedor) == 220
    assert banco.transferencias == [(pagador, recebedor, 120)]


def test_nao_permite_transferir_para_si_mesmo() -> None:
    jogador, _ = criar_jogador(saldo=100)
    with pytest.raises(ValueError):
        jogador.pagar_a_jogador(jogador, 10)


def test_compra_titulo_propriedade_sucesso() -> None:
    jogador, banco = criar_jogador(saldo=400)
    titulo = TituloPropriedadeFalso(aluguel=25)

    executado = jogador.comprar_titulo(titulo, valor=300)
    assert executado is True
    assert titulo in jogador.titulos
    assert titulo.proprietario is jogador
    assert banco.obter_saldo(jogador) == 100
    assert banco.vendas == [(jogador, titulo, 300)]


def test_compra_titulo_falha_quando_indisponivel() -> None:
    jogador, banco = criar_jogador(saldo=400)
    outro = Jogador(nome="Ana", peca=Peca("ana"), banco=banco, saldo_inicial=0)
    titulo = TituloPropriedadeFalso()
    titulo.registrar_compra(outro)

    executado = jogador.comprar_titulo(titulo, valor=200)
    assert executado is False
    assert banco.vendas == []


def test_pagamento_aluguel_propriedade() -> None:
    pagador, banco = criar_jogador(saldo=300)
    proprietario = Jogador(nome="Joao", peca=Peca("joao"), banco=banco, saldo_inicial=50)
    titulo = TituloPropriedadeFalso(aluguel=40)
    titulo.registrar_compra(proprietario)

    valor_pago = pagador.pagar_aluguel(titulo)
    assert valor_pago == 40
    assert banco.transferencias[-1] == (pagador, proprietario, 40)
    assert pagador in titulo.jogadores_consultados


def test_pagamento_aluguel_companhia() -> None:
    pagador, banco = criar_jogador(saldo=500)
    proprietario = Jogador(nome="Duda", peca=Peca("duda"), banco=banco, saldo_inicial=100)
    titulo = TituloCompanhiaFalso(fator=12)
    titulo.registrar_compra(proprietario)

    valor_pago = pagador.pagar_aluguel(titulo, multiplicador_companhia=4)
    assert valor_pago == 48
    assert banco.transferencias[-1] == (pagador, proprietario, 48)
    assert titulo.multiplicadores == [4]


def test_exige_multiplicador_para_companhia() -> None:
    pagador, banco = criar_jogador(saldo=200)
    proprietario = Jogador(nome="Rival", peca=Peca("rival"), banco=banco, saldo_inicial=0)
    titulo = TituloCompanhiaFalso()
    titulo.registrar_compra(proprietario)

    with pytest.raises(ValueError):
        pagador.pagar_aluguel(titulo)


def test_hipoteca_e_resgate_de_titulo() -> None:
    jogador, banco = criar_jogador(saldo=200)
    titulo = TituloPropriedadeFalso()
    jogador.comprar_titulo(titulo, valor=50)

    sucesso_hipoteca = jogador.hipotecar_titulo(titulo, valor=75)
    assert sucesso_hipoteca is True
    assert banco.hipotecas == [(jogador, titulo, 75)]
    assert titulo.esta_hipotecado() is True

    sucesso_resgate = jogador.resgatar_hipoteca(titulo, valor=80)
    assert sucesso_resgate is True
    assert banco.resgates == [(jogador, titulo, 80)]
    assert titulo.esta_hipotecado() is False


def test_nao_hipoteca_titulo_caso_nao_possua() -> None:
    jogador, _ = criar_jogador(saldo=200)
    titulo = TituloPropriedadeFalso()
    assert jogador.hipotecar_titulo(titulo, valor=50) is False


def test_cartas_de_sair_da_cadeia() -> None:
    jogador, _ = criar_jogador()
    carta = CartaSairCadeiaFalsa()
    jogador.registrar_carta_sair_cadeia(carta)

    jogador.entrar_na_cadeia(posicao=10)
    assert jogador.esta_preso is True
    assert jogador.possui_carta_sair_cadeia() is True

    usado = jogador.usar_carta_sair_cadeia()
    assert usado is True
    assert jogador.esta_preso is False
    assert carta.usos == [jogador]


def test_mover_com_tabuleiro_externo() -> None:
    jogador, _ = criar_jogador()
    tabuleiro = TabuleiroFalso()
    nova_posicao = jogador.mover(7, tabuleiro=tabuleiro)

    assert nova_posicao == 7
    assert tabuleiro.movimentos == [(jogador, 7, 7)]
    assert jogador.peca.posicao == 7


def test_mover_diretamente_sem_tabuleiro() -> None:
    jogador, _ = criar_jogador()
    nova_posicao = jogador.mover(12, tamanho_tabuleiro=40)
    assert nova_posicao == 12
    assert jogador.peca.posicao == 12


def test_jogador_preso_nao_pode_mover() -> None:
    jogador, _ = criar_jogador()
    jogador.entrar_na_cadeia(posicao=10)
    with pytest.raises(RuntimeError):
        jogador.mover(5)


def test_registro_de_turnos_na_cadeia() -> None:
    jogador, _ = criar_jogador()
    jogador.entrar_na_cadeia(posicao=10)
    jogador.registrar_turno_preso()
    jogador.registrar_turno_preso()
    assert jogador.turnos_preso == 2

    jogador.liberar_da_cadeia()
    assert jogador.turnos_preso == 0
    assert jogador.esta_preso is False


def test_pagar_fianca_libera_jogador() -> None:
    jogador, banco = criar_jogador(saldo=200)
    jogador.entrar_na_cadeia(posicao=10)
    jogador.pagar_fianca(50)
    assert jogador.esta_preso is False
    assert banco.obter_saldo(jogador) == 150


def test_participacao_em_leilao() -> None:
    jogador, _ = criar_jogador(saldo=300)
    leilao = LeilaoFalso()

    aceito = jogador.participar_de_leilao(leilao, lance=150)
    assert aceito is True
    assert leilao.participantes == [jogador]
    assert leilao.lances == [(jogador, 150)]


def test_requisicao_de_leilao_ao_banco() -> None:
    jogador, banco = criar_jogador()
    titulo = TituloPropriedadeFalso()
    outros = [Jogador(nome="A", peca=Peca("a"), banco=banco), Jogador(nome="B", peca=Peca("b"), banco=banco)]

    jogador.propor_participantes_para_leilao(titulo, outros)
    assert banco.leiloes == [(titulo, tuple(outros))]


def test_remover_titulo_da_posse() -> None:
    jogador, _ = criar_jogador(saldo=300)
    titulo = TituloPropriedadeFalso()
    jogador.comprar_titulo(titulo, valor=100)

    assert jogador.remover_titulo(titulo) is True
    assert titulo not in jogador.titulos

    assert jogador.remover_titulo(titulo) is False
