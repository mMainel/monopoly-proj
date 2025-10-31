from typing import List
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.dados import Dados
from modules.regras import Regras
from modules.eventoJogo import EventoJogo, TipoEvento
from modules.observador import Observador

class Jogo:
    """
    Classe principal que orquestra o fluxo do jogo Monopoly
    """
    def __init__(self):
        self.tabuleiro: object = None
        self.jogadores: List[object] = []
        self.jogadorAtual: object = None
        self.banco: object = None
        self.dados: Dados = Dados()
        self.turno: int = 0
        
        self._observadores: List[Observador] = []
        self._regras: Regras = Regras()
        self._contador_duplas: int = 0
        self._jogo_ativo: bool = False
    
    def adicionar_observador(self, observador: Observador) -> None:
        """
        Adiciona um observador para receber eventos do jogo
        """
        self._observadores.append(observador)
    
    def remover_observador(self, observador: Observador) -> None:
        """
        Remove um observador da lista de notificações
        """
        if observador in self._observadores:
            self._observadores.remove(observador)
    
    def _publicar_evento(self, tipo: TipoEvento, dados: dict) -> None:
        """
        Publica um evento para todos os observadores
        """
        evento = EventoJogo(tipo=tipo, dados=dados)
        for observador in self._observadores:
            observador.notificar(evento)
    
    def iniciar_jogo(self, numero_jogadores: int) -> None:
        """
        Inicializa o jogo com o número de jogadores
        """
        if numero_jogadores < 2:
            raise ValueError("O jogo precisa de pelo menos 2 jogadores")
        
        self.jogadores = []
        for i in range(numero_jogadores):
            jogador = type('Jogador', (), {
                'id': i,
                'dinheiro': self._regras.obter_saldo_inicial(),
                'posicao': 0,
                'preso': False,
                'propriedades': []
            })()
            self.jogadores.append(jogador)
        
        self.jogadorAtual = self.jogadores[0]
        self.turno = 1
        self._jogo_ativo = True
        
        self._publicar_evento(TipoEvento.TURNO_INICIADO, {
            'turno': self.turno,
            'jogador': self.jogadorAtual
        })
    
    def executar_turno(self) -> None:
        """
        Executa um turno completo do jogador atual
        """
        if not self._jogo_ativo:
            raise RuntimeError("O jogo não foi iniciado")
        
        self._publicar_evento(TipoEvento.TURNO_INICIADO, {
            'turno': self.turno,
            'jogador': self.jogadorAtual
        })
        
        resultado_dados = self.dados.lancar()
        soma = self.dados.soma_dados()
        
        self._publicar_evento(TipoEvento.DADOS_LANCADOS, {
            'jogador': self.jogadorAtual,
            'dados': resultado_dados,
            'soma': soma
        })
        
        if self.dados.isDupla():
            self._contador_duplas += 1
            self._publicar_evento(TipoEvento.DUPLA_LANCADA, {
                'jogador': self.jogadorAtual,
                'contador_duplas': self._contador_duplas
            })
            
            if self._contador_duplas >= self._regras.obter_max_duplas():
                self._enviar_para_prisao(self.jogadorAtual)
                self.proximo_turno()
                return
        else:
            self._contador_duplas = 0
        
        self._mover_jogador(self.jogadorAtual, soma)
        
        if not self.dados.isDupla():
            self.proximo_turno()
    
    def proximo_turno(self) -> None:
        """
        Avança para o próximo jogador
        """
        self._publicar_evento(TipoEvento.TURNO_FINALIZADO, {
            'turno': self.turno,
            'jogador': self.jogadorAtual
        })
        
        self._contador_duplas = 0
        
        indice_atual = self.jogadores.index(self.jogadorAtual)
        proximo_indice = (indice_atual + 1) % len(self.jogadores)
        self.jogadorAtual = self.jogadores[proximo_indice]
        
        if proximo_indice == 0:
            self.turno += 1
    
    def _mover_jogador(self, jogador: object, casas: int) -> None:
        """
        Move o jogador no tabuleiro e processa a casa de destino
        """
        posicao_anterior = jogador.posicao
        jogador.posicao = (jogador.posicao + casas) % 40
        
        if jogador.posicao < posicao_anterior:
            self._processar_passagem_inicio(jogador)
        
        self._publicar_evento(TipoEvento.JOGADOR_MOVEU, {
            'jogador': jogador,
            'posicao_anterior': posicao_anterior,
            'posicao_nova': jogador.posicao,
            'casas': casas
        })
    
    def _processar_passagem_inicio(self, jogador: object) -> None:
        """
        Processa quando jogador passa pelo Início
        """
        salario = self._regras.obter_salario_inicio()
        jogador.dinheiro += salario
        
        self._publicar_evento(TipoEvento.PASSOU_INICIO, {
            'jogador': jogador,
            'valor': salario
        })
    
    def _enviar_para_prisao(self, jogador: object) -> None:
        """
        Envia jogador para a prisão
        """
        jogador.posicao = 10
        jogador.preso = True
        
        self._publicar_evento(TipoEvento.JOGADOR_PRESO, {
            'jogador': jogador,
            'motivo': 'tres_duplas'
        })
    
    def verificar_vencedor(self) -> object:
        """
        Verifica se há um vencedor
        """
        jogadores_ativos = [j for j in self.jogadores if j.dinheiro > 0]
        
        if len(jogadores_ativos) == 1:
            return jogadores_ativos[0]
        
        return None
    
    def finalizar_jogo(self) -> None:
        """
        Finaliza o jogo
        """
        vencedor = self.verificar_vencedor()
        self._jogo_ativo = False
        
        self._publicar_evento(TipoEvento.JOGADOR_FALIU, {
            'vencedor': vencedor,
            'turno_final': self.turno
        })
    
    def esta_ativo(self) -> bool:
        """
        Verifica se o jogo está ativo
        """
        return self._jogo_ativo