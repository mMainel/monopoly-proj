import pygame
import os
from config import Config

class DadoUI:
    def __init__(self, tela):
        self.tela = tela
        self.visivel = False
        self.sprites = []
        self.dado1_val = 1
        self.dado2_val = 1

        self.tamanho_dado = int(Config.TAMANHO_TABULEIRO * 0.10) 
        
      

        board_end_x = Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO

       
        largura_tela = Config.LARGURA_TELA
        proporcao_painel = 0.30 
        margem_painel = 16       
        largura_painel_calc = max(240, int(largura_tela * proporcao_painel))
        largura_painel_calc = min(int(largura_tela * 0.45), largura_painel_calc)
        panel_start_x = largura_tela - largura_painel_calc - margem_painel

        
        gap_width = panel_start_x - board_end_x
        centro_gap_x = board_end_x + (gap_width // 2)

        
        centro_tabuleiro_y = Config.POS_Y_INICIO + (Config.TAMANHO_TABULEIRO // 2)
        
        
        espacamento = int(self.tamanho_dado * 0.15)
        self.pos_dado1 = (
            centro_gap_x - self.tamanho_dado - espacamento,
            centro_tabuleiro_y - (self.tamanho_dado // 2) 
        )
        self.pos_dado2 = (
            centro_gap_x + espacamento,
            centro_tabuleiro_y - (self.tamanho_dado // 2) 
        )
      
        try:
            caminho_base = os.path.dirname(__file__)
            caminho_raiz = os.path.join(caminho_base, '..')
            caminho_dados = os.path.join(caminho_raiz, 'assets', 'dados')
            
            for i in range(1, 7):
                img_path = os.path.join(caminho_dados, f"{i}.png")
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.smoothscale(img, (self.tamanho_dado, self.tamanho_dado))
                self.sprites.append(img)
                
        except Exception as e:
            print(f"Erro ao carregar sprites dos dados: {e}")
            self.sprites = [pygame.Surface((self.tamanho_dado, self.tamanho_dado)) for _ in range(6)]

    def set_resultado(self, dado1, dado2):
        self.dado1_val = dado1
        self.dado2_val = dado2

    def mostrar(self):
        self.visivel = True

    def esconder(self):
        self.visivel = False

    def desenhar(self):
        if not self.visivel:
            return
        
        self.tela.blit(self.sprites[self.dado1_val - 1], self.pos_dado1)
        self.tela.blit(self.sprites[self.dado2_val - 1], self.pos_dado2)