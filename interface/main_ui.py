import pygame
from interface.tabuleiro_ui import TabuleiroUI
from interface.painel_jogadores_ui import PainelJogadoresUI
from interface.jogadores_ui import JogadoresUI
from interface.botao_dado_ui import BotaoDadoUI
from interface.evento_ui import EventoUI, DialogoCompraUI
from interface.dialogo_cadeia_ui import DialogoOpcoesCadeiaUI
from turno import executar_turno_com_ui
from modules.observador import Observador
from modules.eventoJogo import TipoEvento

def main_ui(jogo):
    pygame.init()

    tabuleiro = TabuleiroUI(jogo)
    painel = PainelJogadoresUI(tabuleiro.tela, jogo.jogadores)
    jogadores_ui = JogadoresUI(tabuleiro.tela, jogo.jogadores)
    botao_dado = BotaoDadoUI(tabuleiro.tela, jogo)
    evento_ui = EventoUI(tabuleiro.tela)
    dialogo_compra = DialogoCompraUI(tabuleiro.tela)
    dialogo_cadeia = DialogoOpcoesCadeiaUI(tabuleiro.tela)
    
    class ObservadorUI(Observador):
        def __init__(self, evento_ui):
            self.evento_ui = evento_ui
        
        def notificar(self, evento):
            tipo = evento.tipo
            dados = evento.dados
            
            if tipo == TipoEvento.JOGADOR_MOVEU:
                jogador = dados.get('jogador')
                casas = dados.get('casas', 0)
                if jogador and casas:
                    self.evento_ui.adicionar_evento(f"{jogador.getNome()} andou {casas} casas")
            
            elif tipo == TipoEvento.PASSOU_INICIO:
                jogador = dados.get('jogador')
                if jogador:
                    self.evento_ui.adicionar_evento(f"{jogador.getNome()} recebeu R$200")
            
            elif tipo == TipoEvento.PROPRIEDADE_COMPRADA:
                jogador = dados.get('jogador')
                prop = dados.get('propriedade')
                valor = dados.get('valor', 0)
                if jogador and prop:
                    nome_prop = prop.getNome() if hasattr(prop, 'getNome') else 'Propriedade'
                    self.evento_ui.adicionar_evento(f"{jogador.getNome()} comprou {nome_prop} (R${valor})")
            
            elif tipo == TipoEvento.ALUGUEL_PAGO:
                pagador = dados.get('pagador')
                recebedor = dados.get('recebedor')
                valor = dados.get('valor', 0)
                if pagador and recebedor:
                    self.evento_ui.adicionar_evento(f"{pagador.getNome()} pagou R${valor} a {recebedor.getNome()}")
            
            elif tipo == TipoEvento.JOGADOR_PRESO:
                jogador = dados.get('jogador')
                if jogador:
                    self.evento_ui.adicionar_evento(f"{jogador.getNome()} foi preso!")
            
            elif tipo == TipoEvento.SAIU_CADEIA:
                jogador = dados.get('jogador')
                metodo = dados.get('metodo', '')
                if jogador:
                    if metodo == 'dupla':
                        self.evento_ui.adicionar_evento(f"{jogador.getNome()} tirou dupla e saiu!")
                    elif metodo == 'fianca':
                        self.evento_ui.adicionar_evento(f"{jogador.getNome()} pagou fiança")
                    else:
                        self.evento_ui.adicionar_evento(f"{jogador.getNome()} saiu da cadeia")
            
            elif tipo == TipoEvento.CONSTRUCAO_FEITA:
                jogador = dados.get('jogador')
                prop = dados.get('propriedade')
                tipo_construcao = dados.get('tipo', 'casa')
                if jogador and prop:
                    nome_prop = prop.getNome() if hasattr(prop, 'getNome') else 'Propriedade'
                    if tipo_construcao == 'hotel':
                        self.evento_ui.adicionar_evento(f"{jogador.getNome()} construiu hotel em {nome_prop}")
                    else:
                        self.evento_ui.adicionar_evento(f"{jogador.getNome()} construiu casa em {nome_prop}")
            
            elif tipo == TipoEvento.PROPRIEDADE_HIPOTECADA:
                jogador = dados.get('jogador')
                prop = dados.get('propriedade')
                valor = dados.get('valor', 0)
                if jogador and prop:
                    nome_prop = prop.getNome() if hasattr(prop, 'getNome') else 'Propriedade'
                    self.evento_ui.adicionar_evento(f"{jogador.getNome()} hipotecou {nome_prop} (R${valor})")
            
            elif tipo == TipoEvento.LEILAO_FINALIZADO:
                vencedor = dados.get('vencedor')
                valor = dados.get('valor', 0)
                prop = dados.get('propriedade')
                if vencedor and prop:
                    nome_prop = prop.getNome() if hasattr(prop, 'getNome') else 'Propriedade'
                    self.evento_ui.adicionar_evento(f"{vencedor.getNome()} arrematou {nome_prop} por R${valor}")
            
            elif tipo == TipoEvento.JOGADOR_FALIU:
                jogador = dados.get('jogador')
                if jogador:
                    self.evento_ui.adicionar_evento(f"{jogador.getNome()} FALIU!")
    
    observador_ui = ObservadorUI(evento_ui)
    jogo.adicionar_observador(observador_ui)
    
    evento_ui.adicionar_evento(f"🎮 Jogo iniciado! Boa sorte!")

    rodando = True
    turno_em_andamento = False
    
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            dialogo_compra.handle_event(evento)
            dialogo_cadeia.handle_event(evento)
            
            if not dialogo_compra.ativo and not dialogo_cadeia.ativo:
                botao_dado.handle_event(evento)

        if botao_dado.foi_clicado() and not turno_em_andamento and not dialogo_compra.ativo and not dialogo_cadeia.ativo:
            try:
                turno_em_andamento = True
                botao_dado.desabilitar()
                
                jogador_atual = jogo.jogadorAtual
                
                executar_turno_com_ui(jogo, jogador_atual, dialogo_compra, evento_ui, dialogo_cadeia)
                
                vencedor = jogo.verificar_vencedor()
                if vencedor:
                    evento_ui.adicionar_evento(f"🏆 {vencedor.getNome()} VENCEU! 🏆")
                    pygame.time.wait(3000)
                    rodando = False
                
                turno_em_andamento = False
                botao_dado.habilitar()
                
            except Exception as e:
                print(f"Erro ao executar turno: {e}")
                import traceback
                traceback.print_exc()
                turno_em_andamento = False
                botao_dado.habilitar()

        tabuleiro.desenhar_tabuleiro()
        jogadores_ui.desenhar_jogadores()
        painel.desenhar()
        evento_ui.desenhar()
        botao_dado.desenhar()
        dialogo_compra.desenhar()
        dialogo_cadeia.desenhar()
        pygame.display.flip()
        tabuleiro.relogio.tick(60)

    pygame.quit()