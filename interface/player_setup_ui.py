import pygame
from interface.config import Config
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
        self.active = False
        self.is_default = True 
        self.border_radius = 10 # <-- Arredondamento

    def handle_event(self, event):
        """Processa eventos de mouse e teclado."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if not self.active: 
                    self.active = True
                    if self.is_default:
                        self.text = "" 
                        self.is_default = False
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                self.is_default = False
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = self.color_inactive
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        """Desenha a caixa de texto na tela com cantos arredondados."""
        pygame.draw.rect(screen, Config.BRANCO, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=self.border_radius)
        
        txt_surface = self.fonte.render(self.text, True, Config.PRETO)
        text_y = self.rect.y + (self.rect.height - txt_surface.get_height()) // 2
        screen.blit(txt_surface, (self.rect.x + 10, text_y))

    def get_text(self):
        return self.text


class PieceSelector:
    """
    Widget de UI para selecionar uma Peça do Monopoly com setas.
    """
    def __init__(self, x, y, w, h, fonte_peca, fonte_setas, caminho_assets_pecas):
        # O rect (x,y,w,h) agora representa a ÁREA TOTAL do widget, 
        # incluindo o texto à direita.
        self.rect = pygame.Rect(x, y, w, h)
        self.pecas_disponiveis = list(Peca)
        self.indice_atual = 0
        self.fonte_peca = fonte_peca
        self.fonte_setas = fonte_setas
        self.caminho_assets = caminho_assets_pecas
        
        # --- MUDANÇA 1: Redefinir layout interno ---
        
        # 1. Área da Imagem/Setas (à esquerda)
        self.visual_width = 120  # Largura fixa para a parte [<] [IMG] [>]
        self.image_size = h - 1  # Tamanho quadrado 1:1 para a imagem
        self.image_center_pos = (x + self.visual_width // 2, y + h // 2)
        
        
        self.placeholder_rect = pygame.Rect(0, 0, self.image_size, self.image_size)
        self.placeholder_rect.center = self.image_center_pos

        
        self.btn_anterior = pygame.Rect(x, y, 30, h)
        self.btn_proximo = pygame.Rect(x + self.visual_width - 30, y, 30, h)
        
       
        self.circle_radius = 13
        self.circle_center_x = x + self.visual_width + 10 
        self.circle_center_y = y + h // 2
        
        self.text_start_x = self.circle_center_x + self.circle_radius + 6
        

        self.image_cache = {}
        
    def get_selected_piece(self) -> Peca:
        """Retorna o Enum Peca atualmente selecionado."""
        return self.pecas_disponiveis[self.indice_atual]

    def set_indice(self, indice):
        """Define o índice (usado para definir peças padrão)."""
        self.indice_atual = indice % len(self.pecas_disponiveis)

    def handle_event(self, event):
        """Processa cliques nos botões de seta."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_anterior.collidepoint(event.pos):
                self.indice_atual = (self.indice_atual - 1) % len(self.pecas_disponiveis)
                return True # Indica que houve mudança
            if self.btn_proximo.collidepoint(event.pos):
                self.indice_atual = (self.indice_atual + 1) % len(self.pecas_disponiveis)
                return True # Indica que houve mudança
        return False

    def draw(self, screen):
        """Desenha o seletor (setas, placeholder/imagem e nome)."""
        # Desenha setas
        seta_anterior_render = self.fonte_setas.render("<", True, Config.PRETO)
        screen.blit(seta_anterior_render, seta_anterior_render.get_rect(center=self.btn_anterior.center))
        
        seta_proxima_render = self.fonte_setas.render(">", True, Config.PRETO)
        screen.blit(seta_proxima_render, seta_proxima_render.get_rect(center=self.btn_proximo.center))
        

        # --- Lógica para desenhar Placeholder ou Imagem Real ---
        peca_selecionada = self.get_selected_piece()
        # Usa Peca.ARTES.name -> "ARTES"
        nome_imagem = f"{peca_selecionada.name}.png" 
        cor_da_peca = Config.CORES_PECAS.get(peca_selecionada, Config.CINZA_CLARO)
        
        imagem_carregada = self.image_cache.get(nome_imagem)
        
        if not imagem_carregada:
            try:
                caminho_completo = os.path.join(self.caminho_assets, nome_imagem)
                img = pygame.image.load(caminho_completo).convert_alpha()
                img = pygame.transform.scale(img, (self.placeholder_rect.width - 10, self.placeholder_rect.height - 10))
                self.image_cache[nome_imagem] = img
                imagem_carregada = img
            except Exception as e:
                # Se falhar (ex: imagem não encontrada), armazena False no cache
                self.image_cache[nome_imagem] = False 
        
        if imagem_carregada:
            # Desenha a imagem real
            screen.blit(imagem_carregada, imagem_carregada.get_rect(center=self.placeholder_rect.center))
        else:
            # Desenha o retângulo genérico (placeholder)
            pygame.draw.rect(screen, Config.CINZA_CLARO, self.placeholder_rect)
            pygame.draw.rect(screen, Config.PRETO, self.placeholder_rect, 1)
        # -------------------------------------

        nome_peca = peca_selecionada.value 

        # 1. Desenha a bolinha
        pygame.draw.circle(screen, cor_da_peca, (self.circle_center_x, self.circle_center_y), self.circle_radius)
        pygame.draw.circle(screen, Config.PRETO, (self.circle_center_x, self.circle_center_y), self.circle_radius, 1) # Borda

        # 2. Desenha o nome
        nome_render = self.fonte_peca.render(nome_peca, True, Config.PRETO)
        
        # Coloca o nome AO LADO da bolinha, centralizado verticalmente
        nome_rect = nome_render.get_rect(left=self.text_start_x, centery=self.rect.centery)
        screen.blit(nome_render, nome_rect)


def rodar_setup_ui():
    """
    Executa o loop da tela de setup (lobby) e retorna uma lista de tuplas (nome, peca).
    Retorna None se o usuário fechar a janela.
    """
    pygame.init()
    tela = pygame.display.set_mode((Config.LARGURA_TELA, Config.ALTURA_TELA))
    pygame.display.set_caption("Configurar Jogo - Monopoly Uffiano")
    relogio = pygame.time.Clock()
    pygame.key.set_repeat(300, 30)
    
    # --- Caminhos e Imagens ---
    caminho_base = os.path.dirname(__file__) # .../interface
    caminho_raiz = os.path.join(caminho_base, '..') # .../
    caminho_imagem_lobby = os.path.join(caminho_raiz, 'assets', 'lobby.png')
    caminho_assets_pecas = os.path.join(caminho_raiz, 'assets', 'pecas') # <-- Caminho para as peças
    
    background_image = pygame.image.load(caminho_imagem_lobby)
    background_image = pygame.transform.scale(background_image, (Config.LARGURA_TELA, Config.ALTURA_TELA))


    fonte_titulo = pygame.font.Font(None, 50) 
    fonte_label = pygame.font.Font(None, 28)  
    fonte_normal = pygame.font.Font(None, 28) 
    fonte_input = pygame.font.Font(None, 28)  
    fonte_num_botao = pygame.font.Font(None, 24)
    fonte_peca = pygame.font.Font(None, 22) # Fonte para nome da peça
    fonte_setas = pygame.font.Font(None, 36) # Fonte para setas < >

    # --- Configuração Botões de Número (2-8) ---
    num_jogadores = 2
    botoes_num = []
    BTN_RAIO = 20
    BTN_SPACING = 15
    NUM_BOTOES = 7 
    
    total_largura_botoes = (NUM_BOTOES * (BTN_RAIO * 2)) + ((NUM_BOTOES - 1) * BTN_SPACING)
    start_x = (Config.LARGURA_TELA - total_largura_botoes) // 2
    botoes_y = 220 # Posição Y dos botões

    for i in range(NUM_BOTOES):
        num = i + 2
        centro_x = start_x + (i * (BTN_RAIO * 2 + BTN_SPACING)) + BTN_RAIO
        botoes_num.append({'rect': pygame.Rect(centro_x - BTN_RAIO, botoes_y - BTN_RAIO, BTN_RAIO * 2, BTN_RAIO * 2), 'num': num})

    # --- Configuração Linhas de Jogador (Caixa de Texto + Seletor de Peça) ---
    text_boxes = []
    piece_selectors = [] # <-- Lista para seletores
    
    BOX_WIDTH = 300 # Largura reduzida
    BOX_HEIGHT = 30
    SELECTOR_WIDTH = 200 # Largura do seletor
    SELECTOR_HEIGHT = 55
    BOX_SPACING = 44
    
    # Centraliza o conjunto (Label + Caixa + Seletor)
    total_linha_width = 130 + BOX_WIDTH + SELECTOR_WIDTH + 20 # (Label + Caixa + Espaço + Seletor)
    start_x_label = (Config.LARGURA_TELA - total_linha_width) // 2
    start_x_box = start_x_label + 130
    start_x_selector = start_x_box + BOX_WIDTH + 20
    
    box_base_y = 250
    pecas_disponiveis = list(Peca)

    def atualizar_componentes_jogador(num_selecionado):
        """Atualiza ambas as listas: text_boxes e piece_selectors."""
        text_boxes.clear()
        piece_selectors.clear()
        for i in range(num_selecionado):
            y_pos_box = box_base_y + (i * BOX_SPACING)
            y_pos_selector = box_base_y + (i * BOX_SPACING) - (SELECTOR_HEIGHT - BOX_HEIGHT)//2

            text_boxes.append(TextInputBox(start_x_box, y_pos_box, BOX_WIDTH, BOX_HEIGHT, fonte_input, text=f"Jogador {i + 1}"))
            
            selector = PieceSelector(start_x_selector, y_pos_selector, SELECTOR_WIDTH, SELECTOR_HEIGHT, fonte_peca, fonte_setas, caminho_assets_pecas)
            selector.set_indice(i % len(pecas_disponiveis)) # Define peça inicial (0, 1, 2...)
            piece_selectors.append(selector)

    atualizar_componentes_jogador(num_jogadores) 

    # --- Botão Iniciar ---
    BTN_INICIAR_W = 220
    BTN_INICIAR_H = 60
    btn_iniciar = pygame.Rect((Config.LARGURA_TELA - BTN_INICIAR_W) // 2, 600, BTN_INICIAR_W, BTN_INICIAR_H)
    btn_iniciar_radius = 15
    erro_duplicado = False

    rodando = True
    while rodando:
        
        pecas_selecionadas = set()
        erro_duplicado = False
        
        # --- Processamento de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                return None 

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Botão Iniciar Jogo (só funciona se não houver erro)
                if btn_iniciar.collidepoint(event.pos) and not erro_duplicado:
                    rodando = False 
                    
                # Botões de Número (2-8)
                for btn in botoes_num:
                    if btn['rect'].collidepoint(event.pos):
                        if num_jogadores != btn['num']:
                            num_jogadores = btn['num']
                            atualizar_componentes_jogador(num_jogadores)
            
            # Passa eventos para as caixas de texto
            for box in text_boxes:
                box.handle_event(event)
            # Passa eventos para os seletores de peça
            for selector in piece_selectors:
                selector.handle_event(event)

        # --- Lógica de Desenho ---
        tela.blit(background_image, (0, 0))

        # Título
        titulo_render = fonte_titulo.render("CONFIGURAR JOGO", True, Config.PRETO)
        tela.blit(titulo_render, (Config.LARGURA_TELA // 2 - titulo_render.get_width() // 2, 133)) # Y mais alto

        # Label "Selecione..."
        label_render = fonte_label.render("Selecione a quantidade de jogadores", True, Config.PRETO)
        tela.blit(label_render, (Config.LARGURA_TELA // 2 - label_render.get_width() // 2, 170)) # Y abaixo do título

        # Seletor de número de jogadores (Botões Redondos)
        for btn in botoes_num:
            cor_fundo = Config.PRETO if btn['num'] == num_jogadores else Config.BRANCO
            cor_texto = Config.BRANCO if btn['num'] == num_jogadores else Config.PRETO
            pygame.draw.circle(tela, cor_fundo, btn['rect'].center, BTN_RAIO)
            pygame.draw.circle(tela, Config.PRETO, btn['rect'].center, BTN_RAIO, 1) 
            num_surf = fonte_num_botao.render(str(btn['num']), True, cor_texto)
            num_rect = num_surf.get_rect(center=btn['rect'].center)
            tela.blit(num_surf, num_rect)
        
        # Desenha as caixas de texto e seletores
        pecas_selecionadas.clear()
        
        for i in range(num_jogadores):
            box = text_boxes[i]
            selector = piece_selectors[i]
            
            # Checa duplicatas
            peca = selector.get_selected_piece()
            if peca in pecas_selecionadas:
                erro_duplicado = True
            pecas_selecionadas.add(peca)
            
            # Label "Jogador X:"
            label = fonte_normal.render(f"Jogador {i+1}:", True, Config.PRETO)
            label_y = box.rect.y + (box.rect.height - label.get_height()) // 2
            tela.blit(label, (start_x_label, label_y))
            
            # Caixa de Texto
            box.draw(tela)
            # Seletor de Peça
            selector.draw(tela)

        # Botão Iniciar (com cantos arredondados)
        cor_botao_iniciar = (150, 150, 150) if erro_duplicado else (0, 100, 200) # Cinza se houver erro
        pygame.draw.rect(tela, cor_botao_iniciar, btn_iniciar, border_radius=btn_iniciar_radius)
        
        texto_botao = "INICIAR JOGO"
        if erro_duplicado:
            texto_botao = "Peças duplicadas!" # Mostra erro
            
        iniciar_render = fonte_normal.render(texto_botao, True, Config.BRANCO)
        iniciar_rect = iniciar_render.get_rect(center=btn_iniciar.center)
        tela.blit(iniciar_render, iniciar_rect)

        pygame.display.flip()
        relogio.tick(60)

    # --- Fim do Loop: Coleta os dados ---
    dados_finais = []
    for i in range(num_jogadores):
        nome = text_boxes[i].get_text().strip()
        if not nome or text_boxes[i].is_default:
            nome = f"Jogador {i + 1}" 
        
        peca = piece_selectors[i].get_selected_piece()
        dados_finais.append((nome, peca)) # <-- Retorna (nome, peca)

    pygame.key.set_repeat(0)
    pygame.quit() 
    return dados_finais # <-- Retorna (nome, peca)