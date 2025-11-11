import pygame
from config import Config

class DialogoOpcoesCadeiaUI:
    """Interface para o jogador escolher como tentar sair da cadeia"""
    
    def __init__(self, tela):
        self.tela = tela
        self.ativo = False
        self.jogador = None
        self.opcao_escolhida = None
        
        # Dimensões do diálogo
        self.largura = 500
        self.altura = 400
        self.x = (Config.LARGURA_TELA - self.largura) // 2
        self.y = (Config.ALTURA_TELA - self.altura) // 2
        
        # Fontes
        self.fonte_titulo = pygame.font.Font(None, 40)
        self.fonte_texto = pygame.font.Font(None, 28)
        self.fonte_botao = pygame.font.Font(None, 32)
        
        # Cores
        self.cor_fundo = (240, 240, 240)
        self.cor_borda = (50, 50, 50)
        self.cor_titulo = (200, 0, 0)
        self.cor_texto = (40, 40, 40)
        self.cor_botao_normal = (70, 130, 180)
        self.cor_botao_hover = (100, 160, 210)
        self.cor_botao_desabilitado = (150, 150, 150)
        self.cor_texto_botao = (255, 255, 255)
        
        # Botões
        self.botoes = []
        self.botao_hover = None
        
    def mostrar(self, jogador):
        """
        Mostra o diálogo de opções da cadeia
        
        Args:
            jogador: Jogador que está na cadeia
        """
        self.ativo = True
        self.jogador = jogador
        self.opcao_escolhida = None
        self._criar_botoes()
        
    def _criar_botoes(self):
        """Cria os botões baseado nas opções disponíveis do jogador"""
        self.botoes = []
        y_inicial = self.y + 180
        espacamento = 80
        
        # Opção 1: Tentar tirar dupla
        botao_dupla = {
            'rect': pygame.Rect(self.x + 50, y_inicial, 400, 60),
            'texto': 'Rolar o dado (tentar tirar dupla)',
            'opcao': 'dupla',
            'habilitado': True
        }
        self.botoes.append(botao_dupla)
        
        # Opção 2: Usar carta de sair da cadeia
        y_inicial += espacamento
        pode_usar_carta = self.jogador.podeUsarCartaSairCadeia()
        botao_carta = {
            'rect': pygame.Rect(self.x + 50, y_inicial, 400, 60),
            'texto': 'Usar carta "Saia da prisão"',
            'opcao': 'carta',
            'habilitado': pode_usar_carta
        }
        self.botoes.append(botao_carta)
        
        # Opção 3: Pagar fiança
        y_inicial += espacamento
        pode_pagar = self.jogador.podePagarFianca()
        botao_fianca = {
            'rect': pygame.Rect(self.x + 50, y_inicial, 400, 60),
            'texto': f'Pagar R$50 de fiança',
            'opcao': 'fianca',
            'habilitado': pode_pagar
        }
        self.botoes.append(botao_fianca)
    
    def handle_event(self, evento):
        """Processa eventos do pygame"""
        if not self.ativo:
            return
        
        if evento.type == pygame.MOUSEMOTION:
            self.botao_hover = None
            for botao in self.botoes:
                if botao['habilitado'] and botao['rect'].collidepoint(evento.pos):
                    self.botao_hover = botao
                    break
        
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Botão esquerdo
                for botao in self.botoes:
                    if botao['habilitado'] and botao['rect'].collidepoint(evento.pos):
                        self.opcao_escolhida = botao['opcao']
                        self.ativo = False
                        break
    
    def desenhar(self):
        """Desenha o diálogo na tela"""
        if not self.ativo or not self.jogador:
            return
        
        # Fundo semi-transparente
        overlay = pygame.Surface((Config.LARGURA_TELA, Config.ALTURA_TELA))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.tela.blit(overlay, (0, 0))
        
        # Caixa do diálogo
        pygame.draw.rect(self.tela, self.cor_fundo, 
                        (self.x, self.y, self.largura, self.altura))
        pygame.draw.rect(self.tela, self.cor_borda, 
                        (self.x, self.y, self.largura, self.altura), 4)
        
        # Título
        titulo = self.fonte_titulo.render("🔒 NA CADEIA 🔒", True, self.cor_titulo)
        titulo_rect = titulo.get_rect(center=(self.x + self.largura // 2, self.y + 40))
        self.tela.blit(titulo, titulo_rect)
        
        # Informações do jogador
        info_text = f"{self.jogador.getNome()}"
        info = self.fonte_texto.render(info_text, True, self.cor_texto)
        info_rect = info.get_rect(center=(self.x + self.largura // 2, self.y + 85))
        self.tela.blit(info, info_rect)
        
        # Saldo
        saldo_text = f"Saldo: R${self.jogador.getSaldo()}"
        saldo = self.fonte_texto.render(saldo_text, True, self.cor_texto)
        saldo_rect = saldo.get_rect(center=(self.x + self.largura // 2, self.y + 115))
        self.tela.blit(saldo, saldo_rect)
        
        # Instrução
        instrucao = self.fonte_texto.render("Como deseja sair?", True, self.cor_texto)
        instrucao_rect = instrucao.get_rect(center=(self.x + self.largura // 2, self.y + 145))
        self.tela.blit(instrucao, instrucao_rect)
        
        # Botões
        for botao in self.botoes:
            # Escolhe a cor do botão
            if not botao['habilitado']:
                cor = self.cor_botao_desabilitado
            elif self.botao_hover == botao:
                cor = self.cor_botao_hover
            else:
                cor = self.cor_botao_normal
            
            # Desenha o botão
            pygame.draw.rect(self.tela, cor, botao['rect'], border_radius=8)
            pygame.draw.rect(self.tela, self.cor_borda, botao['rect'], 2, border_radius=8)
            
            # Texto do botão
            texto = self.fonte_botao.render(botao['texto'], True, self.cor_texto_botao)
            texto_rect = texto.get_rect(center=botao['rect'].center)
            self.tela.blit(texto, texto_rect)
            
            # Se desabilitado, mostra um X
            if not botao['habilitado']:
                x_surface = pygame.Surface((botao['rect'].width, botao['rect'].height))
                x_surface.set_alpha(100)
                x_surface.fill((100, 0, 0))
                self.tela.blit(x_surface, botao['rect'].topleft)
                
                texto_x = self.fonte_titulo.render("✗", True, (200, 0, 0))
                texto_x_rect = texto_x.get_rect(center=botao['rect'].center)
                self.tela.blit(texto_x, texto_x_rect)
    
    def obter_resposta(self):
        """Retorna a opção escolhida pelo jogador"""
        return self.opcao_escolhida
    
    def esta_ativo(self):
        """Verifica se o diálogo está ativo"""
        return self.ativo