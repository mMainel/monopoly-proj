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
        self.fonte_propriedades = None

        self.x = 0
        self.y = 0
        self.largura = 0
        self.altura = 0
        
        caminho_base = os.path.dirname(__file__)  
        caminho_raiz = os.path.join(caminho_base, '..')
        self.caminho_assets_pecas = os.path.join(caminho_raiz, 'assets', 'pecas')
        self.image_cache = {}

        self.update_layout()  
        
    def _get_tinted_color(self, color, tint_factor=0.6):
        if sum(color) < 100:
             return (245, 245, 245) 
        
        r = int(color[0] + (255 - color[0]) * tint_factor)
        g = int(color[1] + (255 - color[1]) * tint_factor)
        b = int(color[2] + (255 - color[2]) * tint_factor)
        return (r, g, b)

    def update_layout(self):
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
        self.fonte_propriedades = pygame.font.Font(None, max(10, base - 4))

    def desenhar(self):
        self.update_layout()
        
        painel_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(self.tela, Config.CINZA_CLARO, painel_rect)
        pygame.draw.rect(self.tela, Config.PRETO, painel_rect, 2)

        titulo = self.fonte_titulo.render("JOGADORES", True, Config.PRETO)
        self.tela.blit(titulo, (self.x + 12, self.y + 10))

        num_jogadores = max(1, len(self.jogadores))
        duas_colunas = num_jogadores > 4

        margem_topo = 56
        margem_interna = 10
        n_colunas = 2 if duas_colunas else 1
        coluna_largura = (self.largura - (n_colunas + 1) * margem_interna) // n_colunas
        coluna_altura = self.altura - margem_topo - margem_interna

        if duas_colunas:
            jogadores_por_coluna = (num_jogadores + 1) // 2
        else:
            jogadores_por_coluna = num_jogadores

        espaco_por_jogador = max(60, coluna_altura // jogadores_por_coluna)

        # Desenhar cada jogador
        for i, jogador in enumerate(self.jogadores):
            col = 0 if (not duas_colunas or i < jogadores_por_coluna) else 1
            linha = i if col == 0 else i - jogadores_por_coluna

            base_x = self.x + margem_interna + col * (coluna_largura + margem_interna)
            base_y = self.y + margem_topo + linha * espaco_por_jogador

            if base_y + espaco_por_jogador > self.y + self.altura:
                altura_bloco = max(48, (self.y + self.altura) - base_y - margem_interna)
            else:
                altura_bloco = espaco_por_jogador - 6

            self.desenhar_jogador(jogador, base_x, base_y, coluna_largura, altura_bloco)

    def desenhar_jogador(self, jogador, x, y, largura, altura):
        padding = 8
        
        peca = jogador.getPeca() 
        cor_peca = Config.CORES_PECAS.get(peca, Config.PRETO)
        cor_nome = cor_peca if not jogador.estaFalido else (180, 0, 0)
        cor_fundo_jogador = self._get_tinted_color(cor_peca)
        
        jogador_rect = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(self.tela, cor_fundo_jogador, jogador_rect)
        pygame.draw.rect(self.tela, Config.PRETO, jogador_rect, 1)
        
        if peca:
            nome_imagem = f"{peca.name}.png"
            imagem_peca = self.image_cache.get(nome_imagem)

            if not imagem_peca:
                try:
                    caminho_completo = os.path.join(self.caminho_assets_pecas, nome_imagem)
                    img = pygame.image.load(caminho_completo).convert_alpha()
                    
                    # Redimensiona para uma proporção do cartão (ex: 80% da altura do cartão)
                    # Mantém a proporção 1:1 original da imagem
                    target_size = int(altura * 0.6) 
                    img = pygame.transform.smoothscale(img, (target_size, target_size))
                    
                    # Define a opacidade
                    img.set_alpha(230) 
                    
                    self.image_cache[nome_imagem] = img
                    imagem_peca = img
                except Exception as e:
                    self.image_cache[nome_imagem] = False
            
            if imagem_peca:
                img_rect = imagem_peca.get_rect(center=jogador_rect.center)
                self.tela.blit(imagem_peca, img_rect)

        raio = max(6, min(12, altura // 8))
        nome_x = x + padding + raio + 6
        nome_y = y + padding
        nome_render = self.fonte_titulo.render(jogador.getNome(), True, cor_nome)
        self.tela.blit(nome_render, (nome_x, nome_y))

        saldo_texto = f"R$ {jogador.getSaldo()}"
        saldo_render = self.fonte_info.render(saldo_texto, True, Config.PRETO)
        self.tela.blit(saldo_render, (x + padding, y + padding + raio * 2 - 2))

        pos_texto = f"Casa {jogador.getPosicao()}"
        pos_render = self.fonte_info.render(pos_texto, True, Config.PRETO)
        self.tela.blit(pos_render, (x + padding, y + padding + raio * 2 + 18))

        if jogador.estaEmCadeia():
            cadeia_texto = f"🔒 {jogador.getTurnosCadeia()}t"
            cadeia_render = self.fonte_info.render(cadeia_texto, True, (180, 40, 40))
            self.tela.blit(cadeia_render, (x + largura - padding - cadeia_render.get_width(), y + padding))

        propriedades = jogador.getPropriedades()
        num_props = len(propriedades)
        
        props_header = f"Propriedades ({num_props}):"
        props_header_render = self.fonte_info.render(props_header, True, Config.PRETO)
        y_props = y + altura - padding - 50
        self.tela.blit(props_header_render, (x + padding, y_props))
        
        if num_props > 0:
            y_offset = y_props + 15
            max_mostrar = min(3, num_props)
            
            for i in range(max_mostrar):
                prop = propriedades[i]
                nome_prop = prop.getNome() if hasattr(prop, 'getNome') else 'Prop'
                
                if len(nome_prop) > 12:
                    nome_prop = nome_prop[:10] + "..."
                
                cor_texto = Config.PRETO
                if hasattr(prop, 'getCor'):
                    try:
                        cor_nome = prop.getCor()
                        cores_mapa = {
                            "Marrom": (139, 69, 19),
                            "Azul Claro": (135, 206, 250),
                            "Rosa": (255, 20, 147),
                            "Laranja": (255, 140, 0),
                            "Vermelho": (220, 20, 60),
                            "Amarelo": (255, 215, 0),
                            "Verde": (0, 128, 0),
                            "Azul Escuro": (0, 0, 139)
                        }
                        cor_texto = cores_mapa.get(cor_nome, Config.PRETO)
                    except:
                        pass
                
                raio_prop = 3
                pygame.draw.circle(self.tela, cor_texto, 
                                 (x + padding + raio_prop, y_offset + 5), raio_prop)
                
                texto_prop = self.fonte_propriedades.render(nome_prop, True, Config.PRETO)
                self.tela.blit(texto_prop, (x + padding + raio_prop * 2 + 3, y_offset))
                y_offset += 12
            
            if num_props > 3:
                mais_texto = self.fonte_propriedades.render(f"... e mais {num_props - 3}", True, Config.PRETO)
                self.tela.blit(mais_texto, (x + padding, y_offset))