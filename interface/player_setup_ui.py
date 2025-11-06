import pygame
from config import Config
import os
from modules.peca import Peca

class TextInputBox:
    """
    Classe para criar uma caixa de input de texto no Pygame.
    """
    def __init__(self, x, y, w, h, fonte_texto, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = Config.CINZA_CLARO
        self.color_active = Config.PRETO
        self.color = self.color_inactive
        self.text = text
        self.fonte = fonte_texto
        # self.txt_surface = self.fonte.render(text, True, self.color)
        self.active = False
        self.is_default = True 
        self.border_radius = 25

    def handle_event(self, event):
        """Processa eventos de mouse e teclado."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Se o usuário clicou na caixa
            if self.rect.collidepoint(event.pos):
                # --- MUDANÇA 2: Lógica de "Limpar ao Clicar" ---
                if not self.active: # Se estava inativa e vai ativar
                    self.active = True
                    if self.is_default:
                        self.text = "" # Limpa o texto
                        self.is_default = False
                # -----------------------------------------------
            else:
                self.active = False
            # Muda a cor
            self.color = self.color_active if self.active else self.color_inactive
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                # --- MUDANÇA 3: Marca como não-padrão ao digitar ---
                self.is_default = False
                # --------------------------------------------------
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = self.color_inactive
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        """Desenha a caixa de texto na tela com cantos arredondados."""
        # Fundo da caixa
        pygame.draw.rect(screen, Config.BRANCO, self.rect, border_radius=self.border_radius)
        # Borda da caixa
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=self.border_radius)
        
        # --- MUDANÇA 4: Renderiza o texto toda vez ---
        # Isso garante que o texto "Jogador 1" suma imediatamente ao clicar
        self.txt_surface = self.fonte.render(self.text, True, Config.PRETO)
        # -----------------------------------------------
        
        # Desenha o texto (com padding e centralizado verticalmente)
        text_y = self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2
        screen.blit(self.txt_surface, (self.rect.x + 10, text_y))

    def get_text(self):
        return self.text



def rodar_setup_ui():
    """
    Executa o loop da tela de setup (lobby) e retorna a lista de nomes.
    Retorna None se o usuário fechar a janela.
    """
    pygame.init()
    tela = pygame.display.set_mode((Config.LARGURA_TELA, Config.ALTURA_TELA))
    pygame.display.set_caption("Configurar Jogo - Monopoly Uffiano")
    relogio = pygame.time.Clock()
    pygame.key.set_repeat(300, 30)
    
    # --- Carregar Imagem ---
    caminho_base = os.path.dirname(__file__) # .../interface
    caminho_raiz = os.path.join(caminho_base, '..') # .../
    caminho_imagem = os.path.join(caminho_raiz, 'assets', 'lobby.png')
    
    background_image = pygame.image.load(caminho_imagem)
    background_image = pygame.transform.scale(background_image, (Config.LARGURA_TELA, Config.ALTURA_TELA))

    # --- Fontes ---
    fonte_titulo = pygame.font.Font(None, 50) # Fonte do título principal
    fonte_label = pygame.font.Font(None, 28)  # Fonte "fina" para o label
    fonte_normal = pygame.font.Font(None, 28) # Fonte para botões e nomes
    fonte_input = pygame.font.Font(None, 28)  # Fonte das caixas de texto
    fonte_num_botao = pygame.font.Font(None, 24) # Fonte dos números (2-8)

    # --- Configuração Botões de Número (2-8) ---
    num_jogadores = 2
    botoes_num = []
    BTN_RAIO = 20
    BTN_SPACING = 15
    NUM_BOTOES = 7 # (Para 2, 3, 4, 5, 6, 7, 8)
    
    # Calcula a largura total de todos os botões e espaços
    total_largura_botoes = (NUM_BOTOES * (BTN_RAIO * 2)) + ((NUM_BOTOES - 1) * BTN_SPACING)
    # Calcula o X inicial para centralizar o grupo de botões
    start_x = (Config.LARGURA_TELA - total_largura_botoes) // 2
    botoes_y = 200 # Posição Y dos botões

    for i in range(NUM_BOTOES):
        num = i + 2
        centro_x = start_x + (i * (BTN_RAIO * 2 + BTN_SPACING)) + BTN_RAIO
        # Armazena o 'Rect' para detecção de clique e o número
        botoes_num.append({'rect': pygame.Rect(centro_x - BTN_RAIO, botoes_y - BTN_RAIO, BTN_RAIO * 2, BTN_RAIO * 2), 'num': num})

    # --- Configuração Caixas de Texto ---
    text_boxes = []
    BOX_WIDTH = 400
    BOX_HEIGHT = 30
    BOX_SPACING = 35
    box_x_central = (Config.LARGURA_TELA - BOX_WIDTH) // 2
    box_base_y = 285

    def atualizar_text_boxes(num_selecionado):
        """Função interna para adicionar/remover caixas de texto."""
        text_boxes.clear()
        for i in range(num_selecionado):
            y_pos = box_base_y + (i * BOX_SPACING)
            text_boxes.append(TextInputBox(box_x_central, y_pos, BOX_WIDTH, BOX_HEIGHT, fonte_input, text=f"Jogador {i + 1}"))

    atualizar_text_boxes(num_jogadores) # Inicializa as 2 primeiras caixas

    # --- Botão Iniciar ---
    BTN_INICIAR_W = 220
    BTN_INICIAR_H = 60
    btn_iniciar = pygame.Rect((Config.LARGURA_TELA - BTN_INICIAR_W) // 2, 600, BTN_INICIAR_W, BTN_INICIAR_H)
    btn_iniciar_radius = 15

    rodando = True
    while rodando:
        
        # --- Processamento de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                return None 

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Botão Iniciar Jogo
                if btn_iniciar.collidepoint(event.pos):
                    rodando = False 
                    
                # Botões de Número (2-8)
                for btn in botoes_num:
                    if btn['rect'].collidepoint(event.pos):
                        if num_jogadores != btn['num']:
                            num_jogadores = btn['num']
                            atualizar_text_boxes(num_jogadores)
            
            # Passa eventos para as caixas de texto
            for box in text_boxes:
                box.handle_event(event)

        # --- Lógica de Desenho ---
        tela.blit(background_image, (0, 0))

        # Título
        titulo_render = fonte_titulo.render("CONFIGURAR JOGO", True, Config.PRETO)
        tela.blit(titulo_render, (Config.LARGURA_TELA // 2 - titulo_render.get_width() // 2, 140)) # Y mais alto

        # Label "Selecione..."
        label_render = fonte_label.render("Selecione a quantidade de jogadores", True, Config.PRETO)
        tela.blit(label_render, (Config.LARGURA_TELA // 2 - label_render.get_width() // 2, 225)) # Y abaixo do título

        # Seletor de número de jogadores (Botões Redondos)
        for btn in botoes_num:
            cor_fundo = Config.PRETO if btn['num'] == num_jogadores else Config.BRANCO
            cor_texto = Config.BRANCO if btn['num'] == num_jogadores else Config.PRETO
            
            # Desenha o círculo
            pygame.draw.circle(tela, cor_fundo, btn['rect'].center, BTN_RAIO)
            # Desenha a borda
            pygame.draw.circle(tela, Config.PRETO, btn['rect'].center, BTN_RAIO, 1) 
            
            # Desenha o número
            num_surf = fonte_num_botao.render(str(btn['num']), True, cor_texto)
            num_rect = num_surf.get_rect(center=btn['rect'].center)
            tela.blit(num_surf, num_rect)
        
        # Desenha as caixas de texto
        label_x_pos = box_x_central - 130 # Posição X para os labels "Jogador X:"
        
        for i, box in enumerate(text_boxes):
            label = fonte_normal.render(f"Jogador {i+1}:", True, Config.PRETO)
            # Alinha o Y do label ao centro da caixa de texto
            label_y = box.rect.y + (box.rect.height - label.get_height()) // 2
            tela.blit(label, (label_x_pos, label_y))
            box.draw(tela)

        # Botão Iniciar (com cantos arredondados)
        pygame.draw.rect(tela, (0, 100, 200), btn_iniciar, border_radius=btn_iniciar_radius)
        iniciar_render = fonte_normal.render("INICIAR JOGO", True, Config.BRANCO)
        iniciar_rect = iniciar_render.get_rect(center=btn_iniciar.center)
        tela.blit(iniciar_render, iniciar_rect)

        pygame.display.flip()
        relogio.tick(60)

    # --- Fim do Loop: Coleta os dados ---
    nomes_finais = []
    for i, box in enumerate(text_boxes):
        nome = box.get_text().strip()
        if not nome:
            nome = f"Jogador {i + 1}" 
        nomes_finais.append(nome)

    pygame.quit() 
    return nomes_finais