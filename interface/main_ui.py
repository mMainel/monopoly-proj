import pygame
from interface.tabuleiro_ui import TabuleiroUI 
from interface.painel_jogadores_ui import PainelJogadoresUI
from interface.jogadores_ui import JogadoresUI
from interface.botao_dado_ui import BotaoDadoUI  # Importa o botão

def main_ui(jogo):
    """
    Inicializa a interface gráfica e executa o loop principal do Pygame.
    Recebe a instância 'jogo' criada na main (main.py).
    """
    # inicializa pygame (TabuleiroUI também chama pygame.init(), mas chamar aqui é OK)
    pygame.init()

    tabuleiro = TabuleiroUI(jogo)
    painel = PainelJogadoresUI(tabuleiro.tela, jogo.jogadores)
    jogadores_ui = JogadoresUI(tabuleiro.tela, jogo.jogadores)
    botao_dado = BotaoDadoUI(tabuleiro.tela, jogo)  # Instancia o botão

    rodando = True
    while rodando:
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            # Passa eventos para o botão
            botao_dado.handle_event(evento)

        # Desenhar
        tabuleiro.desenhar_tabuleiro()
        jogadores_ui.desenhar_jogadores()  # Desenha os jogadores
        painel.desenhar()
        botao_dado.desenhar()  # Desenha o botão

        # Atualizar tela
        pygame.display.flip()
        tabuleiro.relogio.tick(60)

    pygame.quit()