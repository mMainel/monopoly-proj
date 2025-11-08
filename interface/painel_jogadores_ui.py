import pygame
import os
from modules.peca import Peca
from config import Config

class PainelJogadoresUI:

    def __init__(self, tela, jogadores, proporcao=0.30, margem=16):
        self.tela = tela
        self.jogadores = jogadores
        self.proporcao = proporcao 
        self.margem_externa = margem

        self.fonte_titulo = None
        self.fonte_info = None


        self.x = 0
        self.y = 0
        self.largura = 0
        self.altura = 0
        
        caminho_base = os.path.dirname(__file__)  # .../interface
        caminho_raiz = os.path.join(caminho_base, '..')  # .../
        self.caminho_assets_pecas = os.path.join(caminho_raiz, 'assets', 'pecas')
        self.image_cache = {}

        self.update_layout()  # configura largura/altura iniciais
        
    def _get_tinted_color(self, color, tint_factor=0.6):
        """Mistura a cor da peça com branco para criar um fundo pastel."""
        # Garante que a cor não seja muito escura (ex: Preto do fallback)
        if sum(color) < 100:
             return (245, 245, 245) # Fallback para bege
             
        r = int(color[0] + (255 - color[0]) * tint_factor)
        g = int(color[1] + (255 - color[1]) * tint_factor)
        b = int(color[2] + (255 - color[2]) * tint_factor)
        return (r, g, b)

    def update_layout(self):
        """Recalcula posições, tamanhos e fontes com base no tamanho atual da tela."""
        largura_tela, altura_tela = self.tela.get_size()


        largura_calc = max(240, int(largura_tela * self.proporcao))
        largura_calc = min(int(largura_tela * 0.45), largura_calc)  
    

        self.largura = largura_calc
        self.x = largura_tela - self.largura - self.margem_externa
        self.y = self.margem_externa
        self.altura = altura_tela - 2 * self.margem_externa


        base = max(12, int(altura_tela / 32))   
        self.fonte_titulo = pygame.font.Font(None, base + 8)
        self.fonte_info = pygame.font.Font(None, base)

    def desenhar(self):
        """Desenha o painel completo; chama desenhar_jogador para cada jogador."""
        self.update_layout()
        
        # Painel de fundo
        painel_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(self.tela, Config.CINZA_CLARO, painel_rect)
        pygame.draw.rect(self.tela, Config.PRETO, painel_rect, 2)

        # Título
        titulo = self.fonte_titulo.render("JOGADORES", True, Config.PRETO)
        self.tela.blit(titulo, (self.x + 12, self.y + 10))

        # configuração de layout interno
        num_jogadores = max(1, len(self.jogadores))
        duas_colunas = num_jogadores > 4

        margem_topo = 56
        margem_interna = 10
        # calcula largura por coluna
        n_colunas = 2 if duas_colunas else 1
        coluna_largura = (self.largura - (n_colunas + 1) * margem_interna) // n_colunas
        coluna_altura = self.altura - margem_topo - margem_interna

        # quantos por coluna
        if duas_colunas:
            jogadores_por_coluna = (num_jogadores + 1) // 2
        else:
            jogadores_por_coluna = num_jogadores

        # espaço vertical por jogador (reserva um pequeno padding entre blocos)
        espaco_por_jogador = max(60, coluna_altura // jogadores_por_coluna)

        # desenhar cada jogador
        for i, jogador in enumerate(self.jogadores):
            col = 0 if (not duas_colunas or i < jogadores_por_coluna) else 1
            linha = i if col == 0 else i - jogadores_por_coluna

            base_x = self.x + margem_interna + col * (coluna_largura + margem_interna)
            base_y = self.y + margem_topo + linha * espaco_por_jogador

            # limita o desenho para não ultrapassar o painel
            if base_y + espaco_por_jogador > self.y + self.altura:
                # se faltar espaço, encurta a altura do último bloco
                altura_bloco = max(48, (self.y + self.altura) - base_y - margem_interna)
            else:
                altura_bloco = espaco_por_jogador - 6

            self.desenhar_jogador(jogador, base_x, base_y, coluna_largura, altura_bloco)

    def desenhar_jogador(self, jogador, x, y, largura, altura):
        padding = 8
        
        # fundo e borda do cartão do jogador
        jogador_rect = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(self.tela, (245, 245, 245), jogador_rect)
        pygame.draw.rect(self.tela, Config.PRETO, jogador_rect, 1)

        peca = jogador.getPeca() 
        # Cor sólida (para bolinha e nome)
        cor_peca = Config.CORES_PECAS.get(peca, Config.PRETO) #
        # Cor do nome (vermelho se falido)
        cor_nome = cor_peca if not jogador.estaFalido else (180, 0, 0)
        # Cor de fundo (versão pastel da cor da peça)
        cor_fundo_jogador = self._get_tinted_color(cor_peca)
        
        jogador_rect = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(self.tela, cor_fundo_jogador, jogador_rect)
        
        #imagem
        if peca: # Desenha apenas se a peça for válida
            nome_imagem = f"{peca.name}.png"
            imagem_peca = self.image_cache.get(nome_imagem)

            if not imagem_peca:
                try:
                    caminho_completo = os.path.join(self.caminho_assets_pecas, nome_imagem)
                    img = pygame.image.load(caminho_completo).convert_alpha()
                    
                    # Redimensiona para uma proporção do cartão (ex: 80% da altura do cartão)
                    # Mantém a proporção 1:1 original da imagem
                    target_size = int(altura * 0.7) 
                    img = pygame.transform.smoothscale(img, (target_size, target_size))
                    
                    # Define a opacidade (alpha value: 0-255)
                    img.set_alpha(75) # Ajuste este valor para mais ou menos opacidade (ex: 50 a 100)
                    
                    self.image_cache[nome_imagem] = img
                    imagem_peca = img
                except Exception as e:
                    #print(f"Erro ao carregar imagem da peça {nome_imagem}: {e}") # Para debug
                    self.image_cache[nome_imagem] = False # Cache falha
            
            if imagem_peca:
                # Centraliza a imagem no fundo do cartão do jogador
                img_rect = imagem_peca.get_rect(center=jogador_rect.center)
                self.tela.blit(imagem_peca, img_rect)

        raio = max(6, min(12, altura // 8))
        centro_cx = x + padding + raio
        centro_cy = y + padding + raio
        #pygame.draw.circle(self.tela, cor_peca, (centro_cx, centro_cy), raio)
        #pygame.draw.circle(self.tela, Config.PRETO, (centro_cx, centro_cy), raio, 1)

        # Nome (alinhado à direita da bolinha)
        nome_x = centro_cx + raio + 6
        nome_y = y + padding
        nome_render = self.fonte_titulo.render(jogador.getNome(), True, cor_nome)
        self.tela.blit(nome_render, (nome_x, nome_y))

        # Saldo (linha abaixo)
        saldo_texto = f"Saldo: R$ {jogador.getSaldo()}"
        saldo_render = self.fonte_info.render(saldo_texto, True, Config.PRETO)
        self.tela.blit(saldo_render, (x + padding, y + padding + raio * 2 - 2))

        # Posição
        pos_texto = f"Pos: {jogador.getPosicao()}"
        pos_render = self.fonte_info.render(pos_texto, True, Config.PRETO)
        self.tela.blit(pos_render, (x + padding, y + padding + raio * 2 + 18))

        # Cadeia
        if jogador.estaEmCadeia():
            cadeia_texto = f"Preso: {jogador.getTurnosCadeia()}t"
            cadeia_render = self.fonte_info.render(cadeia_texto, True, (180, 40, 40))
            self.tela.blit(cadeia_render, (x + largura - padding - cadeia_render.get_width(), y + padding))

        # Propriedades
        props_texto = f"Propriedades: {len(jogador.getPropriedades())}"
        props_render = self.fonte_info.render(props_texto, True, Config.PRETO)
        self.tela.blit(props_render, (x + padding, y + altura - padding - props_render.get_height()))
