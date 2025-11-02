import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.banco import banco
from modules.titulo import tituloPropriedade, titulo
from random import randint

class propriedadeMock():
    def __init__(self, nome, valorHipoteca):
        self.nome = nome
        self.valorHipoteca = valorHipoteca
        self.proprietario = None
        self.casas = 0
        self.hotel = 0

    def transferir_proprietario(self, jogador):
        self.proprietario = jogador

class JogadorMock:  # classe teste
    def __init__(self, nome, dinheiro):
        self.nome = nome
        self.dinheiro = dinheiro
        self.propriedades = []

    def debitar(self, valor):
        self.dinheiro -= valor

    def creditar(self, valor):
        self.dinheiro += valor

    def realizarlance(self):
        return randint(0, self.dinheiro)

PROPRIEDADES = [tituloPropriedade(None, False, 1000, propriedadeMock(f'{a}',100),10,1000) for a in range(10)]



def test_banco_inicializa_propriedades():
    print("-----")
    print("Testando: inicializacao do banco e propriedades disponiveis")
    print("-----")
    b = banco(PROPRIEDADES)
    assert hasattr(b, "propriedadesDisponiveis")
    assert isinstance(b.propriedadesDisponiveis, list)
    assert len(b.propriedadesDisponiveis) == 10


def test_vender_propriedade_sucesso():
    print("-----")
    print("Testando: venda de propriedade sem dono pelo banco")
    print("-----")
    b = banco(PROPRIEDADES)
    titulo = b.propriedadesDisponiveis[0]
    jogador = JogadorMock("Jogador1", 10000)
    print(b.vender_propriedade(titulo, jogador))
    print(b.propriedadesDisponiveis)
    assert titulo not in b.propriedadesDisponiveis , "Propriedade não foi removida do banco após venda."
    assert getattr(titulo, "proprietario", None) == jogador


def test_vender_mesma_propriedade_novamente():
    print("-----")
    print("Testando: tentativa de vender novamente a mesma propriedade já vendida")
    print("-----")
    b = banco(PROPRIEDADES[1:])
    titulo = PROPRIEDADES[0]
    jogador = JogadorMock("Jogador1", 500)
    b.vender_propriedade(titulo, jogador)
    try:
        b.vender_propriedade(titulo, jogador)
    except Exception:
        # comportamento aceitável se o banco impedir venda de propriedade já vendida
        return
    # se não levantou, garantir que a propriedade não foi re-adicionada ao banco
    assert titulo not in b.propriedadesDisponiveis

def test_vender_casa_sucesso():
    print("-----")
    print("Testando: venda de casa pelo banco")
    print("-----")
    b = banco(PROPRIEDADES)
    titulo = b.propriedadesDisponiveis[0]
    sucesso = b.vender_casa(titulo)
    assert sucesso == True, "Banco não conseguiu vender casa quando deveria."
    assert b.casasDisponiveis == 31, "Número de casas disponíveis no banco não foi decrementado corretamente."
    print('------')
    print('teste comprar casa')
    b.comprar_construcao("casa", titulo)
    assert b.casasDisponiveis == 32, "Número de casas disponíveis no banco não foi incrementado corretamente após compra."
    assert titulo.propriedade.casas == 0, "Número de casas na propriedade não foi decrementado corretamente após venda."
    
def test_vender_hotel_sucesso():
    print("-----")
    print("Testando: venda de hotel pelo banco")
    print("-----")
    b = banco(PROPRIEDADES)
    titulo = b.propriedadesDisponiveis[0]
    sucesso = b.vender_hotel(titulo)
    assert sucesso == True, "Banco não conseguiu vender hotel quando deveria."
    assert b.hoteisDisponiveis == 11, "Número de hotéis disponíveis no banco não foi decrementado corretamente."
    print('------')
    print('teste comprar hotel')
    b.comprar_construcao("hotel", titulo)
    assert b.hoteisDisponiveis == 12, "Número de hotéis disponíveis no banco não foi incrementado corretamente após compra."
    assert titulo.propriedade.hotel == 0, "Número de hotéis na propriedade não foi decrementado corretamente após venda."

def teste_pargar_salario():
    print("-----")
    print("Testando: pagamento de salário pelo banco")
    print("-----")
    b = banco(PROPRIEDADES)
    jogador = JogadorMock("Jogador1", 1000)
    salario_inicial = jogador.dinheiro
    b.pagar_salario(jogador)
    assert jogador.dinheiro == salario_inicial + 200, "Salário não foi pago corretamente pelo banco."

def test_cobrar_taxa():
    print("-----")
    print("Testando: cobrança de taxa pelo banco")
    print("-----")
    b = banco(PROPRIEDADES)
    jogador = JogadorMock("Jogador1", 1000)
    taxa = 150
    saldo_inicial = jogador.dinheiro
    b.cobrar_taxa(jogador, taxa)
    assert jogador.dinheiro == saldo_inicial - taxa, "Taxa não foi cobrada corretamente pelo banco."

def test_hipotecar_titulo():
    print("-----")
    print("Testando: hipoteca de título pelo banco")
    print("-----")
    b = banco(PROPRIEDADES)
    titulo = b.propriedadesDisponiveis[0]
    assert not titulo.hipotecado, "Título já está hipotecado antes do teste."
    titulo.hipotecar()
    assert titulo.hipotecado, "Título não foi hipotecado corretamente."

def test_realizar_leilao():
    print("-----")
    print("Testando: realização de leilão pelo banco")
    print("-----")
    b = banco(PROPRIEDADES)
    propriedade = propriedadeMock("PropriedadeLeilao", 200)
    jogador1 = JogadorMock("Jogador1", 500)
    jogador2 = JogadorMock("Jogador2", 800)
    jogadores = [jogador1, jogador2]
    leilao = b.realizar_leilao(propriedade, jogadores=[jogador1, jogador2])
    vencedor = leilao.vencedor
    lance_vencedor = leilao.lance_atual
    assert vencedor in jogadores, "Vencedor do leilão não é um dos jogadores participantes."
    assert lance_vencedor <= vencedor.dinheiro + lance_vencedor, "Lance vencedor não é válido."

if __name__ == "__main__":
    test_banco_inicializa_propriedades()
    test_vender_propriedade_sucesso()
    test_vender_mesma_propriedade_novamente()
    test_vender_casa_sucesso()
    test_vender_hotel_sucesso()
    teste_pargar_salario()
    test_cobrar_taxa()
    test_hipotecar_titulo()
    test_realizar_leilao()