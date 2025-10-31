import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.eventoJogo import TipoEvento, EventoJogo
from datetime import datetime

def test_tipo_evento_tem_todos_tipos():
    """Testa se todos os tipos de eventos existem"""
    print("-----")
    print("Testando: tipo evento tem todos os tipos")
    print("-----")
    assert hasattr(TipoEvento, 'TURNO_INICIADO')
    assert hasattr(TipoEvento, 'TURNO_FINALIZADO')
    assert hasattr(TipoEvento, 'DADOS_LANCADOS')
    assert hasattr(TipoEvento, 'DUPLA_LANCADA')
    assert hasattr(TipoEvento, 'JOGADOR_MOVEU')
    assert hasattr(TipoEvento, 'PASSOU_INICIO')
    assert hasattr(TipoEvento, 'PROPRIEDADE_COMPRADA')
    assert hasattr(TipoEvento, 'ALUGUEL_PAGO')
    assert hasattr(TipoEvento, 'CONSTRUCAO_FEITA')
    assert hasattr(TipoEvento, 'JOGADOR_PRESO')
    assert hasattr(TipoEvento, 'JOGADOR_FALIU')

def test_evento_jogo_criacao_basica():
    """Testa criação básica de evento"""
    print("-----")
    print("Testando: criacao basica de evento")
    print("-----")
    evento = EventoJogo(
        tipo=TipoEvento.TURNO_INICIADO,
        dados={'turno': 1}
    )
    
    assert evento.tipo == TipoEvento.TURNO_INICIADO
    assert evento.dados == {'turno': 1}
    assert isinstance(evento.timestamp, datetime)

def test_evento_jogo_timestamp_automatico():
    """Testa se timestamp é gerado automaticamente"""
    print("-----")
    print("Testando: timestamp automatico")
    print("-----")
    evento = EventoJogo(
        tipo=TipoEvento.DADOS_LANCADOS,
        dados={'resultado': (3, 5)}
    )
    
    assert evento.timestamp is not None
    assert isinstance(evento.timestamp, datetime)

def test_evento_jogo_imutavel():
    """Testa se evento é imutável"""
    print("-----")
    print("Testando: evento e imutavel")
    print("-----")
    evento = EventoJogo(
        tipo=TipoEvento.JOGADOR_MOVEU,
        dados={'posicao': 10}
    )
    
    try:
        evento.tipo = TipoEvento.TURNO_FINALIZADO
        assert False, "Deveria ter lançado erro ao tentar modificar"
    except:
        pass

def test_evento_jogo_com_dados_complexos():
    """Testa event"""
    print("-----")
    print("Testando: evento")
    print("-----")
    evento = EventoJogo(
        tipo=TipoEvento.PROPRIEDADE_COMPRADA,
        dados={
            'jogador_id': 1,
            'propriedade': 'Leblon',
            'valor': 400,
            'casas': 0
        }
    )
    
    assert evento.dados['jogador_id'] == 1
    assert evento.dados['propriedade'] == 'Leblon'
    assert evento.dados['valor'] == 400

def test_eventos_diferentes_tem_timestamps_diferentes():
    """Testa que eventos criados em momentos diferentes têm timestamps diferentes"""
    print("-----")
    print("Testando: eventos tem timestamps diferentes")
    print("-----")
    evento1 = EventoJogo(
        tipo=TipoEvento.TURNO_INICIADO,
        dados={'turno': 1}
    )

    evento2 = EventoJogo(
        tipo=TipoEvento.TURNO_INICIADO,
        dados={'turno': 2}
    )
    
    assert evento1.timestamp < evento2.timestamp

test_tipo_evento_tem_todos_tipos()
test_evento_jogo_criacao_basica()
test_evento_jogo_timestamp_automatico()
test_evento_jogo_imutavel()
test_evento_jogo_com_dados_complexos()
test_eventos_diferentes_tem_timestamps_diferentes()