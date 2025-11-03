import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.tituloPropriedade import TituloPropriedade
from modules.jogador import Jogador
from modules.peca import Peca

def test_propriedade_inicializacao():
    """Testa inicialização de Propriedade"""
    print("-----")
    print("Testando: Propriedade inicializacao")
    print("-----")

    prop = TituloPropriedade(
        nome="Medicina",
        preco=400,
        cor="Azul Escuro",
        aluguel_base=50,
        alugueis=[50, 200, 600, 1400, 1700, 2000],
        custo_casa=200
    )

    assert prop.getNome() == "Medicina"
    assert prop.getPreco() == 400
    assert prop.getCor() == "Azul Escuro"
    assert prop.getAluguelBase() == 50
    assert prop.getCustoCasa() == 200
    assert prop.getNumCasas() == 0
    assert prop.temHotel() == False
    assert prop.estaDisponivel() == True
    print("Propriedade inicializada corretamente")

def test_propriedade_compra():
    """Testa compra de propriedade"""
    print("-----")
    print("Testando: Propriedade compra")
    print("-----")

    jogador = Jogador("Emanuel", Peca.CACHORRO)
    prop = TituloPropriedade("Artes", 300, "Verde", 30, [30, 150, 450, 1000, 1200, 1400], 200)

    prop.proprietario = jogador
    jogador.pagarAoBanco(300)
    jogador.adicionarPropriedade(prop)

    assert prop.getProprietario() == jogador
    assert jogador.getSaldo() == 1200
    assert prop in jogador.getPropriedades()
    print("Compra realizada corretamente")

def test_propriedade_compra_sem_saldo():
    """Testa compra sem saldo suficiente"""
    print("-----")
    print("Testando: Propriedade compra sem saldo")
    print("-----")

    jogador = Jogador("Lucas", Peca.SAPATO)
    jogador.pagarAoBanco(1400)

    prop = TituloPropriedade("Biologia", 300, "Amarelo", 30, [30, 150, 450, 1000, 1200, 1400], 200)

    assert jogador.getSaldo() < prop.getPreco()
    assert prop.getProprietario() is None
    print("Compra sem saldo rejeitada corretamente")

def test_propriedade_aluguel_sem_casas():
    """Testa cálculo de aluguel sem casas"""
    print("-----")
    print("Testando: Propriedade aluguel sem casas")
    print("-----")

    jogador = Jogador("Lorhan", Peca.CARRO_CORRIDA)
    prop = TituloPropriedade("Economia", 350, "Vermelho", 35, [35, 175, 500, 1100, 1300, 1500], 150)

    prop.proprietario = jogador
    aluguel = prop.calcularAluguel()

    assert aluguel == 35
    print("Aluguel sem casas calculado corretamente")

def test_propriedade_aluguel_com_monopolio():
    """Testa aluguel dobrado com monopolio"""
    print("-----")
    print("Testando: Propriedade aluguel com monopolio")
    print("-----")

    jogador = Jogador("Emanuel", Peca.CHAPEU)
    jogador.possuiMonopolio = lambda cor: True

    prop = TituloPropriedade("Teatro", 280, "Rosa", 25, [25, 125, 375, 875, 1050, 1250], 150)
    prop.proprietario = jogador

    aluguel = prop.calcularAluguel()

    assert aluguel == 50
    print("Aluguel com monopolio calculado corretamente")

def test_propriedade_construir_casa():
    """Testa construção de casas"""
    print("-----")
    print("Testando: Propriedade construir casa")
    print("-----")

    jogador = Jogador("Lucas", Peca.NAVIO_GUERRA)
    jogador.possuiMonopolio = lambda cor: True

    prop = TituloPropriedade("Arquitetura", 400, "Verde", 40, [40, 200, 600, 1400, 1700, 2000], 200)
    prop.proprietario = jogador

    sucesso = prop.construirCasa()

    assert sucesso == True
    assert prop.getNumCasas() == 1
    assert jogador.getSaldo() == 1300

    aluguel = prop.calcularAluguel()
    assert aluguel == 200
    print("Construção de casa funcionando")

def test_propriedade_construir_multiplas_casas():
    """Testa construção de múltiplas casas"""
    print("-----")
    print("Testando: Propriedade construir multiplas casas")
    print("-----")

    jogador = Jogador("Lorhan", Peca.DEDAL)
    jogador.possuiMonopolio = lambda cor: True

    prop = TituloPropriedade("Física", 300, "Laranja", 25, [25, 125, 375, 875, 1050, 1250], 150)
    prop.proprietario = jogador

    for i in range(3):
        prop.construirCasa()

    assert prop.getNumCasas() == 3
    assert jogador.getSaldo() == 1050
    assert prop.calcularAluguel() == 875
    print("Múltiplas casas construídas corretamente")

def test_propriedade_construir_hotel():
    """Testa construção de hotel"""
    print("-----")
    print("Testando: Propriedade construir hotel")
    print("-----")

    jogador = Jogador("Emanuel", Peca.LOCOMOTIVA)
    jogador.possuiMonopolio = lambda cor: True

    prop = TituloPropriedade("Música", 320, "Rosa", 28, [28, 150, 450, 1000, 1200, 1400], 180)
    prop.proprietario = jogador

    for _ in range(4):
        prop.construirCasa()

    sucesso = prop.construirHotel()

    assert sucesso == True
    assert prop.getNumCasas() == 0
    assert prop.temHotel() == True
    assert prop.calcularAluguel() == 1400
    print("Hotel construído corretamente")

def test_propriedade_vender_casa():
    """Testa venda de casa"""
    print("-----")
    print("Testando: Propriedade vender casa")
    print("-----")

    jogador = Jogador("Lucas", Peca.FERRO_PASSAR)
    jogador.possuiMonopolio = lambda cor: True

    prop = TituloPropriedade("Química", 260, "Laranja", 22, [22, 110, 330, 800, 975, 1150], 140)
    prop.proprietario = jogador

    prop.construirCasa()
    prop.construirCasa()

    saldo_antes = jogador.getSaldo()
    sucesso = prop.venderCasa()

    assert sucesso == True
    assert prop.getNumCasas() == 1
    assert jogador.getSaldo() == saldo_antes + 70
    print("Venda de casa funcionando")

def test_propriedade_vender_hotel():
    """Testa venda de hotel"""
    print("-----")
    print("Testando: Propriedade vender hotel")
    print("-----")

    jogador = Jogador("Lorhan", Peca.COWBOY)
    jogador.possuiMonopolio = lambda cor: True

    prop = TituloPropriedade("Enfermagem", 350, "Verde", 35, [35, 175, 500, 1100, 1300, 1500], 200)
    prop.proprietario = jogador

    for _ in range(4):
        prop.construirCasa()
    prop.construirHotel()

    saldo_antes = jogador.getSaldo()
    sucesso = prop.venderHotel()

    assert sucesso == True
    assert prop.temHotel() == False
    assert prop.getNumCasas() == 4
    assert jogador.getSaldo() == saldo_antes + 100
    print("Venda de hotel funcionando")

def test_propriedade_hipotecar():
    """Testa hipoteca de propriedade"""
    print("-----")
    print("Testando: Propriedade hipotecar")
    print("-----")

    jogador = Jogador("Emanuel", Peca.SACO_DINHEIRO)
    prop = TituloPropriedade("Pedagogia", 220, "Rosa", 18, [18, 90, 250, 700, 875, 1050], 150)

    prop.proprietario = jogador
    jogador.adicionarPropriedade(prop)
    saldo_antes = jogador.getSaldo()

    valor = prop.hipotecar()

    assert valor == 110
    assert prop.estaHipotecada() == True
    assert jogador.getSaldo() == saldo_antes + 110
    assert prop.calcularAluguel() == 0
    print("Hipoteca funcionando corretamente")

def test_propriedade_nao_hipotecar_com_casas():
    """Testa que não pode hipotecar com construções"""
    print("-----")
    print("Testando: Propriedade nao hipotecar com casas")
    print("-----")

    jogador = Jogador("Lorhan", Peca.CACHORRO)
    jogador.possuiMonopolio = lambda cor: True

    prop = TituloPropriedade("Matemática", 280, "Vermelho", 24, [24, 120, 360, 850, 1025, 1200], 150)
    prop.proprietario = jogador
    prop.construirCasa()

    valor = prop.hipotecar()

    assert valor == 0
    assert prop.estaHipotecada() == False
    print("Hipoteca com casas corretamente bloqueada")

def test_propriedade_transferir():
    """Testa transferência de propriedade"""
    print("-----")
    print("Testando: Propriedade transferir")
    print("-----")

    jogador1 = Jogador("Emanuel", Peca.SAPATO)
    jogador2 = Jogador("Lucas", Peca.CACHORRO)

    prop = TituloPropriedade("Letras", 180, "Marrom", 10, [10, 50, 150, 450, 625, 750], 50)
    prop.proprietario = jogador1
    jogador1.adicionarPropriedade(prop)

    prop.transferirPropriedade(jogador2)

    assert prop.getProprietario() == jogador2
    assert prop in jogador2.getPropriedades()
    assert prop not in jogador1.getPropriedades()
    print("Transferência funcionando corretamente")

test_propriedade_inicializacao()
test_propriedade_compra()
test_propriedade_compra_sem_saldo()
test_propriedade_aluguel_sem_casas()
test_propriedade_aluguel_com_monopolio()
test_propriedade_construir_casa()
test_propriedade_construir_multiplas_casas()
test_propriedade_construir_hotel()
test_propriedade_vender_casa()
test_propriedade_vender_hotel()
test_propriedade_hipotecar()
test_propriedade_nao_hipotecar_com_casas()
test_propriedade_transferir()