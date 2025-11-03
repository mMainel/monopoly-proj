import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.tituloPropriedade import TituloPropriedade
from modules.tituloCompanhia import TituloCompanhia
from modules.tituloEstacao import TituloEstacao
from modules.jogador import Jogador
from modules.peca import Peca

def test_titulo_propriedade_inicializacao():
    """Testa inicialização de TituloPropriedade"""
    print("-----")
    print("Testando: TituloPropriedade inicializacao")
    print("-----")

    prop = TituloPropriedade(
        nome="Avenida Amaral Peixoto",
        preco=400,
        cor="Azul Escuro",
        aluguel_base=50,
        alugueis=[50, 200, 600, 1400, 1700, 2000],
        custo_casa=200
    )

    assert prop.getNome() == "Avenida Amaral Peixoto"
    assert prop.getPreco() == 400
    assert prop.getCor() == "Azul Escuro"
    assert prop.getAluguelBase() == 50
    assert prop.getCustoCasa() == 200
    assert prop.getNumCasas() == 0
    assert prop.temHotel() == False
    assert prop.estaDisponivel() == True
    print("TituloPropriedade inicializado corretamente")

def test_titulo_propriedade_compra():
    """Testa compra de propriedade"""
    print("-----")
    print("Testando: TituloPropriedade compra")
    print("-----")

    jogador = Jogador("Lucas", Peca.CACHORRO)
    prop = TituloPropriedade("Ipanema", 300, "Verde", 30, [30, 150, 450, 1000, 1200, 1400], 200)

    sucesso = prop.comprar(jogador)

    assert sucesso == True
    assert prop.getProprietario() == jogador
    assert jogador.getSaldo() == 1200
    assert prop in jogador.getPropriedades()
    print("Compra realizada corretamente")

def test_titulo_propriedade_aluguel_base():
    """Testa cálculo de aluguel base"""
    print("-----")
    print("Testando: TituloPropriedade aluguel base")
    print("-----")

    jogador = Jogador("Lorhan", Peca.SAPATO)
    prop = TituloPropriedade("Copacabana", 350, "Amarelo", 35, [35, 175, 500, 1100, 1300, 1500], 150)

    prop.comprar(jogador)
    aluguel = prop.calcularAluguel()

    assert aluguel == 35
    print("Aluguel base calculado corretamente")

def test_titulo_propriedade_construir_casa():
    """Testa construção de casas"""
    print("-----")
    print("Testando: TituloPropriedade construir casa")
    print("-----")

    jogador = Jogador("Pedro", Peca.CARRO_CORRIDA)
    jogador.possuiMonopolio = lambda cor: True

    prop = TituloPropriedade("Leblon", 400, "Verde", 40, [40, 200, 600, 1400, 1700, 2000], 200)
    prop.comprar(jogador)

    sucesso = prop.construirCasa()
    assert sucesso == True
    assert prop.getNumCasas() == 1
    assert jogador.getSaldo() == 900

    aluguel = prop.calcularAluguel()
    assert aluguel == 200
    print("Construção de casa funcionando")

def test_titulo_propriedade_construir_hotel():
    """Testa construção de hotel"""
    print("-----")
    print("Testando: TituloPropriedade construir hotel")
    print("-----")

    jogador = Jogador("Ana", Peca.CHAPEU)
    jogador.possuiMonopolio = lambda cor: True

    prop = TituloPropriedade("Botafogo", 300, "Rosa", 25, [25, 125, 375, 875, 1050, 1250], 150)
    prop.comprar(jogador)

    for _ in range(4):
        prop.construirCasa()

    assert prop.getNumCasas() == 4

    sucesso = prop.construirHotel()
    assert sucesso == True
    assert prop.getNumCasas() == 0
    assert prop.temHotel() == True

    aluguel = prop.calcularAluguel()
    assert aluguel == 1250
    print("Construção de hotel funcionando")

def test_titulo_propriedade_hipotecar():
    """Testa hipoteca de propriedade"""
    print("-----")
    print("Testando: TituloPropriedade hipotecar")
    print("-----")

    jogador = Jogador("Carlos", Peca.NAVIO_GUERRA)
    prop = TituloPropriedade("Flamengo", 200, "Laranja", 20, [20, 100, 300, 750, 925, 1100], 100)

    prop.comprar(jogador)
    saldo_antes = jogador.getSaldo()

    valor = prop.hipotecar()

    assert valor == 100
    assert prop.estaHipotecada() == True
    assert jogador.getSaldo() == saldo_antes + 100
    assert prop.calcularAluguel() == 0
    print("Hipoteca funcionando corretamente")

# TESTES TITULOCOMPANHIA

def test_titulo_companhia_inicializacao():
    """Testa inicialização de TituloCompanhia"""
    print("-----")
    print("Testando: TituloCompanhia inicializacao")
    print("-----")

    comp = TituloCompanhia("Enel", 150)

    assert comp.getNome() == "Enel"
    assert comp.getPreco() == 150
    assert comp.getTipo() == "Companhia"
    assert comp.getFatorUmaCompanhia() == 4
    assert comp.getFatorDuasCompanhias() == 10
    print("TituloCompanhia inicializado corretamente")

def test_titulo_companhia_aluguel_uma():
    """Testa cálculo de aluguel com uma companhia"""
    print("-----")
    print("Testando: TituloCompanhia aluguel com uma companhia")
    print("-----")

    jogador = Jogador("Roberto", Peca.LOCOMOTIVA)
    comp = TituloCompanhia("Companhia de Água", 150)

    comp.comprar(jogador)
    aluguel = comp.calcularAluguel(7)

    assert aluguel == 28
    print("Aluguel com uma companhia calculado corretamente")

def test_titulo_companhia_aluguel_duas():
    """Testa cálculo de aluguel com duas companhias"""
    print("-----")
    print("Testando: TituloCompanhia aluguel com duas companhias")
    print("-----")

    jogador = Jogador("Fernanda", Peca.FERRO_PASSAR)
    comp1 = TituloCompanhia("Enel", 150)
    comp2 = TituloCompanhia("Companhia de Água", 150)

    comp1.comprar(jogador)
    comp2.comprar(jogador)

    aluguel = comp1.calcularAluguel(8)

    assert aluguel == 80
    print("Aluguel com duas companhias calculado corretamente")

# TESTES TITULOESTACAO

def test_titulo_estacao_inicializacao():
    """Testa inicialização de TituloEstacao"""
    print("-----")
    print("Testando: TituloEstacao inicializacao")
    print("-----")

    estacao = TituloEstacao("Estação Central", 200)

    assert estacao.getNome() == "Estação Central"
    assert estacao.getPreco() == 200
    assert estacao.getTipo() == "Estacao"
    assert estacao.getAluguelBase() == 25
    print("TituloEstacao inicializado corretamente")

def test_titulo_estacao_aluguel_uma():
    """Testa aluguel com uma estação"""
    print("-----")
    print("Testando: TituloEstacao aluguel com uma estacao")
    print("-----")

    jogador = Jogador("Marcos", Peca.COWBOY)
    estacao = TituloEstacao("Estação Norte", 200)

    estacao.comprar(jogador)
    aluguel = estacao.calcularAluguel()

    assert aluguel == 25
    print("Aluguel com uma estação calculado corretamente")

def test_titulo_estacao_aluguel_multiplas():
    """Testa aluguel com múltiplas estações"""
    print("-----")
    print("Testando: TituloEstacao aluguel com multiplas estacoes")
    print("-----")

    jogador = Jogador("Patrícia", Peca.SACO_DINHEIRO)
    est1 = TituloEstacao("Estação Sul", 200)
    est2 = TituloEstacao("Estação Leste", 200)
    est3 = TituloEstacao("Estação Oeste", 200)

    est1.comprar(jogador)
    est2.comprar(jogador)
    est3.comprar(jogador)

    aluguel = est1.calcularAluguel()

    assert aluguel == 100
    print("Aluguel com múltiplas estações calculado corretamente")

def test_titulo_transferir_propriedade():
    """Testa transferência de propriedade entre jogadores"""
    print("-----")
    print("Testando: transferir propriedade")
    print("-----")

    jogador1 = Jogador("Vendedor", Peca.CACHORRO)
    jogador2 = Jogador("Comprador", Peca.SAPATO)

    prop = TituloPropriedade("Propriedade X", 300, "Vermelho", 30, [30, 150, 450, 1000, 1200, 1400], 200)
    prop.comprar(jogador1)

    prop.transferirPropriedade(jogador2)

    assert prop.getProprietario() == jogador2
    assert prop in jogador2.getPropriedades()
    assert prop not in jogador1.getPropriedades()
    print("Transferência funcionando corretamente")

test_titulo_propriedade_inicializacao()
test_titulo_propriedade_compra()
test_titulo_propriedade_aluguel_base()
test_titulo_propriedade_construir_casa()
test_titulo_propriedade_construir_hotel()
test_titulo_propriedade_hipotecar()

test_titulo_companhia_inicializacao()
test_titulo_companhia_aluguel_uma()
test_titulo_companhia_aluguel_duas()

test_titulo_estacao_inicializacao()
test_titulo_estacao_aluguel_uma()
test_titulo_estacao_aluguel_multiplas()

test_titulo_transferir_propriedade()