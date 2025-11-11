import pygame
from config import Config
from modules.peca import Peca

class JogadoresUI:
    def __init__(self, tela, jogadores, tabuleiro_ui):
        self.tela = tela
        self.jogadores = jogadores
        self.tabuleiro_ui = tabuleiro_ui

    def desenhar_jogadores(self):
        for i, jogador in enumerate(self.jogadores):
            if i < 8:
                self.desenhar_jogador(jogador, i)

    def desenhar_jogador(self, jogador, indice_jogador):
        if indice_jogador >= 8:
            return

        peca = jogador.getPeca() 
        cor = Config.CORES_PECAS.get(peca, Config.PRETO)
        #cor = Config.CORES_JOGADORES[indice_jogador % len(Config.CORES_JOGADORES)]

        numero_casa = jogador.getPosicao()
        pos_x, pos_y = self.calcular_posicao_jogador(numero_casa)

        raio = Config.RAIO_JOGADOR * 0.5

        pygame.draw.circle(self.tela, cor, (int(pos_x), int(pos_y)), int(raio))
        pygame.draw.circle(self.tela, Config.PRETO, (int(pos_x), int(pos_y)), int(raio), 1)

        fonte = pygame.font.SysFont(None, 16)
        texto = fonte.render(str(indice_jogador + 1), True, Config.BRANCO)
        texto_rect = texto.get_rect(center=(int(pos_x), int(pos_y)))
        self.tela.blit(texto, texto_rect)

    def calcular_posicao_jogador(self, numero_casa):
        deslocamento = Config.TAMANHO_CASA_PEQUENA

        x_inicial = Config.POS_X_INICIO
        y_inicial = Config.POS_Y_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO

        ajuste_pequeno = Config.TAMANHO_CASA_PEQUENA // 2
        ajuste_canto = Config.TAMANHO_CASA_CANTO // 2

        if numero_casa == 0:
            pos_x = x_inicial + ajuste_canto
            pos_y = y_inicial + ajuste_canto

        elif 1 <= numero_casa <= 9:
            pos_x = x_inicial + ajuste_canto
            pos_y = y_inicial - (numero_casa) * deslocamento + ajuste_pequeno

        elif numero_casa == 10:
            pos_x = x_inicial + ajuste_canto
            pos_y = Config.POS_Y_INICIO + ajuste_canto

        elif 11 <= numero_casa <= 19:
            pos_x = x_inicial + Config.TAMANHO_CASA_CANTO + (numero_casa - 11) * deslocamento + ajuste_pequeno
            pos_y = Config.POS_Y_INICIO + ajuste_canto

        elif numero_casa == 20:
            pos_x = Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO - ajuste_canto
            pos_y = Config.POS_Y_INICIO + ajuste_canto

        elif 21 <= numero_casa <= 29:
            pos_x = Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO - ajuste_canto
            pos_y = Config.POS_Y_INICIO + Config.TAMANHO_CASA_CANTO + (numero_casa - 21) * deslocamento + ajuste_pequeno

        elif numero_casa == 30:
            pos_x = Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO - ajuste_canto
            pos_y = y_inicial + ajuste_canto

        elif 31 <= numero_casa <= 39:
            pos_x = x_inicial + Config.TAMANHO_CASA_CANTO + (9 - (numero_casa - 30)) * deslocamento + ajuste_pequeno
            pos_y = y_inicial + ajuste_canto

        else:
            pos_x = x_inicial + ajuste_canto
            pos_y = y_inicial + ajuste_canto

        return pos_x, pos_y