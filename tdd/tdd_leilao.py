import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.leilao import Leilao
from modules.jogador import Jogador
from modules.peca import Peca

def test_iniciar_leilao():
    """Testa inicialização de um leilão"""
    print("-----")
    print("Testando: iniciar leilão")
    print("-----")
    
    leilao = Leilao()
    jogador1 = Jogador("João", Peca.CACHORRO)
    jogador2 = Jogador("Maria", Peca.SAPATO)
    
    propriedade = type('Propriedade', (), {'nome': 'Avenida Atlântica', 'preco': 300})()
    
    leilao.iniciarLeilao(propriedade, [jogador1, jogador2])
    
    assert leilao.propriedade == propriedade
    assert len(leilao.participantes) == 2
    assert leilao.ativo == True
    assert leilao.lance_minimo == 1
    print("Leilão iniciado corretamente")

def test_fazer_lance_valido():
    """Testa fazer um lance válido"""
    print("-----")
    print("Testando: fazer lance válido")
    print("-----")
    
    leilao = Leilao()
    jogador1 = Jogador("João", Peca.CACHORRO)
    jogador2 = Jogador("Maria", Peca.SAPATO)
    
    propriedade = type('Propriedade', (), {'nome': 'Avenida Atlântica', 'preco': 300})()
    
    leilao.iniciarLeilao(propriedade, [jogador1, jogador2])
    
    sucesso = leilao.fazerLance(jogador1, 100)
    
    assert sucesso == True
    assert leilao.lances[jogador1] == 100
    assert leilao.lance_minimo == 101
    print("Lance válido aceito")

def test_fazer_lance_invalido_menor():
    """Testa lance menor que o mínimo"""
    print("-----")
    print("Testando: lance menor que mínimo")
    print("-----")
    
    leilao = Leilao()
    jogador1 = Jogador("João", Peca.CACHORRO)
    jogador2 = Jogador("Maria", Peca.SAPATO)
    
    propriedade = type('Propriedade', (), {'nome': 'Avenida Atlântica', 'preco': 300})()
    
    leilao.iniciarLeilao(propriedade, [jogador1, jogador2])
    leilao.fazerLance(jogador1, 100)
    
    sucesso = leilao.fazerLance(jogador2, 50)
    
    assert sucesso == False
    assert leilao.lances[jogador2] == 0
    print("Lance inválido rejeitado")

def test_fazer_lance_sem_saldo():
    """Testa lance maior que o saldo do jogador"""
    print("-----")
    print("Testando: lance sem saldo suficiente")
    print("-----")
    
    leilao = Leilao()
    jogador1 = Jogador("João", Peca.CACHORRO)
    
    propriedade = type('Propriedade', (), {'nome': 'Avenida Atlântica', 'preco': 300})()
    
    leilao.iniciarLeilao(propriedade, [jogador1])
    
    sucesso = leilao.fazerLance(jogador1, 2000)
    
    assert sucesso == False
    print("Lance sem saldo rejeitado")

def test_finalizar_leilao_com_vencedor():
    """Testa finalização de leilão com vencedor"""
    print("-----")
    print("Testando: finalizar leilão com vencedor")
    print("-----")
    
    leilao = Leilao()
    jogador1 = Jogador("João", Peca.CACHORRO)
    jogador2 = Jogador("Maria", Peca.SAPATO)
    
    propriedade = type('Propriedade', (), {
        'nome': 'Avenida Atlântica',
        'preco': 300,
        'proprietario': None
    })()
    
    leilao.iniciarLeilao(propriedade, [jogador1, jogador2])
    leilao.fazerLance(jogador1, 200)
    leilao.fazerLance(jogador2, 250)
    
    vencedor, valor = leilao.finalizarLeilao()
    
    assert vencedor == jogador2
    assert valor == 250
    assert leilao.ativo == False
    assert jogador2.getSaldo() == 1250  # 1500 - 250
    assert propriedade in jogador2.getPropriedades()
    print("Leilão finalizado com vencedor correto")

def test_finalizar_leilao_sem_lances():
    """Testa finalização de leilão sem lances"""
    print("-----")
    print("Testando: finalizar leilão sem lances")
    print("-----")
    
    leilao = Leilao()
    jogador1 = Jogador("João", Peca.CACHORRO)
    
    propriedade = type('Propriedade', (), {'nome': 'Avenida Atlântica', 'preco': 300})()
    
    leilao.iniciarLeilao(propriedade, [jogador1])
    
    vencedor, valor = leilao.finalizarLeilao()
    
    assert vencedor is None
    assert valor == 0
    print("Leilão sem lances retorna None")

def test_cancelar_leilao():
    """Testa cancelamento de leilão"""
    print("-----")
    print("Testando: cancelar leilão")
    print("-----")
    
    leilao = Leilao()
    jogador1 = Jogador("João", Peca.CACHORRO)
    
    propriedade = type('Propriedade', (), {'nome': 'Avenida Atlântica', 'preco': 300})()
    
    leilao.iniciarLeilao(propriedade, [jogador1])
    leilao.fazerLance(jogador1, 100)
    leilao.cancelarLeilao()
    
    assert leilao.ativo == False
    assert len(leilao.lances) == 0
    assert leilao.vencedor is None
    print("Leilão cancelado corretamente")

def test_get_lance_maior():
    """Testa obtenção do maior lance"""
    print("-----")
    print("Testando: get lance maior")
    print("-----")
    
    leilao = Leilao()
    jogador1 = Jogador("João", Peca.CACHORRO)
    jogador2 = Jogador("Maria", Peca.SAPATO)
    
    propriedade = type('Propriedade', (), {'nome': 'Avenida Atlântica', 'preco': 300})()
    
    leilao.iniciarLeilao(propriedade, [jogador1, jogador2])
    leilao.fazerLance(jogador1, 100)
    leilao.fazerLance(jogador2, 200)
    
    assert leilao.getLanceMaior() == 200
    print("Maior lance obtido corretamente")

def test_get_lider_atual():
    """Testa obtenção do líder atual"""
    print("-----")
    print("Testando: get líder atual")
    print("-----")
    
    leilao = Leilao()
    jogador1 = Jogador("João", Peca.CACHORRO)
    jogador2 = Jogador("Maria", Peca.SAPATO)
    
    propriedade = type('Propriedade', (), {'nome': 'Avenida Atlântica', 'preco': 300})()
    
    leilao.iniciarLeilao(propriedade, [jogador1, jogador2])
    leilao.fazerLance(jogador1, 100)
    leilao.fazerLance(jogador2, 200)
    
    assert leilao.getLiderAtual() == jogador2
    print("Líder atual obtido corretamente")

test_iniciar_leilao()
test_fazer_lance_valido()
test_fazer_lance_invalido_menor()
test_fazer_lance_sem_saldo()
test_finalizar_leilao_com_vencedor()
test_finalizar_leilao_sem_lances()
test_cancelar_leilao()
test_get_lance_maior()
test_get_lider_atual()
