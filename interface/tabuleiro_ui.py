from config import Config
import pygame
import os
from modules.tituloPropriedade import TituloPropriedade

class TabuleiroUI:
    def __init__(self, jogo):
        pygame.init()
        self.jogo = jogo
        self.tela = pygame.display.set_mode((Config.LARGURA_TELA, Config.ALTURA_TELA))
        pygame.display.set_caption("Monopoly Uffiano - Pygame")
        self.relogio = pygame.time.Clock()
        caminho_base = os.path.dirname(__file__) 
        caminho_raiz = os.path.join(caminho_base, '..')
        caminho_imagem = os.path.join(caminho_raiz, 'assets', 'tabuleiroBG.jpg')
        img = pygame.image.load(caminho_imagem)
        self.imagem_fundo_tabuleiro = pygame.transform.smoothscale(img, (Config.TAMANHO_TABULEIRO, Config.TAMANHO_TABULEIRO))
        self._rects_espacos = self._calcular_rects_espacos()

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
            
        self.tela.blit(self.imagem_fundo_tabuleiro, (Config.POS_X_INICIO, Config.POS_Y_INICIO))
        
        self._desenhar_construcoes()

    def _desenhar_construcoes(self):
        """Desenha casas (quadrados verdes) e hotéis (retângulo vermelho) nas propriedades"""
        for idx, espaco in enumerate(self.jogo.tabuleiro.espacos):
            if hasattr(espaco, 'titulo') and espaco.titulo:
                titulo = espaco.titulo
                if isinstance(titulo, TituloPropriedade):
                    num_casas = titulo.getNumCasas()
                    tem_hotel = titulo.temHotel()
                    
                    if tem_hotel:
                        self._desenhar_hotel(idx)
                    elif num_casas > 0:
                        self._desenhar_casas(idx, num_casas)
    
    def _desenhar_casas(self, idx, num_casas):
        """Desenha quadrados verdes representando casas em uma propriedade"""
        rect = self._rects_espacos[idx]
        if not rect:
            return
        
        tamanho_casa = 8
        espaco = 2
        cor_casa = (0, 200, 0)
        
        if 1 <= idx <= 9:
            y_base = rect.y + 5
            largura_total = num_casas * tamanho_casa + (num_casas - 1) * espaco
            x_inicio = rect.x + (rect.width - largura_total) // 2
            
            for i in range(num_casas):
                x = x_inicio + i * (tamanho_casa + espaco)
                pygame.draw.rect(self.tela, cor_casa, 
                               pygame.Rect(x, y_base, tamanho_casa, tamanho_casa))
                pygame.draw.rect(self.tela, Config.PRETO, 
                               pygame.Rect(x, y_base, tamanho_casa, tamanho_casa), 1)
                
        elif 11 <= idx <= 19:
            x_base = rect.x + 5
            largura_total = num_casas * tamanho_casa + (num_casas - 1) * espaco
            y_inicio = rect.y + (rect.height - largura_total) // 2
            
            for i in range(num_casas):
                y = y_inicio + i * (tamanho_casa + espaco)
                pygame.draw.rect(self.tela, cor_casa, 
                               pygame.Rect(x_base, y, tamanho_casa, tamanho_casa))
                pygame.draw.rect(self.tela, Config.PRETO, 
                               pygame.Rect(x_base, y, tamanho_casa, tamanho_casa), 1)
                
        elif 21 <= idx <= 29:
            y_base = rect.y + 5
            largura_total = num_casas * tamanho_casa + (num_casas - 1) * espaco
            x_inicio = rect.x + (rect.width - largura_total) // 2
            
            for i in range(num_casas):
                x = x_inicio + i * (tamanho_casa + espaco)
                pygame.draw.rect(self.tela, cor_casa, 
                               pygame.Rect(x, y_base, tamanho_casa, tamanho_casa))
                pygame.draw.rect(self.tela, Config.PRETO, 
                               pygame.Rect(x, y_base, tamanho_casa, tamanho_casa), 1)
                
        elif 31 <= idx <= 39:
            x_base = rect.x + 5
            largura_total = num_casas * tamanho_casa + (num_casas - 1) * espaco
            y_inicio = rect.y + (rect.height - largura_total) // 2
            
            for i in range(num_casas):
                y = y_inicio + i * (tamanho_casa + espaco)
                pygame.draw.rect(self.tela, cor_casa, 
                               pygame.Rect(x_base, y, tamanho_casa, tamanho_casa))
                pygame.draw.rect(self.tela, Config.PRETO, 
                               pygame.Rect(x_base, y, tamanho_casa, tamanho_casa), 1)
    
    def _desenhar_hotel(self, idx):
        """Desenha um retângulo vermelho representando um hotel em uma propriedade"""
        rect = self._rects_espacos[idx]
        if not rect:
            return
        
        cor_hotel = (220, 20, 20)
        tamanho_casa = 8
        espaco = 2
        largura_hotel = 2 * tamanho_casa + espaco
        altura_hotel = tamanho_casa
        
        if 1 <= idx <= 9:
            y_base = rect.y + 5
            x_inicio = rect.x + (rect.width - largura_hotel) // 2
            
            pygame.draw.rect(self.tela, cor_hotel, 
                           pygame.Rect(x_inicio, y_base, largura_hotel, altura_hotel))
            pygame.draw.rect(self.tela, Config.PRETO, 
                           pygame.Rect(x_inicio, y_base, largura_hotel, altura_hotel), 1)
            
        elif 11 <= idx <= 19:
            x_base = rect.x + 5
            y_inicio = rect.y + (rect.height - largura_hotel) // 2
            
            pygame.draw.rect(self.tela, cor_hotel, 
                           pygame.Rect(x_base, y_inicio, altura_hotel, largura_hotel))
            pygame.draw.rect(self.tela, Config.PRETO, 
                           pygame.Rect(x_base, y_inicio, altura_hotel, largura_hotel), 1)
            
        elif 21 <= idx <= 29:
            y_base = rect.y + 5
            x_inicio = rect.x + (rect.width - largura_hotel) // 2
            
            pygame.draw.rect(self.tela, cor_hotel, 
                           pygame.Rect(x_inicio, y_base, largura_hotel, altura_hotel))
            pygame.draw.rect(self.tela, Config.PRETO, 
                           pygame.Rect(x_inicio, y_base, largura_hotel, altura_hotel), 1)
            
        elif 31 <= idx <= 39:
            x_base = rect.x + 5
            y_inicio = rect.y + (rect.height - largura_hotel) // 2
            
            pygame.draw.rect(self.tela, cor_hotel, 
                           pygame.Rect(x_base, y_inicio, altura_hotel, largura_hotel))
            pygame.draw.rect(self.tela, Config.PRETO, 
                           pygame.Rect(x_base, y_inicio, altura_hotel, largura_hotel), 1)

    def _calcular_rects_espacos(self):
        """Calcula os rects de clique para as 40 casas do tabuleiro na geometria atual."""
        rects = [None] * 40
        # 0 canto inferior esquerdo
        rects[0] = pygame.Rect(Config.POS_X_INICIO,
                               Config.POS_Y_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO,
                               Config.TAMANHO_CASA_CANTO,
                               Config.TAMANHO_CASA_CANTO)
        # 1..9 lado esquerdo (de baixo para cima)
        for i in range(1, 10):
            x = Config.POS_X_INICIO
            y = Config.POS_Y_INICIO + Config.TAMANHO_CASA_CANTO + (9 - i) * Config.TAMANHO_CASA_PEQUENA
            rects[i] = pygame.Rect(x, y, Config.TAMANHO_CASA_CANTO, Config.TAMANHO_CASA_PEQUENA)
        # 10 canto superior esquerdo
        rects[10] = pygame.Rect(Config.POS_X_INICIO, Config.POS_Y_INICIO, Config.TAMANHO_CASA_CANTO, Config.TAMANHO_CASA_CANTO)
        # 11..19 topo (esquerda -> direita)
        for i in range(1, 10):
            x = Config.POS_X_INICIO + Config.TAMANHO_CASA_CANTO + (i - 1) * Config.TAMANHO_CASA_PEQUENA
            y = Config.POS_Y_INICIO
            rects[10 + i] = pygame.Rect(x, y, Config.TAMANHO_CASA_PEQUENA, Config.TAMANHO_CASA_CANTO)
        # 20 canto superior direito
        rects[20] = pygame.Rect(Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO,
                                Config.POS_Y_INICIO,
                                Config.TAMANHO_CASA_CANTO,
                                Config.TAMANHO_CASA_CANTO)
        # 21..29 lado direito (cima -> baixo)
        for i in range(1, 10):
            x = Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO
            y = Config.POS_Y_INICIO + Config.TAMANHO_CASA_CANTO + (i - 1) * Config.TAMANHO_CASA_PEQUENA
            rects[20 + i] = pygame.Rect(x, y, Config.TAMANHO_CASA_CANTO, Config.TAMANHO_CASA_PEQUENA)
        # 30 canto inferior direito
        rects[30] = pygame.Rect(Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO,
                                Config.POS_Y_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO,
                                Config.TAMANHO_CASA_CANTO,
                                Config.TAMANHO_CASA_CANTO)
        # 31..39 base (direita -> esquerda)
        for i in range(1, 10):
            x = Config.POS_X_INICIO + Config.TAMANHO_CASA_CANTO + (9 - i) * Config.TAMANHO_CASA_PEQUENA
            y = Config.POS_Y_INICIO + Config.TAMANHO_TABULEIRO - Config.TAMANHO_CASA_CANTO
            rects[30 + i] = pygame.Rect(x, y, Config.TAMANHO_CASA_PEQUENA, Config.TAMANHO_CASA_CANTO)
        return rects

    def get_posicao_por_ponto(self, ponto):
        """Retorna o índice da casa clicada, ou None se fora."""
        if not self._rects_espacos:
            return None
        for idx, r in enumerate(self._rects_espacos):
            if r and r.collidepoint(ponto):
                return idx
        return None

