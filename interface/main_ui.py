import pygame
from interface.tabuleiro_ui import TabuleiroUI
from interface.painel_jogadores_ui import PainelJogadoresUI
from interface.jogadores_ui import JogadoresUI
from interface.botao_dado_ui import BotaoDadoUI
from interface.evento_ui import EventoUI, DialogoCompraUI
from interface.dialogo_cadeia_ui import DialogoOpcoesCadeiaUI
from turno import executar_turno_com_ui
from interface.dado_ui import DadoUI
from modules.observador import Observador
from modules.eventoJogo import TipoEvento
from interface.negociacao_ui import DialogoEscolherJogadorUI, DialogoNegociacaoUI, DialogoConfirmacaoUI


class ObservadorUI(Observador):
    """
    Observador que traduz eventos do jogo para mensagens na UI.
    ATUALIZADO: Inclui handlers para eventos de cartas
    """
    def __init__(self, evento_ui, dado_ui):
        self.evento_ui = evento_ui
        self.dado_ui = dado_ui
    
    def notificar(self, evento):
        tipo = evento.tipo
        dados = evento.dados
        
        # Dicionário de handlers por tipo de evento
        handlers = {
            # Eventos originais
            TipoEvento.DADOS_LANCADOS: self._handle_dados_lancados,
            TipoEvento.JOGADOR_MOVEU: self._handle_jogador_moveu,
            TipoEvento.PASSOU_INICIO: self._handle_passou_inicio,
            TipoEvento.PROPRIEDADE_COMPRADA: self._handle_propriedade_comprada,
            TipoEvento.ALUGUEL_PAGO: self._handle_aluguel_pago,
            TipoEvento.JOGADOR_PRESO: self._handle_jogador_preso,
            TipoEvento.SAIU_CADEIA: self._handle_saiu_cadeia,
            TipoEvento.CONSTRUCAO_FEITA: self._handle_construcao_feita,
            TipoEvento.PROPRIEDADE_HIPOTECADA: self._handle_propriedade_hipotecada,
            TipoEvento.LEILAO_FINALIZADO: self._handle_leilao_finalizado,
            TipoEvento.JOGADOR_FALIU: self._handle_jogador_faliu,
            
            # ===== NOVOS HANDLERS PARA CARTAS =====
            TipoEvento.CARTA_SORTE_PEGA: self._handle_carta_sorte_pega,
            TipoEvento.CARTA_COFRE_PEGA: self._handle_carta_cofre_pega,
            TipoEvento.JOGADOR_RECEBEU_DINHEIRO: self._handle_jogador_recebeu_dinheiro,
            TipoEvento.JOGADOR_PAGOU_TAXA: self._handle_jogador_pagou_taxa,
            TipoEvento.JOGADOR_RECEBEU_CARTA_SAIR_CADEIA: self._handle_carta_sair_cadeia,
        }
        
        handler = handlers.get(tipo)
        if handler:
            handler(dados)
    
    # ===== HANDLERS ORIGINAIS =====
    
    def _handle_dados_lancados(self, dados):
        dados_valores = dados.get('dados', (1, 1))
        self.dado_ui.set_resultado(dados_valores[0], dados_valores[1])
        self.dado_ui.mostrar()
    
    def _handle_jogador_moveu(self, dados):
        jogador = dados.get('jogador')
        casas = dados.get('casas', 0)
        if jogador and casas:
            self.evento_ui.adicionar_evento(f"{jogador.getNome()} andou {casas} casas")
    
    def _handle_passou_inicio(self, dados):
        jogador = dados.get('jogador')
        if jogador:
            self.evento_ui.adicionar_evento(f"{jogador.getNome()} recebeu R$200")
    
    def _handle_propriedade_comprada(self, dados):
        jogador = dados.get('jogador')
        prop = dados.get('propriedade')
        valor = dados.get('valor', 0)
        if jogador and prop:
            nome_prop = prop.getNome() if hasattr(prop, 'getNome') else 'Propriedade'
            self.evento_ui.adicionar_evento(f"{jogador.getNome()} comprou {nome_prop} (R${valor})")
    
    def _handle_aluguel_pago(self, dados):
        pagador = dados.get('pagador')
        recebedor = dados.get('recebedor')
        valor = dados.get('valor', 0)
        if pagador and recebedor:
            self.evento_ui.adicionar_evento(f"{pagador.getNome()} pagou R${valor} a {recebedor.getNome()}")
    
    def _handle_jogador_preso(self, dados):
        jogador = dados.get('jogador')
        if jogador:
            self.evento_ui.adicionar_evento(f"{jogador.getNome()} foi preso!")
    
    def _handle_saiu_cadeia(self, dados):
        jogador = dados.get('jogador')
        metodo = dados.get('metodo', '')
        if jogador:
            mensagens = {
                'dupla': f"{jogador.getNome()} tirou dupla e saiu!",
                'fianca': f"{jogador.getNome()} pagou fiança",
            }
            mensagem = mensagens.get(metodo, f"{jogador.getNome()} saiu da cadeia")
            self.evento_ui.adicionar_evento(mensagem)
    
    def _handle_construcao_feita(self, dados):
        jogador = dados.get('jogador')
        prop = dados.get('propriedade')
        tipo_construcao = dados.get('tipo', 'casa')
        if jogador and prop:
            nome_prop = prop.getNome() if hasattr(prop, 'getNome') else 'Propriedade'
            tipo_msg = 'hotel' if tipo_construcao == 'hotel' else 'casa'
            self.evento_ui.adicionar_evento(f"{jogador.getNome()} construiu {tipo_msg} em {nome_prop}")
    
    def _handle_propriedade_hipotecada(self, dados):
        jogador = dados.get('jogador')
        prop = dados.get('propriedade')
        valor = dados.get('valor', 0)
        if jogador and prop:
            nome_prop = prop.getNome() if hasattr(prop, 'getNome') else 'Propriedade'
            self.evento_ui.adicionar_evento(f"{jogador.getNome()} hipotecou {nome_prop} (R${valor})")
    
    def _handle_leilao_finalizado(self, dados):
        vencedor = dados.get('vencedor')
        valor = dados.get('valor', 0)
        prop = dados.get('propriedade')
        if vencedor and prop:
            nome_prop = prop.getNome() if hasattr(prop, 'getNome') else 'Propriedade'
            self.evento_ui.adicionar_evento(f"{vencedor.getNome()} arrematou {nome_prop} por R${valor}")
    
    def _handle_jogador_faliu(self, dados):
        jogador = dados.get('jogador')
        if jogador:
            self.evento_ui.adicionar_evento(f"{jogador.getNome()} FALIU!")
    
    # ===== NOVOS HANDLERS PARA CARTAS =====
    
    def _handle_carta_sorte_pega(self, dados):
        """Quando jogador pega uma carta Sorte"""
        jogador = dados.get('jogador')
        descricao = dados.get('descricao', 'Carta Sorte')
        
        if jogador:
            # Mostrar que pegou a carta com emoji
            self.evento_ui.adicionar_evento(f"🎴 {jogador.getNome()} pegou: {descricao}")
    
    def _handle_carta_cofre_pega(self, dados):
        """Quando jogador pega uma carta Cofre Comunitário"""
        jogador = dados.get('jogador')
        descricao = dados.get('descricao', 'Carta Cofre')
        
        if jogador:
            # Mostrar que pegou a carta com emoji
            self.evento_ui.adicionar_evento(f"💰 {jogador.getNome()} pegou: {descricao}")
    
    def _handle_jogador_recebeu_dinheiro(self, dados):
        """Quando jogador recebe dinheiro (carta, salário, etc)"""
        jogador = dados.get('jogador')
        valor = dados.get('valor', 0)
        motivo = dados.get('motivo', '')
        
        if jogador:
            if motivo:
                self.evento_ui.adicionar_evento(f"💵 {jogador.getNome()} recebeu R${valor} ({motivo})")
            else:
                self.evento_ui.adicionar_evento(f"💵 {jogador.getNome()} recebeu R${valor}")
    
    def _handle_jogador_pagou_taxa(self, dados):
        """Quando jogador paga taxa/imposto"""
        jogador = dados.get('jogador')
        valor = dados.get('valor', 0)
        motivo = dados.get('motivo', '')
        
        if jogador:
            if motivo:
                self.evento_ui.adicionar_evento(f"💸 {jogador.getNome()} pagou R${valor} ({motivo})")
            else:
                self.evento_ui.adicionar_evento(f"💸 {jogador.getNome()} pagou R${valor}")
    
    def _handle_carta_sair_cadeia(self, dados):
        """Quando jogador recebe carta 'Sair da Cadeia'"""
        jogador = dados.get('jogador')
        tipo_carta = dados.get('tipo_carta', 'sorte')
        
        if jogador:
            tipo_nome = "Sorte" if tipo_carta == 'sorte' else "Cofre"
            self.evento_ui.adicionar_evento(
                f"🔑 {jogador.getNome()} ganhou carta 'Sair da Cadeia' ({tipo_nome})"
            )


def main_ui(jogo):
    """
    Loop principal da interface gráfica
    """
    pygame.init()

    # ===== INICIALIZAR COMPONENTES DA UI =====
    tabuleiro = TabuleiroUI(jogo)
    painel = PainelJogadoresUI(tabuleiro.tela, jogo.jogadores)
    jogadores_ui = JogadoresUI(tabuleiro.tela, jogo.jogadores, tabuleiro)
    botao_dado = BotaoDadoUI(tabuleiro.tela, jogo)
    evento_ui = EventoUI(tabuleiro.tela)
    dialogo_compra = DialogoCompraUI(tabuleiro.tela)
    dado_ui = DadoUI(tabuleiro.tela)
    dialogo_cadeia = DialogoOpcoesCadeiaUI(tabuleiro.tela)
    dialogo_escolher = DialogoEscolherJogadorUI(tabuleiro.tela)
    dialogo_negociacao = DialogoNegociacaoUI(tabuleiro.tela)
    dialogo_confirmar = DialogoConfirmacaoUI(tabuleiro.tela)
    
    # ===== REGISTRAR OBSERVADOR =====
    observador_ui = ObservadorUI(evento_ui, dado_ui)
    jogo.adicionar_observador(observador_ui)
    
    # ===== MENSAGEM INICIAL =====
    evento_ui.adicionar_evento(f"🎮 Jogo iniciado! Boa sorte!")

    # ===== VARIÁVEIS DE CONTROLE =====
    rodando = True
    turno_em_andamento = False
    
    # ===== LOOP PRINCIPAL =====
    while rodando:
        # Processar eventos do Pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            # Diálogos têm prioridade
            dialogo_compra.handle_event(evento)
            dialogo_cadeia.handle_event(evento)
            
            # Botão de dado só responde se não houver diálogos ativos
            if not dialogo_compra.ativo and not dialogo_cadeia.ativo:
                botao_dado.handle_event(evento)

        # Executar turno quando botão clicado
        if botao_dado.foi_clicado() and not turno_em_andamento and not dialogo_compra.ativo and not dialogo_cadeia.ativo:
            turno_em_andamento = True
            botao_dado.desabilitar()
            
            try:
                jogador_atual = jogo.jogadorAtual
                
                elementos_ui = {
                    "tabuleiro": tabuleiro,
                    "jogadores_ui": jogadores_ui,
                    "painel": painel,
                    "evento_ui": evento_ui,
                    "botao_dado": botao_dado,
                    "dado_ui": dado_ui,
                    "dialogo_escolher": dialogo_escolher,
                    "dialogo_negociacao": dialogo_negociacao,
                    "dialogo_confirmar": dialogo_confirmar,
                }
                executar_turno_com_ui(jogo, jogador_atual, dialogo_compra, elementos_ui, dialogo_cadeia)
                
                # Verificar vencedor
                vencedor = jogo.verificar_vencedor()
                if vencedor:
                    evento_ui.adicionar_evento(f"🏆 {vencedor.getNome()} VENCEU! 🏆")
                    pygame.time.wait(3000)
                    rodando = False
                
            except Exception as e:
                print(f"Erro ao executar turno: {e}")
                import traceback
                traceback.print_exc()
            
            finally:
                turno_em_andamento = False
                botao_dado.habilitar()

        # Desenhar tudo
        tabuleiro.desenhar_tabuleiro()
        jogadores_ui.desenhar_jogadores()
        painel.desenhar()
        evento_ui.desenhar()
        botao_dado.desenhar()
        dado_ui.desenhar()
        dialogo_compra.desenhar()
        dialogo_cadeia.desenhar()
        
        pygame.display.flip()
        tabuleiro.relogio.tick(60)

    pygame.quit()