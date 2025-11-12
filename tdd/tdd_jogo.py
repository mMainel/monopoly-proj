import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.jogo import Jogo
from modules.observador import Observador
from modules.eventoJogo import EventoJogo, TipoEvento
from modules.dados import Dados
from modules.peca import Peca

class ObservadorTeste(Observador):
    """Observador de teste para capturar eventos"""
    def __init__(self):
        self.eventos = []
    
    def notificar(self, evento: EventoJogo) -> None:
        self.eventos.append(evento)

def criar_config_jogadores(num_jogadores: int):
    """Helper para criar configuração de jogadores para testes"""
    pecas = list(Peca)
    return [(f"Jogador {i+1}", pecas[i % len(pecas)]) for i in range(num_jogadores)]

def test_jogo_inicializacao():
    """Testa inicialização do jogo"""
    print("-----")
    print("Testando: jogo inicializacao")
    print("-----")
    jogo = Jogo()
    
    assert jogo.tabuleiro is None
    assert jogo.banco is None
    assert jogo.dados is not None
    assert len(jogo.jogadores) == 0
    assert jogo.jogadorAtual is None
    assert jogo.turno == 0

def test_iniciar_jogo_com_jogadores():
    """Testa inicialização do jogo com jogadores"""
    print("-----")
    print("Testando: iniciar jogo com jogadores")
    print("-----")
    jogo = Jogo()
    jogo.iniciar_jogo(criar_config_jogadores(3))
    
    assert len(jogo.jogadores) == 3
    assert jogo.jogadorAtual == jogo.jogadores[0]
    assert jogo.turno == 1
    assert jogo.esta_ativo() == True

def test_iniciar_jogo_distribui_dinheiro():
    """Testa se o jogo distribui dinheiro inicial"""
    print("-----")
    print("Testando: iniciar jogo distribui dinheiro")
    print("-----")
    jogo = Jogo()
    jogo.iniciar_jogo(criar_config_jogadores(2))
    
    assert jogo.jogadores[0].dinheiro == 1500
    assert jogo.jogadores[1].dinheiro == 1500

def test_iniciar_jogo_minimo_jogadores():
    """Testa erro ao iniciar sem jogadores"""
    print("-----")
    print("Testando: iniciar jogo minimo jogadores")
    print("-----")
    jogo = Jogo()
    
    try:
        jogo.iniciar_jogo([])  # Lista vazia de jogadores
        assert False, "Deveria ter lançado ValueError"
    except ValueError as e:
        assert "pelo menos 1 jogador" in str(e)

def test_iniciar_jogo_um_jogador_adiciona_ia():
    """Testa que ao iniciar com 1 jogador, uma IA é adicionada automaticamente"""
    print("-----")
    print("Testando: iniciar jogo com 1 jogador adiciona IA")
    print("-----")
    from modules.peca import Peca
    from modules.jogadorIA import JogadorIA
    
    jogo = Jogo()
    jogo.iniciar_jogo([("Humano", Peca.BIOLOGIA)])
    
    # Deve ter 2 jogadores: 1 humano + 1 IA
    assert len(jogo.jogadores) == 2
    assert jogo.jogadores[0].nome == "Humano"
    assert not isinstance(jogo.jogadores[0], JogadorIA)
    assert jogo.jogadores[1].nome == "IA"
    assert isinstance(jogo.jogadores[1], JogadorIA)
    # IAs devem ter peças diferentes
    assert jogo.jogadores[0].peca != jogo.jogadores[1].peca

def test_adicionar_observador():
    """Testa adição de observador"""
    print("-----")
    print("Testando: adicionar observador")
    print("-----")
    jogo = Jogo()
    obs = ObservadorTeste()
    
    jogo.adicionar_observador(obs)
    jogo.iniciar_jogo(criar_config_jogadores(2))
    
    assert len(obs.eventos) > 0
    assert obs.eventos[0].tipo == TipoEvento.TURNO_INICIADO

def test_remover_observador():
    """Testa remoção de observador"""
    print("-----")
    print("Testando: remover observador")
    print("-----")
    jogo = Jogo()
    obs = ObservadorTeste()
    
    jogo.adicionar_observador(obs)
    jogo.remover_observador(obs)
    jogo.iniciar_jogo(criar_config_jogadores(2))
    
    assert len(obs.eventos) == 0

def test_proximo_turno():
    """Testa mudança de turno"""
    print("-----")
    print("Testando: proximo turno")
    print("-----")
    jogo = Jogo()
    jogo.iniciar_jogo(criar_config_jogadores(3))
    
    jogador_inicial = jogo.jogadorAtual
    jogo.proximo_turno()
    
    assert jogo.jogadorAtual != jogador_inicial
    assert jogo.jogadorAtual == jogo.jogadores[1]

def test_proximo_turno_rotacao_circular():
    """Testa rotação circular de turnos"""
    print("-----")
    print("Testando: proximo turno rotacao circular")
    print("-----")
    jogo = Jogo()
    jogo.iniciar_jogo(criar_config_jogadores(3))
    
    jogo.proximo_turno()
    jogo.proximo_turno()
    jogo.proximo_turno()
    
    assert jogo.jogadorAtual == jogo.jogadores[0]
    assert jogo.turno == 2

def test_verificar_vencedor_sem_vencedor():
    """Testa verificação de vencedor quando não há"""
    print("-----")
    print("Testando: verificar vencedor sem vencedor")
    print("-----")
    jogo = Jogo()
    jogo.iniciar_jogo(criar_config_jogadores(3))
    
    vencedor = jogo.verificar_vencedor()
    assert vencedor is None


def test_verificar_vencedor_com_vencedor():
    """Testa verificação de vencedor quando há um"""
    print("-----")
    print("Testando: verificar vencedor com vencedor")
    print("-----")
    jogo = Jogo()
    jogo.iniciar_jogo(criar_config_jogadores(3))
    
    jogo.jogadores[0].dinheiro = 1000
    jogo.jogadores[1].dinheiro = 0
    jogo.jogadores[2].dinheiro = 0
    
    vencedor = jogo.verificar_vencedor()
    assert vencedor == jogo.jogadores[0]

def test_finalizar_jogo():
    """Testa finalização do jogo"""
    print("-----")
    print("Testando: finalizar jogo")
    print("-----")
    jogo = Jogo()
    obs = ObservadorTeste()
    
    jogo.adicionar_observador(obs)
    jogo.iniciar_jogo(criar_config_jogadores(2))
    jogo.jogadores[1].dinheiro = 0
    jogo.finalizar_jogo()
    
    assert jogo.esta_ativo() == False
    eventos_faliu = [e for e in obs.eventos if e.tipo == TipoEvento.JOGADOR_FALIU]
    assert len(eventos_faliu) > 0

def test_executar_turno_publica_eventos():
    """Testa se executar turno publica eventos"""
    print("-----")
    print("Testando: executar turno publica eventos")
    print("-----")
    jogo = Jogo()
    obs = ObservadorTeste()
    
    jogo.adicionar_observador(obs)
    jogo.iniciar_jogo(criar_config_jogadores(2))
    
    eventos_iniciais = len(obs.eventos)
    jogo.executar_turno()
    
    assert len(obs.eventos) > eventos_iniciais

def test_executar_turno_sem_iniciar():
    """Testa erro ao executar turno sem iniciar jogo"""
    print("-----")
    print("Testando: executar turno sem iniciar")
    print("-----")
    jogo = Jogo()
    
    try:
        jogo.executar_turno()
        assert False, "Deveria ter lançado RuntimeError"
    except RuntimeError as e:
        assert "não foi iniciado" in str(e)

test_jogo_inicializacao()
test_iniciar_jogo_com_jogadores()
test_iniciar_jogo_distribui_dinheiro()
test_iniciar_jogo_minimo_jogadores()
test_adicionar_observador()
test_remover_observador()
test_proximo_turno()
test_proximo_turno_rotacao_circular()
test_verificar_vencedor_sem_vencedor()
test_verificar_vencedor_com_vencedor()
test_finalizar_jogo()
test_executar_turno_publica_eventos()
test_executar_turno_sem_iniciar()