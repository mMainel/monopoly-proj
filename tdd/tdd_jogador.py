import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.jogador import Jogador
from modules.peca import Peca
from modules.regras import Regras

def test_jogador_inicializacao():
    """Testa inicialização do jogador"""
    print("-----")
    print("Testando: jogador inicializacao")
    print("-----")
    
    jogador = Jogador("Emanuel", Peca.CACHORRO)
    
    assert jogador.getNome() == "Emanuel"
    assert jogador.getPeca() == Peca.CACHORRO
    assert jogador.getSaldo() == 1500
    assert jogador.getPosicao() == 0
    assert len(jogador.getPropriedades()) == 0
    assert jogador.estaEmCadeia() == False
    assert jogador.verificarFalencia() == False
    print("Jogador inicializado corretamente")

def test_jogador_mover():
    """Testa movimento do jogador no tabuleiro"""
    print("-----")
    print("Testando: jogador mover")
    print("-----")
    
    jogador = Jogador("Maria", Peca.CARRO_CORRIDA)
    
    passou_go = jogador.mover(10)
    assert jogador.getPosicao() == 10
    assert passou_go == 0
    
    passou_go = jogador.mover(35)
    assert jogador.getPosicao() == 5
    assert passou_go == 1
    print("Movimentação funcionando corretamente")

def test_jogador_ir_para():
    """Testa ir diretamente para uma posição"""
    print("-----")
    print("Testando: jogador irPara")
    print("-----")
    
    jogador = Jogador("João", Peca.NAVIO_GUERRA)
    jogador.mover(20)
    
    passou_go = jogador.irPara(10)
    assert jogador.getPosicao() == 10
    assert passou_go == False
    print("irPara funcionando corretamente")

def test_jogador_financas():
    """Testa receber e pagar dinheiro"""
    print("-----")
    print("Testando: jogador financas")
    print("-----")
    
    jogador = Jogador("Ana", Peca.SAPATO)
    
    jogador.receberDinheiro(500)
    assert jogador.getSaldo() == 2000
    
    sucesso = jogador.pagarAoBanco(300)
    assert sucesso == True
    assert jogador.getSaldo() == 1700
    print("Finanças funcionando corretamente")

def test_jogador_falencia():
    """Testa falência ao pagar mais que o saldo"""
    print("-----")
    print("Testando: jogador falencia")
    print("-----")
    
    jogador = Jogador("Falido", Peca.DEDAL)
    
    sucesso = jogador.pagarAoBanco(2000)
    assert sucesso == False
    assert jogador.verificarFalencia() == True
    assert jogador.getSaldo() < 0
    print("Falência funcionando corretamente")

def test_jogador_propriedades():
    """Testa adicionar e remover propriedades"""
    print("-----")
    print("Testando: jogador propriedades")
    print("-----")
    
    jogador = Jogador("Proprietário", Peca.CHAPEU)
    prop = type('Propriedade', (), {'nome': 'Av. Atlântica'})()
    
    jogador.adicionarPropriedade(prop)
    assert len(jogador.getPropriedades()) == 1
    
    removeu = jogador.removerPropriedade(prop)
    assert removeu == True
    assert len(jogador.getPropriedades()) == 0
    print("Propriedades funcionando corretamente")

def test_jogador_pagar_aluguel():
    """Testa pagamento de aluguel entre jogadores"""
    print("-----")
    print("Testando: jogador pagarAluguel")
    print("-----")
    
    jogador1 = Jogador("Inquilino", Peca.CACHORRO)
    jogador2 = Jogador("Proprietario", Peca.SAPATO)
    
    saldo_inicial_j2 = jogador2.getSaldo()
    
    sucesso = jogador1.pagarAluguel(jogador2, 200)
    assert sucesso == True
    assert jogador1.getSaldo() == 1300
    assert jogador2.getSaldo() == saldo_inicial_j2 + 200
    print("Pagamento de aluguel funcionando")

def test_jogador_cadeia():
    """Testa entrada e saída da cadeia"""
    print("-----")
    print("Testando: jogador cadeia")
    print("-----")
    
    jogador = Jogador("Preso", Peca.COWBOY)
    
    jogador.entrarCadeia()
    assert jogador.estaEmCadeia() == True
    assert jogador.getPosicao() == 10
    assert jogador.getTurnosCadeia() == 0
    
    jogador.incrementarTurnoCadeia()
    assert jogador.getTurnosCadeia() == 1
    
    jogador.sairCadeia()
    assert jogador.estaEmCadeia() == False
    assert jogador.getTurnosCadeia() == 0
    print("Sistema de cadeia funcionando")

def test_jogador_pode_usar_carta():
    """Testa verificação de carta para sair da cadeia"""
    print("-----")
    print("Testando: jogador podeUsarCartaSairCadeia")
    print("-----")
    
    jogador = Jogador("Sortudo", Peca.LOCOMOTIVA)
    
    assert jogador.podeUsarCartaSairCadeia() == False
    
    jogador.entrarCadeia()
    assert jogador.podeUsarCartaSairCadeia() == False
    
    jogador.adicionarCartaSairCadeia()
    assert jogador.podeUsarCartaSairCadeia() == True
    
    usou = jogador.usarCartaSairCadeia()
    assert usou == True
    assert jogador.podeUsarCartaSairCadeia() == False
    print("Cartas de cadeia funcionando")

def test_jogador_pode_pagar_fianca():
    """Testa verificação de fiança"""
    print("-----")
    print("Testando: jogador podePagarFianca")
    print("-----")
    
    jogador = Jogador("Rico", Peca.SACO_DINHEIRO)
    assert jogador.podePagarFianca() == True
    
    jogador.pagarAoBanco(1480)
    assert jogador.podePagarFianca() == False
    print("Verificação de fiança funcionando")

def test_jogador_tentar_sair_cadeia_dupla():
    """Testa saída da cadeia com dupla"""
    print("-----")
    print("Testando: jogador tentarSairCadeiaDupla")
    print("-----")
    
    jogador = Jogador("Sortudo", Peca.FERRO_PASSAR)
    jogador.entrarCadeia()
    
    saiu = jogador.tentarSairCadeiaDupla(True)
    assert saiu == True
    assert jogador.estaEmCadeia() == False
    print("Saída por dupla funcionando")

def test_jogador_tentar_sair_cadeia_3_turnos():
    """Testa saída forçada após 3 turnos"""
    print("-----")
    print("Testando: jogador tentarSairCadeiaDupla apos 3 turnos")
    print("-----")
    
    jogador = Jogador("Azarado", Peca.CARRINHO_MAO)
    jogador.entrarCadeia()
    
    jogador.incrementarTurnoCadeia()
    jogador.incrementarTurnoCadeia()
    jogador.incrementarTurnoCadeia()
    
    saiu = jogador.tentarSairCadeiaDupla(False)
    assert saiu == True
    assert jogador.estaEmCadeia() == False
    assert jogador.getSaldo() == 1450
    print("Saída forçada após 3 turnos funcionando")

def test_jogador_total_casas():
    """Testa contagem de casas"""
    print("-----")
    print("Testando: jogador getTotalCasas")
    print("-----")
    
    jogador = Jogador("Construtor", Peca.CHAPEU)
    
    prop1 = type('Propriedade', (), {'num_casas': 2})()
    prop2 = type('Propriedade', (), {'num_casas': 3})()
    
    jogador.adicionarPropriedade(prop1)
    jogador.adicionarPropriedade(prop2)
    
    assert jogador.getTotalCasas() == 5
    print("Contagem de casas funcionando")

def test_jogador_calcular_patrimonio():
    """Testa cálculo de patrimônio"""
    print("-----")
    print("Testando: jogador calcularPatrimonio")
    print("-----")
    
    jogador = Jogador("Milionário", Peca.SACO_DINHEIRO)
    
    prop1 = type('Propriedade', (), {'preco': 200, 'num_casas': 2, 'custo_casa': 50})()
    prop2 = type('Propriedade', (), {'preco': 300})()
    
    jogador.adicionarPropriedade(prop1)
    jogador.adicionarPropriedade(prop2)
    
    patrimonio = jogador.calcularPatrimonio()
    assert patrimonio == 1500 + 200 + 100 + 300
    print("Cálculo de patrimônio funcionando")

test_jogador_inicializacao()
test_jogador_mover()
test_jogador_ir_para()
test_jogador_financas()
test_jogador_falencia()
test_jogador_propriedades()
test_jogador_pagar_aluguel()
test_jogador_cadeia()
test_jogador_pode_usar_carta()
test_jogador_pode_pagar_fianca()
test_jogador_tentar_sair_cadeia_dupla()
test_jogador_tentar_sair_cadeia_3_turnos()
test_jogador_total_casas()
test_jogador_calcular_patrimonio()
