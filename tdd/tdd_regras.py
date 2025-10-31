import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.regras import Regras

def test_obter_saldo_inicial():
    """Testa se retorna o saldo inicial correto"""
    print("-----")
    print("Testando: obter saldo inicial")
    print("-----")
    regras = Regras()
    assert regras.obter_saldo_inicial() == 1500

def test_obter_salario_inicio():
    """Testa se retorna o salário correto"""
    print("-----")
    print("Testando: obter salario do inicio")
    print("-----")
    regras = Regras()
    assert regras.obter_salario_inicio() == 200

def test_obter_valor_prisao():
    """Testa se retorna o valor da fiança correto"""
    print("-----")
    print("Testando: obter valor da prisao")
    print("-----")
    regras = Regras()
    assert regras.obter_valor_prisao() == 50

def test_obter_max_casas():
    """Testa se retorna o máximo de casas correto"""
    print("-----")
    print("Testando: obter maximo de casas")
    print("-----")
    regras = Regras()
    assert regras.obter_max_casas() == 4

def test_obter_max_duplas():
    """Testa se retorna o máximo de duplas correto"""
    print("-----")
    print("Testando: obter maximo de duplas")
    print("-----")
    regras = Regras()
    assert regras.obter_max_duplas() == 2

def test_validar_compra_propriedade_livre():
    """Testa compra de propriedade livre com dinheiro suficiente"""
    print("-----")
    print("Testando: validar compra de propriedade livre")
    print("-----")
    regras = Regras()
    
    jogador = type('Jogador', (), {'dinheiro': 500})()
    propriedade = type('Propriedade', (), {'preco': 300, 'proprietario': None})()
    
    assert regras.validar_compra(jogador, propriedade) == True

def test_validar_compra_sem_dinheiro():
    """Testa compra sem dinheiro suficiente"""
    print("-----")
    print("Testando: validar compra sem dinheiro")
    print("-----")
    regras = Regras()
    
    jogador = type('Jogador', (), {'dinheiro': 100})()
    propriedade = type('Propriedade', (), {'preco': 300, 'proprietario': None})()
    
    assert regras.validar_compra(jogador, propriedade) == False

def test_validar_compra_propriedade_ocupada():
    """Testa compra de propriedade já ocupada"""
    print("-----")
    print("Testando: validar compra de propriedade ocupada")
    print("-----")
    regras = Regras()
    
    outro_jogador = type('Jogador', (), {'dinheiro': 1000})()
    jogador = type('Jogador', (), {'dinheiro': 500})()
    propriedade = type('Propriedade', (), {'preco': 300, 'proprietario': outro_jogador})()
    
    assert regras.validar_compra(jogador, propriedade) == False

def test_validar_construcao_valida():
    """Testa construção válida"""
    print("-----")
    print("Testando: validar construcao valida")
    print("-----")
    regras = Regras()
    
    jogador = type('Jogador', (), {'dinheiro': 200})()
    propriedade = type('Propriedade', (), {
        'proprietario': jogador,
        'num_casas': 2,
        'custo_casa': 100
    })()
    
    assert regras.validar_construcao(jogador, propriedade) == True

def test_validar_construcao_nao_proprietario():
    """Testa construção quando não é proprietário"""
    print("-----")
    print("Testando: validar construcao quando nao e proprietario")
    print("-----")
    regras = Regras()
    
    jogador = type('Jogador', (), {'dinheiro': 200})()
    outro_jogador = type('Jogador', (), {'dinheiro': 500})()
    propriedade = type('Propriedade', (), {
        'proprietario': outro_jogador,
        'num_casas': 2,
        'custo_casa': 100
    })()
    
    assert regras.validar_construcao(jogador, propriedade) == False

def test_validar_construcao_max_casas():
    """Testa construção quando já tem máximo de casas"""
    print("-----")
    print("Testando: validar construcao no maximo de casas")
    print("-----")
    regras = Regras()
    
    jogador = type('Jogador', (), {'dinheiro': 200})()
    propriedade = type('Propriedade', (), {
        'proprietario': jogador,
        'num_casas': 4,
        'custo_casa': 100
    })()
    
    assert regras.validar_construcao(jogador, propriedade) == False

def test_validar_construcao_sem_dinheiro():
    """Testa construção sem dinheiro suficiente"""
    print("-----")
    print("Testando: validar construcao sem dinheiro")
    print("-----")
    regras = Regras()
    
    jogador = type('Jogador', (), {'dinheiro': 50})()
    propriedade = type('Propriedade', (), {
        'proprietario': jogador,
        'num_casas': 2,
        'custo_casa': 100
    })()
    
    assert regras.validar_construcao(jogador, propriedade) == False

def test_calcular_aluguel_sem_casas():
    """Testa cálculo de aluguel sem casas"""
    print("-----")
    print("Testando: calcular aluguel sem casas")
    print("-----")
    regras = Regras()
    
    propriedade = type('Propriedade', (), {'aluguel_base': 50})()
    
    assert regras.calcular_aluguel(propriedade) == 50

def test_calcular_aluguel_com_casas():
    """Testa cálculo de aluguel com casas"""
    print("-----")
    print("Testando: calcular aluguel com casas")
    print("-----")
    regras = Regras()
    
    propriedade = type('Propriedade', (), {
        'aluguel_base': 50,
        'num_casas': 2,
        'alugueis': [100, 200, 400, 800]
    })()
    
    assert regras.calcular_aluguel(propriedade) == 200

test_obter_saldo_inicial()
test_obter_salario_inicio()
test_obter_valor_prisao()
test_obter_max_casas()
test_obter_max_duplas()
test_validar_compra_propriedade_livre()
test_validar_compra_sem_dinheiro()
test_validar_compra_propriedade_ocupada()
test_validar_construcao_valida()
test_validar_construcao_nao_proprietario()
test_validar_construcao_max_casas()
test_validar_construcao_sem_dinheiro()
test_calcular_aluguel_sem_casas()
test_calcular_aluguel_com_casas()