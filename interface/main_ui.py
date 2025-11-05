import pygame
from interface.tabuleiro_ui import TabuleiroUI 
from interface.painel_jogadores_ui import PainelJogadoresUI

def main_ui(jogo):
    """
    Inicializa a interface gráfica e executa o loop principal do Pygame.
    Recebe a instância 'jogo' criada na main (main.py).
    """
    # inicializa pygame (TabuleiroUI também chama pygame.init(), mas chamar aqui é OK)
    pygame.init()

    tabuleiro = TabuleiroUI(jogo)
    painel = PainelJogadoresUI(tabuleiro.tela, jogo.jogadores)

    rodando = True
    while rodando:
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            


        # Desenhar
        tabuleiro.desenhar_tabuleiro()
        painel.desenhar()

        # Atualizar tela
        pygame.display.flip()
        tabuleiro.relogio.tick(60)

    pygame.quit()
