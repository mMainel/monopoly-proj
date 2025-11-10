import pygame
from config import Config

class BotaoDadoUI:
    def __init__(self, tela, jogo):
        self.tela = tela
        self.jogo = jogo
        self.clicado = False
        self.habilitado = True  
        
        self.largura = 220
        self.altura = 70
        
        centro_tabuleiro_x = Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO // 2
        centro_tabuleiro_y = Config.POS_Y_INICIO + Config.TAMANHO_TABULEIRO // 2
        
        self.rect = pygame.Rect(
            centro_tabuleiro_x - self.largura // 2,
            centro_tabuleiro_y + 20,  # Logo abaixo do feed de eventos
            self.largura,
            self.altura
        )
        
        self.fonte = pygame.font.Font(None, 36)
        self.fonte_nome = pygame.font.Font(None, 24)
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