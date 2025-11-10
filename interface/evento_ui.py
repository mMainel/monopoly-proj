import pygame
from config import Config
from collections import deque
import time

class EventoUI:
    def __init__(self, tela):
        self.tela = tela
        self.eventos = deque(maxlen=5)
        self.fonte = pygame.font.Font(None, 24)
        self.largura = 400
        self.altura = 130

        centro_tabuleiro_x = Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO // 2
        centro_tabuleiro_y = Config.POS_Y_INICIO + Config.TAMANHO_TABULEIRO // 2

        self.x = centro_tabuleiro_x - self.largura // 2
        self.y = centro_tabuleiro_y - 150

    def adicionar_evento(self, texto):
        timestamp = time.strftime("%H:%M:%S")
        self.eventos.append(f"[{timestamp}] {texto}")
    
    def desenhar(self):
        s = pygame.Surface((self.largura, self.altura))
        s.set_alpha(220)
        s.fill((40, 40, 40))
        self.tela.blit(s, (self.x, self.y))

        pygame.draw.rect(self.tela, Config.PRETO, 
                        pygame.Rect(self.x, self.y, self.largura, self.altura), 
                        3, border_radius=10)
        
        titulo = self.fonte.render("EVENTOS DO JOGO", True, Config.BRANCO)
        titulo_rect = titulo.get_rect(center=(self.x + self.largura // 2, self.y + 15))
        self.tela.blit(titulo, titulo_rect)
        y_offset = 40
        
        for evento in reversed(self.eventos):
            texto_render = pygame.font.Font(None, 20).render(evento, True, Config.BRANCO)
            self.tela.blit(texto_render, (self.x + 10, self.y + y_offset))
            y_offset += 20


class DialogoCompraUI:
    def __init__(self, tela):
        self.tela = tela
        self.ativo = False
        self.propriedade = None
        self.jogador = None
        self.resposta = None
        self.largura = 500
        self.altura = 250

        self.x = (Config.LARGURA_TELA - self.largura) // 2
        self.y = (Config.ALTURA_TELA - self.altura) // 2

        self.fonte_titulo = pygame.font.Font(None, 36)
        self.fonte_texto = pygame.font.Font(None, 24)
        self.fonte_botao = pygame.font.Font(None, 28)

        btn_largura = 120
        btn_altura = 50
        espaco = 40

        centro_x = self.x + self.largura // 2
        btn_y = self.y + self.altura - 70

        self.btn_sim = pygame.Rect(
            centro_x - btn_largura - espaco // 2,
            btn_y,
            btn_largura,
            btn_altura
        )

        self.btn_nao = pygame.Rect(
            centro_x + espaco // 2,
            btn_y,
            btn_largura,
            btn_altura
        )
    
    def mostrar(self, propriedade, jogador):
        self.ativo = True
        self.propriedade = propriedade
        self.jogador = jogador
        self.resposta = None
    
    def handle_event(self, evento):
        if not self.ativo:
            return
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_sim.collidepoint(evento.pos):
                self.resposta = True
                self.ativo = False
            elif self.btn_nao.collidepoint(evento.pos):
                self.resposta = False
                self.ativo = False
    
    def obter_resposta(self):
        return self.resposta
    
    def desenhar(self):
        if not self.ativo or not self.propriedade:
            return
        
        overlay = pygame.Surface((Config.LARGURA_TELA, Config.ALTURA_TELA))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.tela.blit(overlay, (0, 0))

        pygame.draw.rect(self.tela, Config.BRANCO, 
                        pygame.Rect(self.x, self.y, self.largura, self.altura),
                        border_radius=10)
        pygame.draw.rect(self.tela, Config.PRETO, 
                        pygame.Rect(self.x, self.y, self.largura, self.altura), 
                        3, border_radius=10)
        
        titulo = self.fonte_titulo.render("COMPRAR PROPRIEDADE?", True, Config.PRETO)
        titulo_rect = titulo.get_rect(center=(self.x + self.largura // 2, self.y + 40))

        self.tela.blit(titulo, titulo_rect)

        nome = self.propriedade.getNome() if hasattr(self.propriedade, 'getNome') else str(self.propriedade)
        texto_nome = self.fonte_texto.render(nome, True, Config.PRETO)
        texto_nome_rect = texto_nome.get_rect(center=(self.x + self.largura // 2, self.y + 90))

        self.tela.blit(texto_nome, texto_nome_rect)

        preco = self.propriedade.getPreco() if hasattr(self.propriedade, 'getPreco') else 0
        texto_preco = self.fonte_texto.render(f"Preço: R$ {preco}", True, Config.PRETO)
        texto_preco_rect = texto_preco.get_rect(center=(self.x + self.largura // 2, self.y + 120))

        self.tela.blit(texto_preco, texto_preco_rect)

        saldo = self.jogador.getSaldo() if self.jogador else 0
        cor_saldo = (0, 150, 0) if saldo >= preco else (180, 0, 0)
        texto_saldo = self.fonte_texto.render(f"Seu saldo: R$ {saldo}", True, cor_saldo)
        texto_saldo_rect = texto_saldo.get_rect(center=(self.x + self.largura // 2, self.y + 150))

        self.tela.blit(texto_saldo, texto_saldo_rect)

        mouse_pos = pygame.mouse.get_pos()
        cor_sim = (0, 180, 0) if self.btn_sim.collidepoint(mouse_pos) else (0, 150, 0)

        pygame.draw.rect(self.tela, cor_sim, self.btn_sim, border_radius=8)
        pygame.draw.rect(self.tela, Config.PRETO, self.btn_sim, 2, border_radius=8)

        texto_sim = self.fonte_botao.render("SIM", True, Config.BRANCO)
        texto_sim_rect = texto_sim.get_rect(center=self.btn_sim.center)

        self.tela.blit(texto_sim, texto_sim_rect)
        cor_nao = (180, 0, 0) if self.btn_nao.collidepoint(mouse_pos) else (150, 0, 0)

        pygame.draw.rect(self.tela, cor_nao, self.btn_nao, border_radius=8)
        pygame.draw.rect(self.tela, Config.PRETO, self.btn_nao, 2, border_radius=8)

        texto_nao = self.fonte_botao.render("NÃO", True, Config.BRANCO)
        texto_nao_rect = texto_nao.get_rect(center=self.btn_nao.center)
        self.tela.blit(texto_nao, texto_nao_rect)