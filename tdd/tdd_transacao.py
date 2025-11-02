import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.transacao import transacao, tipoTransacao

def test_tipoTrasacao_enum():
    print("-----")
    print("Testando: enumeração de tipos de transação")
    print("-----")
    assert hasattr(tipoTransacao, 'ALUGUEL')
    assert hasattr(tipoTransacao, 'COMPRA_PROPRIEDADE')
    assert hasattr(tipoTransacao, 'SALARIO')
    assert hasattr(tipoTransacao, 'TAXA')
    assert hasattr(tipoTransacao, 'CARTA')
    assert hasattr(tipoTransacao, 'CONSTRUCAO')
    assert hasattr(tipoTransacao, 'HIPOTECA')
    assert hasattr(tipoTransacao, 'LEILAO')

def test_transacao_inicializacao():
    print("-----")
    print("Testando: inicialização de transação")
    print("-----")
    origem_mock = type('MockJogador', (), {'nome': 'Jogador1'})()
    destino_mock = type('MockJogador', (), {'nome': 'Jogador2'})()
    valor = 200
    tipo = tipoTransacao.ALUGUEL
    descricao = "Pagamento de aluguel"
    
    transacao_instance = transacao(origem_mock, destino_mock, valor, tipo, descricao)
    
    assert transacao_instance.origem == origem_mock
    assert transacao_instance.destino == destino_mock

if __name__ == "__main__":
    test_tipoTrasacao_enum()
    test_transacao_inicializacao()