from config import Config
import pygame

class TabuleiroUI:
    def __init__(self, jogo):
        pygame.init()
        self.jogo = jogo
        self.tela = pygame.display.set_mode((Config.LARGURA_TELA, Config.ALTURA_TELA))
        pygame.display.set_caption("Monopoly Uffiano - Pygame")
        self.relogio = pygame.time.Clock()

    def desenhar_tabuleiro(self):
        self.tela.fill(Config.BRANCO)

        tab_rect = pygame.Rect(
            Config.POS_X_INICIO,
            Config.POS_Y_INICIO,
            Config.TAMANHO_TABULEIRO,
            Config.TAMANHO_TABULEIRO,
        )
        pygame.draw.rect(self.tela, Config.CINZA_CLARO, tab_rect)
        pygame.draw.rect(self.tela, Config.PRETO, tab_rect, 3)

        miolo_tam = Config.TAMANHO_TABULEIRO - 2 * Config.TAMANHO_CASA_CANTO
        miolo_x = Config.POS_X_INICIO + Config.TAMANHO_CASA_CANTO
        miolo_y = Config.POS_Y_INICIO + Config.TAMANHO_CASA_CANTO
        miolo_rect = pygame.Rect(miolo_x, miolo_y, miolo_tam, miolo_tam)
        pygame.draw.rect(self.tela, Config.BRANCO, miolo_rect)
        pygame.draw.rect(self.tela, Config.PRETO, miolo_rect, 1)

        cantos = [
            (Config.POS_X_INICIO, Config.POS_Y_INICIO),
            (Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO, Config.POS_Y_INICIO),
            (Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO,
             Config.POS_Y_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO),
            (Config.POS_X_INICIO, Config.POS_Y_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO)
        ]
        for x, y in cantos:
            rect = pygame.Rect(x, y, Config.TAMANHO_CASA_CANTO, Config.TAMANHO_CASA_CANTO)
            pygame.draw.rect(self.tela, Config.VERMELHO, rect)
            pygame.draw.rect(self.tela, Config.PRETO, rect, 1)

        for i in range(1, 10):
            x = Config.POS_X_INICIO + Config.TAMANHO_CASA_CANTO + (i - 1) * Config.TAMANHO_CASA_PEQUENA
            y = Config.POS_Y_INICIO
            rect = pygame.Rect(x, y, Config.TAMANHO_CASA_PEQUENA, Config.TAMANHO_CASA_CANTO)
            pygame.draw.rect(self.tela, Config.CINZA_CLARO, rect)
            pygame.draw.rect(self.tela, Config.PRETO, rect, 1)

        for i in range(1, 10):
            x = Config.POS_X_INICIO
            y = Config.POS_Y_INICIO + Config.TAMANHO_CASA_CANTO + (i - 1) * Config.TAMANHO_CASA_PEQUENA
            rect = pygame.Rect(x, y, Config.TAMANHO_CASA_CANTO, Config.TAMANHO_CASA_PEQUENA)
            pygame.draw.rect(self.tela, Config.CINZA_CLARO, rect)
            pygame.draw.rect(self.tela, Config.PRETO, rect, 1)

        for i in range(1, 10):
            x = Config.POS_X_INICIO + Config.TAMANHO_CASA_CANTO + (i - 1) * Config.TAMANHO_CASA_PEQUENA
            y = Config.POS_Y_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO
            rect = pygame.Rect(x, y, Config.TAMANHO_CASA_PEQUENA, Config.TAMANHO_CASA_CANTO)
            pygame.draw.rect(self.tela, Config.CINZA_CLARO, rect)
            pygame.draw.rect(self.tela, Config.PRETO, rect, 1)

        for i in range(1, 10):
            x = Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO
            y = Config.POS_Y_INICIO + Config.TAMANHO_CASA_CANTO + (9 - i) * Config.TAMANHO_CASA_PEQUENA
            rect = pygame.Rect(x, y, Config.TAMANHO_CASA_CANTO, Config.TAMANHO_CASA_PEQUENA)
            pygame.draw.rect(self.tela, Config.CINZA_CLARO, rect)
            pygame.draw.rect(self.tela, Config.PRETO, rect, 1)