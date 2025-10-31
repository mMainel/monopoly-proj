import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.dados import Dados

def test_lancar_retorna_tupla():
    """Testa se lancar retorna uma tupla de dois valores"""
    print("-----")
    print("Testando: lancar retorna tupla de dois valores")
    print("-----")
    dados = Dados()
    resultado = dados.lancar()
    assert isinstance(resultado, tuple)
    assert len(resultado) == 2

def test_lancar_valores_validos():
    """Testa se os valores estão entre 1 e 6"""
    print("-----")
    print("Testando: valores dos dados entre 1 e 6")
    print("-----")
    dados = Dados()
    for _ in range(20):
        resultado = dados.lancar()
        assert 1 <= resultado[0] <= 6
        assert 1 <= resultado[1] <= 6

def test_isDupla_detecta_corretamente():
    """Testa se isDupla detecta quando os valores são iguais"""
    print("-----")
    print("Testando: deteccao de duplas")
    print("-----")
    dados = Dados()
    encontrou_dupla = False
    encontrou_nao_dupla = False
    
    for _ in range(100):
        resultado = dados.lancar()
        if resultado[0] == resultado[1]:
            assert dados.isDupla() == True
            encontrou_dupla = True
        else:
            assert dados.isDupla() == False
            encontrou_nao_dupla = True
        
        if encontrou_dupla and encontrou_nao_dupla:
            break

def test_isDupla_sem_lancamento():
    print("-----")
    print("Testando: isDupla sem lancamento")
    print("-----")
    dados = Dados()
    try:
        dados.isDupla()
        assert False, "Deveria ter lançado ValueError"
    except ValueError as e:
        assert "Nenhum lançamento" in str(e)

def test_soma_dados_calcula_corretamente():
    """Testa se soma_dados retorna a soma correta"""
    print("-----")
    print("Testando: soma dos dados calcula corretamente")
    print("-----")
    dados = Dados()
    resultado = dados.lancar()
    soma = dados.soma_dados()
    assert soma == resultado[0] + resultado[1]

def test_soma_dados_sem_lancamento():
    """Testa se soma_dados lança erro quando chamado sem lançar"""
    print("-----")
    print("Testando: soma_dados sem lancamento")
    print("-----")
    dados = Dados()
    try:
        dados.soma_dados()
        assert False, "Deveria ter lançado ValueError"
    except ValueError as e:
        assert "Nenhum lançamento" in str(e)

def test_ultimo_lancamento_armazenado():
    """Testa se o último lançamento é armazenado corretamente"""
    print("-----")
    print("Testando: ultimo lancamento armazenado")
    print("-----")
    dados = Dados()
    resultado1 = dados.lancar()
    assert dados.ultimo_lancamento == resultado1
    
    resultado2 = dados.lancar()
    assert dados.ultimo_lancamento == resultado2
    assert dados.ultimo_lancamento != resultado1 or resultado1 == resultado2

test_lancar_retorna_tupla()
test_lancar_valores_validos()
test_isDupla_detecta_corretamente()
test_isDupla_sem_lancamento()
test_soma_dados_calcula_corretamente()
test_soma_dados_sem_lancamento()
test_ultimo_lancamento_armazenado()