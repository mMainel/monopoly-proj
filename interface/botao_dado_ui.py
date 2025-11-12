import pygame
from config import Config

class BotaoDadoUI:
    def __init__(self, tela, jogo):
        self.tela = tela
        self.jogo = jogo
        self.clicado = False
        self.habilitado = True  
        
        self.largura = 180
        self.altura = 55
        
        # Calcular posição no gap entre tabuleiro e painel
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
        tamanho_dado = int(Config.TAMANHO_TABULEIRO * 0.10)
        
        offset_baixo = 80
        y_dados = centro_tabuleiro_y - (tamanho_dado // 2) + offset_baixo
        y_botao = y_dados + tamanho_dado + 60
        
        self.rect = pygame.Rect(
            centro_gap_x - self.largura // 2,
            y_botao,
            self.largura,
            self.altura
        )
        
        self.fonte = pygame.font.Font(None, 32)
        self.fonte_nome = pygame.font.Font(None, 20)
        self.cor_normal = (0, 120, 200)
        self.cor_hover = (0, 150, 255)
        self.cor_desabilitado = (100, 100, 100)

    def desenhar(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if not self.habilitado:
            cor = self.cor_desabilitado
        elif self.rect.collidepoint(mouse_pos):
            cor = self.cor_hover
        else:
            cor = self.cor_normal
        
        pygame.draw.rect(self.tela, cor, self.rect, border_radius=15)
        pygame.draw.rect(self.tela, Config.PRETO, self.rect, 4, border_radius=15)
        
        texto_str = "JOGAR"
        texto = self.fonte.render(texto_str, True, Config.BRANCO)
        texto_rect = texto.get_rect(center=(self.rect.centerx, self.rect.centery - 10))
        self.tela.blit(texto, texto_rect)
        
        jogador_atual = self.jogo.jogadorAtual if self.jogo else None
        if jogador_atual:
            nome_texto = self.fonte_nome.render(f"Turno: {jogador_atual.getNome()}", True, Config.BRANCO)
            nome_rect = nome_texto.get_rect(center=(self.rect.centerx, self.rect.centery + 15))
            self.tela.blit(nome_texto, nome_rect)
        
        if not self.habilitado:
            aviso = pygame.font.Font(None, 22).render("Processando...", True, (255, 255, 100))
            aviso_rect = aviso.get_rect(center=(self.rect.centerx, self.rect.y - 20))
            self.tela.blit(aviso, aviso_rect)

    def handle_event(self, evento):
        if not self.habilitado:
            return
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.clicado = True

    def foi_clicado(self):
        if self.clicado:
            self.clicado = False
            return True
        return False
    
    def habilitar(self):
        self.habilitado = True
    
    def desabilitar(self):
        self.habilitado = False