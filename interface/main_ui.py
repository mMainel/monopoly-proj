import pygame
from interface.tabuleiro_ui import TabuleiroUI
from interface.painel_jogadores_ui import PainelJogadoresUI
from interface.jogadores_ui import JogadoresUI
from interface.botao_dado_ui import BotaoDadoUI
from interface.evento_ui import EventoUI, DialogoCompraUI, DialogoInfoPropriedadeUI, PopupEventosUI
from interface.dialogo_cadeia_ui import DialogoOpcoesCadeiaUI
from turno import executar_turno_com_ui
from interface.dado_ui import DadoUI
from modules.observador import Observador
from modules.eventoJogo import TipoEvento
from interface.negociacao_ui import (
    DialogoEscolherJogadorUI,
    DialogoNegociacaoUI,
    DialogoConfirmacaoUI,
    DialogoMenuFimTurnoUI,
    DialogoGerenciarPropriedadesUI,
)
from interface.leilao_ui import DialogoLeilaoUI


class ObservadorUI(Observador):
    """
    Observador que traduz eventos do jogo para mensagens na UI.
    ATUALIZADO: Inclui handlers para eventos de cartas
    """
    def __init__(self, evento_ui, dado_ui, popup_ui=None):
        self.evento_ui = evento_ui
        self.dado_ui = dado_ui
        self.popup_ui = popup_ui
    
    def notificar(self, evento):
        tipo = evento.tipo
        dados = evento.dados
        
        handlers = {
            TipoEvento.DADOS_LANCADOS: self._handle_dados_lancados,
            TipoEvento.JOGADOR_MOVEU: self._handle_jogador_moveu,
            TipoEvento.PASSOU_INICIO: self._handle_passou_inicio,
            TipoEvento.PROPRIEDADE_COMPRADA: self._handle_propriedade_comprada,
            TipoEvento.ALUGUEL_PAGO: self._handle_aluguel_pago,
            TipoEvento.DUPLA_LANCADA: self._handle_dupla_lancada,
            TipoEvento.JOGADOR_PRESO: self._handle_jogador_preso,
            TipoEvento.SAIU_CADEIA: self._handle_saiu_cadeia,
            TipoEvento.CONSTRUCAO_FEITA: self._handle_construcao_feita,
            TipoEvento.PROPRIEDADE_HIPOTECADA: self._handle_propriedade_hipotecada,
            TipoEvento.PROPRIEDADE_DESHIPOTECADA: self._handle_propriedade_deshipotecada,
            TipoEvento.LEILAO_FINALIZADO: self._handle_leilao_finalizado,
            TipoEvento.JOGADOR_FALIU: self._handle_jogador_faliu,
            TipoEvento.CARTA_SORTE_PEGA: self._handle_carta_sorte_pega,
            TipoEvento.CARTA_COFRE_PEGA: self._handle_carta_cofre_pega,
            TipoEvento.JOGADOR_RECEBEU_DINHEIRO: self._handle_jogador_recebeu_dinheiro,
            TipoEvento.JOGADOR_PAGOU_TAXA: self._handle_jogador_pagou_taxa,
            TipoEvento.JOGADOR_RECEBEU_CARTA_SAIR_CADEIA: self._handle_carta_sair_cadeia,
        }
        
        handler = handlers.get(tipo)
        if handler:
            handler(dados)
    
    
    def _handle_dados_lancados(self, dados):
        dados_valores = dados.get('dados', (1, 1))
        self.dado_ui.set_resultado(dados_valores[0], dados_valores[1])
        self.dado_ui.mostrar()
    
    def _handle_jogador_moveu(self, dados):
        jogador = dados.get('jogador')
        casas = dados.get('casas', 0)
        pos_nova = dados.get('posicao_nova')
        if jogador and casas:
            self.evento_ui.adicionar_evento(f"{jogador.getNome()} andou {casas} casas")
        # Popups especiais por casa
        try:
            if self.popup_ui is not None and isinstance(pos_nova, int):
                if pos_nova == 30:
                    self.popup_ui.mostrar(f"{jogador.getNome()} foi para a Cadeia! 🚔")
                elif pos_nova == 20:
                    self.popup_ui.mostrar("Estacionamento Gratuito 🅿️")
        except Exception:
            pass
    
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
            # Monta mensagem completa conforme solicitado, incluindo o curso/peça do recebedor
            peca_recv = None
            try:
                peca = recebedor.getPeca()
                peca_recv = peca.value if hasattr(peca, 'value') else str(peca)
            except Exception:
                peca_recv = None
            msg = (
                f"{pagador.getNome()} pagou R$ {valor} de aluguel para {recebedor.getNome()}"
                + (f" ({peca_recv})" if peca_recv else "")
            )
            self.evento_ui.adicionar_evento(msg)
            if getattr(self, 'popup_ui', None):
                try:
                    # No popup, usamos a mesma mensagem do feed
                    self.popup_ui.mostrar(msg)
                except Exception:
                    pass

    def _handle_dupla_lancada(self, dados):
        jogador = dados.get('jogador')
        contador = dados.get('contador_duplas', 1)
        if jogador:
            base = f"🎲 Dupla! {jogador.getNome()} joga novamente"
            if contador >= 3:
                # Já deve ter sido tratado em outro handler (prisão), mas registramos destaque
                base = f"🚔 {jogador.getNome()} tirou 3 duplas e foi para a cadeia"
            self.evento_ui.adicionar_evento(base)
            if getattr(self, 'popup_ui', None):
                try:
                    if contador < 3:
                        self.popup_ui.mostrar("Dupla! Joga de novo")
                    else:
                        self.popup_ui.mostrar("3 Duplas! Vai para a cadeia")
                except Exception:
                    pass
    
    def _handle_jogador_preso(self, dados):
        jogador = dados.get('jogador')
        if jogador:
            msg = f"{jogador.getNome()} foi preso!"
            self.evento_ui.adicionar_evento(msg)
            if getattr(self, 'popup_ui', None):
                self.popup_ui.mostrar("Foi para a Cadeia! 🚔")
    
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

    def _handle_propriedade_deshipotecada(self, dados):
        jogador = dados.get('jogador')
        prop = dados.get('propriedade')
        valor = dados.get('valor', 0)
        if jogador and prop:
            nome_prop = prop.getNome() if hasattr(prop, 'getNome') else 'Propriedade'
            self.evento_ui.adicionar_evento(f"{jogador.getNome()} deshipotecou {nome_prop} (R${valor})")
    
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
    
    
    def _handle_carta_sorte_pega(self, dados):
        """Quando jogador pega uma carta Sorte"""
        jogador = dados.get('jogador')
        descricao = dados.get('descricao', 'Carta Sorte')
        
        if jogador:
            # Mostrar que pegou a carta com emoji
            msg = f"🎴 {jogador.getNome()} pegou: {descricao}"
            self.evento_ui.adicionar_evento(msg)
            if getattr(self, 'popup_ui', None):
                self.popup_ui.mostrar(descricao)
    
    def _handle_carta_cofre_pega(self, dados):
        """Quando jogador pega uma carta Cofre Comunitário"""
        jogador = dados.get('jogador')
        descricao = dados.get('descricao', 'Carta Cofre')
        
        if jogador:
            # Mostrar que pegou a carta com emoji
            msg = f"💰 {jogador.getNome()} pegou: {descricao}"
            self.evento_ui.adicionar_evento(msg)
            if getattr(self, 'popup_ui', None):
                self.popup_ui.mostrar(descricao)
    
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
                msg = f"💸 {jogador.getNome()} pagou R${valor} ({motivo})"
                self.evento_ui.adicionar_evento(msg)
                if getattr(self, 'popup_ui', None):
                    self.popup_ui.mostrar(f"Pagou R$ {valor} - {motivo}")
            else:
                msg = f"💸 {jogador.getNome()} pagou R${valor}"
                self.evento_ui.adicionar_evento(msg)
                if getattr(self, 'popup_ui', None):
                    self.popup_ui.mostrar(f"Pagou R$ {valor}")
    
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
    popup_eventos = PopupEventosUI(tabuleiro.tela)
    dialogo_compra = DialogoCompraUI(tabuleiro.tela)
    dialogo_info_prop = DialogoInfoPropriedadeUI(tabuleiro.tela)
    dado_ui = DadoUI(tabuleiro.tela)
    dialogo_cadeia = DialogoOpcoesCadeiaUI(tabuleiro.tela)
    dialogo_escolher = DialogoEscolherJogadorUI(tabuleiro.tela)
    dialogo_negociacao = DialogoNegociacaoUI(tabuleiro.tela)
    dialogo_confirmar = DialogoConfirmacaoUI(tabuleiro.tela)
    dialogo_leilao = DialogoLeilaoUI(tabuleiro.tela)
    dialogo_menu = DialogoMenuFimTurnoUI(tabuleiro.tela)
    dialogo_gerenciar = DialogoGerenciarPropriedadesUI(tabuleiro.tela)
    
    # ===== REGISTRAR OBSERVADOR =====
    observador_ui = ObservadorUI(evento_ui, dado_ui, popup_eventos)
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
            dialogo_info_prop.handle_event(evento)
            # Clique no tabuleiro para abrir info da propriedade
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if not dialogo_compra.ativo and not dialogo_cadeia.ativo and not dialogo_info_prop.ativo:
                    idx = tabuleiro.get_posicao_por_ponto(evento.pos)
                    if idx is not None:
                        try:
                            espaco = jogo.tabuleiro.getEspaco(idx)
                            from modules.espaco import EspacoPropriedade
                            if isinstance(espaco, EspacoPropriedade):
                                titulo = espaco.getTitulo()
                                dialogo_info_prop.mostrar(titulo)
                        except Exception:
                            pass
            
            # Botão de dado só responde se não houver diálogos ativos
            if not dialogo_compra.ativo and not dialogo_cadeia.ativo:
                botao_dado.handle_event(evento)

        # Verificar se é turno da IA e executar automaticamente
        from modules.jogadorIA import JogadorIA
        jogador_atual = jogo.jogadorAtual
        if isinstance(jogador_atual, JogadorIA) and not turno_em_andamento:
            # IA joga automaticamente - pequeno delay para visualização
            pygame.time.wait(500)
            turno_em_andamento = True
            botao_dado.desabilitar()
            
            try:
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
                    "dialogo_leilao": dialogo_leilao,
                    "dialogo_menu": dialogo_menu,
                    "dialogo_gerenciar": dialogo_gerenciar,
                    "popup_eventos": popup_eventos,
                }
                executar_turno_com_ui(jogo, jogador_atual, dialogo_compra, elementos_ui, dialogo_cadeia)
                
                # Verificar vencedor
                vencedor = jogo.verificar_vencedor()
                if vencedor:
                    evento_ui.adicionar_evento(f"🏆 {vencedor.getNome()} VENCEU! 🏆")
                    pygame.time.wait(3000)
                    rodando = False
                
            except Exception as e:
                print(f"Erro ao executar turno da IA: {e}")
                import traceback
                traceback.print_exc()
            
            finally:
                turno_em_andamento = False
                botao_dado.habilitar()

        # Executar turno quando botão clicado (jogador humano)
        elif botao_dado.foi_clicado() and not turno_em_andamento and not dialogo_compra.ativo and not dialogo_cadeia.ativo:
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
                    "dialogo_leilao": dialogo_leilao,
                    "dialogo_menu": dialogo_menu,
                    "dialogo_gerenciar": dialogo_gerenciar,
                    "popup_eventos": popup_eventos,
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
        
        # Só desenha botão de dados se for turno de jogador humano
        if not isinstance(jogo.jogadorAtual, JogadorIA):
            botao_dado.desenhar()
        
        dado_ui.desenhar()
        dialogo_compra.desenhar()
        dialogo_cadeia.desenhar()
        dialogo_info_prop.desenhar()
        popup_eventos.desenhar()
        
        pygame.display.flip()
        tabuleiro.relogio.tick(60)

    pygame.quit()