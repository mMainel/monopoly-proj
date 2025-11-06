import pygame
from config import Config

class JogadoresUI:
    def __init__(self, tela, jogadores):
        self.tela = tela
        self.jogadores = jogadores
    
    def desenhar_jogadores(self):
        """Desenha todos os jogadores no tabuleiro"""
        for i, jogador in enumerate(self.jogadores):
            if i < 8:
                self.desenhar_jogador(jogador, i)
    
    def desenhar_jogador(self, jogador, indice_jogador):
        """
        Desenha um jogador específico no tabuleiro.
        """
        if indice_jogador >= 8:
            return
            
        cor = Config.CORES_JOGADORES[indice_jogador % len(Config.CORES_JOGADORES)]
        
        # Usa a posição inicial da casa de partida
        pos_x, pos_y = Config.POSICAO_INICIAL_JOGADORES[indice_jogador]
        
        raio = Config.RAIO_JOGADOR * 0.5
        
        # Desenha o círculo do jogador
        pygame.draw.circle(self.tela, cor, (int(pos_x), int(pos_y)), int(raio))
        pygame.draw.circle(self.tela, Config.PRETO, (int(pos_x), int(pos_y)), int(raio), 1)
        
        # Número do jogador
        fonte = pygame.font.SysFont(None, 16)
        texto = fonte.render(str(indice_jogador + 1), True, Config.BRANCO)
        texto_rect = texto.get_rect(center=(int(pos_x), int(pos_y)))
        self.tela.blit(texto, texto_rect)