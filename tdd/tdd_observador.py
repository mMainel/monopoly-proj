import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.observador import Observador
from modules.eventoJogo import EventoJogo, TipoEvento

class ObservadorTeste(Observador):
    """Implementação concreta de Observador para testes"""
    def __init__(self):
        self.eventos_recebidos = []
    
    def notificar(self, evento: EventoJogo) -> None:
        self.eventos_recebidos.append(evento)

def test_observador_e_classe_abstrata():
    """Testa se Observador é uma classe abstrata"""
    print("-----")
    print("Testando: observador e classe abstrata")
    print("-----")
    try:
        obs = Observador()
        assert False, "Não deveria conseguir instanciar classe abstrata"
    except TypeError:
        pass

def test_observador_concreto_pode_ser_criado():
    """Testa se implementação concreta pode ser criada"""
    print("-----")
    print("Testando: observador concreto pode ser criado")
    print("-----")
    obs = ObservadorTeste()
    assert obs is not None
    assert isinstance(obs, Observador)

def test_observador_recebe_notificacao():
    """Testa se observador recebe notificações"""
    print("-----")
    print("Testando: observador recebe notificacao")
    print("-----")
    obs = ObservadorTeste()
    
    evento = EventoJogo(
        tipo=TipoEvento.TURNO_INICIADO,
        dados={'turno': 1}
    )
    
    obs.notificar(evento)
    
    assert len(obs.eventos_recebidos) == 1
    assert obs.eventos_recebidos[0] == evento

def test_observador_recebe_multiplas_notificacoes():
    """Testa se observador recebe múltiplas notificações"""
    print("-----")
    print("Testando: observador recebe multiplas notificacoes")
    print("-----")
    obs = ObservadorTeste()
    
    evento1 = EventoJogo(tipo=TipoEvento.TURNO_INICIADO, dados={'turno': 1})
    evento2 = EventoJogo(tipo=TipoEvento.DADOS_LANCADOS, dados={'resultado': (3, 5)})
    evento3 = EventoJogo(tipo=TipoEvento.JOGADOR_MOVEU, dados={'posicao': 10})
    
    obs.notificar(evento1)
    obs.notificar(evento2)
    obs.notificar(evento3)
    
    assert len(obs.eventos_recebidos) == 3
    assert obs.eventos_recebidos[0].tipo == TipoEvento.TURNO_INICIADO
    assert obs.eventos_recebidos[1].tipo == TipoEvento.DADOS_LANCADOS
    assert obs.eventos_recebidos[2].tipo == TipoEvento.JOGADOR_MOVEU

def test_multiplos_observadores():
    """Testa múltiplos observadores independentes"""
    print("-----")
    print("Testando: multiplos observadores")
    print("-----")
    obs1 = ObservadorTeste()
    obs2 = ObservadorTeste()
    
    evento = EventoJogo(tipo=TipoEvento.TURNO_INICIADO, dados={'turno': 1})
    
    obs1.notificar(evento)
    
    assert len(obs1.eventos_recebidos) == 1
    assert len(obs2.eventos_recebidos) == 0

test_observador_e_classe_abstrata()
test_observador_concreto_pode_ser_criado()
test_observador_recebe_notificacao()
test_observador_recebe_multiplas_notificacoes()
test_multiplos_observadores()