import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.transacao import Transacao
from modules.tipoTransacao import TipoTransacao
from modules.jogador import Jogador
from modules.peca import Peca

def test_transacao_inicializacao():
    """Testa inicialização de uma transação"""
    print("-----")
    print("Testando: transacao inicializacao")
    print("-----")

    jogador1 = Jogador("Lucas", Peca.CACHORRO)
    jogador2 = Jogador("Lorhan", Peca.SAPATO)

    transacao = Transacao(
        tipo=TipoTransacao.ALUGUEL,
        valor=200,
        origem=jogador1,
        destino=jogador2,
        descricao="Pagamento de aluguel da Medicina"
    )

    assert transacao.getTipo() == TipoTransacao.ALUGUEL
    assert transacao.getValor() == 200
    assert transacao.getOrigem() == jogador1
    assert transacao.getDestino() == jogador2
    assert transacao.getDescricao() == "Pagamento de aluguel da Medicina"
    assert transacao.getTimestamp() is not None
    print("Transacao inicializada corretamente")

def test_transacao_compra_propriedade():
    """Testa transação de compra de propriedade"""
    print("-----")
    print("Testando: transacao compra propriedade")
    print("-----")

    jogador = Jogador("Carlos", Peca.CARRO_CORRIDA)

    transacao = Transacao(
        tipo=TipoTransacao.COMPRA_PROPRIEDADE,
        valor=350,
        origem=jogador,
        destino=None,
        descricao="Compra de Matemática"
    )

    assert transacao.getTipo() == TipoTransacao.COMPRA_PROPRIEDADE
    assert transacao.getValor() == 350
    assert transacao.getOrigem() == jogador
    assert transacao.getDestino() is None
    print("Transacao de compra criada corretamente")

def test_transacao_salario():
    """Testa transação de salário"""
    print("-----")
    print("Testando: transacao salario")
    print("-----")

    jogador = Jogador("Emanuel", Peca.CHAPEU)

    transacao = Transacao(
        tipo=TipoTransacao.SALARIO,
        valor=200,
        origem=None,
        destino=jogador,
        descricao="Passou pelo GO"
    )

    assert transacao.getTipo() == TipoTransacao.SALARIO
    assert transacao.getValor() == 200
    assert transacao.getOrigem() is None
    assert transacao.getDestino() == jogador
    print("Transacao de salário criada corretamente")

def test_transacao_construcao():
    """Testa transação de construção"""
    print("-----")
    print("Testando: transacao construcao")
    print("-----")

    jogador = Jogador("João", Peca.NAVIO_GUERRA)

    transacao = Transacao(
        tipo=TipoTransacao.CONSTRUCAO,
        valor=150,
        origem=jogador,
        destino=None,
        descricao="Construção de casa em Biologia"
    )

    assert transacao.getTipo() == TipoTransacao.CONSTRUCAO
    assert transacao.getValor() == 150
    print("Transacao de construção criada corretamente")

def test_transacao_hipoteca():
    """Testa transação de hipoteca"""
    print("-----")
    print("Testando: transacao hipoteca")
    print("-----")

    jogador = Jogador("Luisa", Peca.DEDAL)

    transacao = Transacao(
        tipo=TipoTransacao.HIPOTECA,
        valor=200,
        origem=None,
        destino=jogador,
        descricao="Hipoteca de Filosofia"
    )

    assert transacao.getTipo() == TipoTransacao.HIPOTECA
    assert transacao.getValor() == 200
    print("Transacao de hipoteca criada corretamente")

def test_transacao_fianca():
    """Testa transação de fiança da cadeia"""
    print("-----")
    print("Testando: transacao fianca")
    print("-----")

    jogador = Jogador("Roberto", Peca.LOCOMOTIVA)

    transacao = Transacao(
        tipo=TipoTransacao.FIANCA,
        valor=50,
        origem=jogador,
        destino=None,
        descricao="Pagamento de fiança"
    )

    assert transacao.getTipo() == TipoTransacao.FIANCA
    assert transacao.getValor() == 50
    print("Transacao de fiança criada corretamente")

def test_transacao_leilao():
    """Testa transação de leilão"""
    print("-----")
    print("Testando: transacao leilao")
    print("-----")

    jogador = Jogador("Fernanda", Peca.FERRO_PASSAR)

    transacao = Transacao(
        tipo=TipoTransacao.LEILAO,
        valor=450,
        origem=jogador,
        destino=None,
        descricao="Venceu leilão de Botafogo"
    )

    assert transacao.getTipo() == TipoTransacao.LEILAO
    assert transacao.getValor() == 450
    print("Transacao de leilão criada corretamente")

def test_transacao_transferencia():
    """Testa transação de transferência entre jogadores"""
    print("-----")
    print("Testando: transacao transferencia")
    print("-----")

    jogador1 = Jogador("Marcos", Peca.COWBOY)
    jogador2 = Jogador("Patrícia", Peca.SACO_DINHEIRO)

    transacao = Transacao(
        tipo=TipoTransacao.TRANSFERENCIA,
        valor=300,
        origem=jogador1,
        destino=jogador2,
        descricao="Negociação de propriedade"
    )

    assert transacao.getTipo() == TipoTransacao.TRANSFERENCIA
    assert transacao.getOrigem() == jogador1
    assert transacao.getDestino() == jogador2
    print("Transacao de transferência criada corretamente")

def test_transacao_imposto():
    """Testa transação de imposto"""
    print("-----")
    print("Testando: transacao imposto")
    print("-----")

    jogador = Jogador("Leo", Peca.CARRINHO_MAO)

    transacao = Transacao(
        tipo=TipoTransacao.IMPOSTO,
        valor=100,
        origem=jogador,
        destino=None,
        descricao="Imposto de renda"
    )

    assert transacao.getTipo() == TipoTransacao.IMPOSTO
    assert transacao.getValor() == 100
    print("Transacao de imposto criada corretamente")

def test_transacao_str():
    """Testa representação em string da transação"""
    print("-----")
    print("Testando: transacao __str__")
    print("-----")

    jogador1 = Jogador("Vendedor", Peca.CACHORRO)
    jogador2 = Jogador("Comprador", Peca.SAPATO)

    transacao = Transacao(
        tipo=TipoTransacao.ALUGUEL,
        valor=150,
        origem=jogador1,
        destino=jogador2
    )

    str_transacao = str(transacao)

    assert "Pagamento de Aluguel" in str_transacao
    assert "$150" in str_transacao
    assert "Vendedor" in str_transacao
    assert "Comprador" in str_transacao
    print("String de transação formatada corretamente")

def test_transacao_sem_descricao():
    """Testa transação sem descrição"""
    print("-----")
    print("Testando: transacao sem descricao")
    print("-----")

    jogador = Jogador("Jogador", Peca.CACHORRO)

    transacao = Transacao(
        tipo=TipoTransacao.PREMIO,
        valor=100,
        origem=None,
        destino=jogador
    )

    assert transacao.getDescricao() == ""
    assert transacao.getTipo() == TipoTransacao.PREMIO
    print("Transacao sem descrição criada corretamente")

test_transacao_inicializacao()
test_transacao_compra_propriedade()
test_transacao_salario()
test_transacao_construcao()
test_transacao_hipoteca()
test_transacao_fianca()
test_transacao_leilao()
test_transacao_transferencia()
test_transacao_imposto()
test_transacao_str()
test_transacao_sem_descricao()