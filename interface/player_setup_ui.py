import pygame
from interface.config import Config
import os
from modules.peca import Peca

class TextInputBox:
    def __init__(self, x, y, w, h, fonte_texto, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = Config.CINZA_CLARO
        self.color_active = Config.PRETO
        self.color = self.color_inactive
        self.text = text
        self.fonte = fonte_texto
        self.active = False
        self.is_default = True 
        self.border_radius = int(h * 0.33)
        
    def handle_event(self, event):
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
        pygame.draw.rect(screen, Config.BRANCO, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=self.border_radius)
        
        txt_surface = self.fonte.render(self.text, True, Config.PRETO)
        text_y = self.rect.y + (self.rect.height - txt_surface.get_height()) // 2
        padding_x = int(self.rect.width * 0.033) 
        screen.blit(txt_surface, (self.rect.x + padding_x, text_y))
        
    def get_text(self):
        return self.text


class PieceSelector:
    def __init__(self, x, y, w, h, fonte_peca, fonte_setas, caminho_assets_pecas):
        self.rect = pygame.Rect(x, y, w, h)
        self.pecas_disponiveis = list(Peca)
        self.indice_atual = 0
        self.fonte_peca = fonte_peca
        self.fonte_setas = fonte_setas
        self.caminho_assets = caminho_assets_pecas
                
        self.visual_width = int(w * 0.6)
        self.image_size = int(h * 0.95)
        self.image_center_pos = (x + self.visual_width // 2, y + h // 2)
        
        self.placeholder_rect = pygame.Rect(0, 0, self.image_size, self.image_size)
        self.placeholder_rect.center = self.image_center_pos

        btn_w = int(w * 0.15)
        self.btn_anterior = pygame.Rect(x, y, btn_w, h)
        self.btn_proximo = pygame.Rect(x + self.visual_width - btn_w, y, btn_w, h)
        
        self.circle_radius = int(h * 0.23)
        self.circle_center_x = x + self.visual_width + int(w*0.05)
        self.circle_center_y = y + h // 2
        
        self.text_start_x = self.circle_center_x + self.circle_radius + int(w*0.03)
        
        self.image_cache = {}
        
    def get_selected_piece(self) -> Peca:
        return self.pecas_disponiveis[self.indice_atual]

    def set_indice(self, indice):
        self.indice_atual = indice % len(self.pecas_disponiveis)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_anterior.collidepoint(event.pos):
                self.indice_atual = (self.indice_atual - 1) % len(self.pecas_disponiveis)
                return True
            if self.btn_proximo.collidepoint(event.pos):
                self.indice_atual = (self.indice_atual + 1) % len(self.pecas_disponiveis)
                return True
        return False

    def draw(self, screen):
        seta_anterior_render = self.fonte_setas.render("<", True, Config.PRETO)
        screen.blit(seta_anterior_render, seta_anterior_render.get_rect(center=self.btn_anterior.center))
        
        seta_proxima_render = self.fonte_setas.render(">", True, Config.PRETO)
        screen.blit(seta_proxima_render, seta_proxima_render.get_rect(center=self.btn_proximo.center))
        
        peca_selecionada = self.get_selected_piece()
        nome_imagem = f"{peca_selecionada.name}.png" 
        cor_da_peca = Config.CORES_PECAS.get(peca_selecionada, Config.CINZA_CLARO)
        
        imagem_carregada = self.image_cache.get(nome_imagem)
        
        if not imagem_carregada:
            try:
                caminho_completo = os.path.join(self.caminho_assets, nome_imagem)
                img = pygame.image.load(caminho_completo).convert_alpha()
                img = pygame.transform.smoothscale(img, (self.placeholder_rect.width - 10, self.placeholder_rect.height - 10))
                self.image_cache[nome_imagem] = img
                imagem_carregada = img
            except Exception as e:
                self.image_cache[nome_imagem] = False 
        
        if imagem_carregada:
            screen.blit(imagem_carregada, imagem_carregada.get_rect(center=self.placeholder_rect.center))
        else:
            pygame.draw.rect(screen, Config.CINZA_CLARO, self.placeholder_rect)
            pygame.draw.rect(screen, Config.PRETO, self.placeholder_rect, 1)

        nome_peca = peca_selecionada.value 

        pygame.draw.circle(screen, cor_da_peca, (self.circle_center_x, self.circle_center_y), self.circle_radius)
        pygame.draw.circle(screen, Config.PRETO, (self.circle_center_x, self.circle_center_y), self.circle_radius, 1)

        nome_render = self.fonte_peca.render(nome_peca, True, Config.PRETO)
        nome_rect = nome_render.get_rect(left=self.text_start_x, centery=self.rect.centery)
        screen.blit(nome_render, nome_rect)


def rodar_setup_ui():
    pygame.init()
    
    TELA_W = Config.LARGURA_TELA
    TELA_H = Config.ALTURA_TELA
    tela = pygame.display.set_mode((TELA_W, TELA_H))
    pygame.display.set_caption("Configurar Jogo - Monopoly Uffiano")
    relogio = pygame.time.Clock()
    pygame.key.set_repeat(300, 30)
    
    caminho_base = os.path.dirname(__file__) # .../interface
    caminho_raiz = os.path.join(caminho_base, '..') 
    caminho_imagem_lobby = os.path.join(caminho_raiz, 'assets', 'lobby.png')
    caminho_assets_pecas = os.path.join(caminho_raiz, 'assets', 'pecas') # Caminho para as peças
    
    background_image = pygame.image.load(caminho_imagem_lobby)
    background_image = pygame.transform.scale(background_image, (Config.LARGURA_TELA, Config.ALTURA_TELA))

    fonte_titulo = pygame.font.Font(None, int(TELA_H * 0.071))
    fonte_label = pygame.font.Font(None, int(TELA_H * 0.04))
    fonte_normal = pygame.font.Font(None, int(TELA_H * 0.04))
    fonte_input = pygame.font.Font(None, int(TELA_H * 0.04))
    fonte_num_botao = pygame.font.Font(None, int(TELA_H * 0.034))
    fonte_peca = pygame.font.Font(None, int(TELA_H * 0.031))
    fonte_setas = pygame.font.Font(None, int(TELA_H * 0.051))
    
    # --- Configuração Botões de Número (2-8) ---
    num_jogadores = 2
    botoes_num = []
    BTN_RAIO = int(TELA_H * 0.028)
    BTN_SPACING = int(TELA_W * 0.0125)
    NUM_BOTOES = 7 
    
    total_largura_botoes = (NUM_BOTOES * (BTN_RAIO * 2)) + ((NUM_BOTOES - 1) * BTN_SPACING)
    start_x = (TELA_W - total_largura_botoes) // 2
    botoes_y = int(TELA_H * 0.314)

    for i in range(NUM_BOTOES):
        num = i + 2
        centro_x = start_x + (i * (BTN_RAIO * 2 + BTN_SPACING)) + BTN_RAIO
        botoes_num.append({'rect': pygame.Rect(centro_x - BTN_RAIO, botoes_y - BTN_RAIO, BTN_RAIO * 2, BTN_RAIO * 2), 'num': num})

    text_boxes = []
    piece_selectors = []
    
    BOX_WIDTH = int(TELA_W * 0.25)
    BOX_HEIGHT = int(TELA_H * 0.042)
    SELECTOR_WIDTH = int(TELA_W * 0.166)
    SELECTOR_HEIGHT = int(TELA_H * 0.078)
    BOX_SPACING = int(TELA_H * 0.062)
    
    # Layout centralizado
    label_width = int(TELA_W * 0.108)
    spacing_after_box = int(TELA_W * 0.016)
    total_linha_width = label_width + BOX_WIDTH + spacing_after_box + SELECTOR_WIDTH
    start_x_label = (TELA_W - total_linha_width) // 2
    start_x_box = start_x_label + label_width
    start_x_selector = start_x_box + BOX_WIDTH + spacing_after_box
    
    box_base_y = int(TELA_H * 0.357)
    pecas_disponiveis = list(Peca)

    def atualizar_componentes_jogador(num_selecionado):
        text_boxes.clear()
        piece_selectors.clear()
        for i in range(num_selecionado):
            y_pos_box = box_base_y + (i * BOX_SPACING)
            y_pos_selector = box_base_y + (i * BOX_SPACING) - (SELECTOR_HEIGHT - BOX_HEIGHT)//2

            text_boxes.append(TextInputBox(start_x_box, y_pos_box, BOX_WIDTH, BOX_HEIGHT, fonte_input, text=f"Jogador {i + 1}"))
            
            selector = PieceSelector(start_x_selector, y_pos_selector, SELECTOR_WIDTH, SELECTOR_HEIGHT, fonte_peca, fonte_setas, caminho_assets_pecas)
            selector.set_indice(i % len(pecas_disponiveis))
            piece_selectors.append(selector)

    atualizar_componentes_jogador(num_jogadores) 

    # --- Botão Iniciar ---
    BTN_INICIAR_W = int(TELA_W * 0.183)
    BTN_INICIAR_H = int(TELA_H * 0.085) 
    btn_iniciar_y = int(TELA_H * 0.857)
    btn_iniciar = pygame.Rect((TELA_W - BTN_INICIAR_W) // 2, btn_iniciar_y, BTN_INICIAR_W, BTN_INICIAR_H)
    btn_iniciar_radius = int(TELA_H * 0.021)
    erro_duplicado = False

    rodando = True
    while rodando:
        
        pecas_selecionadas = set()
        erro_duplicado = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                return None 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_iniciar.collidepoint(event.pos) and not erro_duplicado:
                    rodando = False 
                    
                for btn in botoes_num:
                    if btn['rect'].collidepoint(event.pos):
                        if num_jogadores != btn['num']:
                            num_jogadores = btn['num']
                            atualizar_componentes_jogador(num_jogadores)
            
            for box in text_boxes:
                box.handle_event(event)
            for selector in piece_selectors:
                selector.handle_event(event)

        tela.blit(background_image, (0, 0))
        
        titulo_y = int(TELA_H * 0.19)
        label_y = int(TELA_H * 0.24)

        titulo_render = fonte_titulo.render("CONFIGURAR JOGO", True, Config.PRETO)
        tela.blit(titulo_render, (TELA_W // 2 - titulo_render.get_width() // 2, titulo_y))

        label_render = fonte_label.render("Selecione a quantidade de jogadores", True, Config.PRETO)
        tela.blit(label_render, (TELA_W // 2 - label_render.get_width() // 2, label_y))
        
        # Seletor de número de jogadores (Botões Redondos)
        for btn in botoes_num:
            cor_fundo = Config.PRETO if btn['num'] == num_jogadores else Config.BRANCO
            cor_texto = Config.BRANCO if btn['num'] == num_jogadores else Config.PRETO
            pygame.draw.circle(tela, cor_fundo, btn['rect'].center, BTN_RAIO)
            pygame.draw.circle(tela, Config.PRETO, btn['rect'].center, BTN_RAIO, 1) 
            num_surf = fonte_num_botao.render(str(btn['num']), True, cor_texto)
            num_rect = num_surf.get_rect(center=btn['rect'].center)
            tela.blit(num_surf, num_rect)
        
        pecas_selecionadas.clear()
        
        for i in range(num_jogadores):
            box = text_boxes[i]
            selector = piece_selectors[i]
            
            peca = selector.get_selected_piece()
            if peca in pecas_selecionadas:
                erro_duplicado = True
            pecas_selecionadas.add(peca)
            
            label = fonte_normal.render(f"Jogador {i+1}:", True, Config.PRETO)
            label_y = box.rect.y + (box.rect.height - label.get_height()) // 2
            tela.blit(label, (start_x_label, label_y))
            
            box.draw(tela)
            selector.draw(tela)

        cor_botao_iniciar = (150, 150, 150) if erro_duplicado else (0, 100, 200)
        pygame.draw.rect(tela, cor_botao_iniciar, btn_iniciar, border_radius=btn_iniciar_radius)
        
        texto_botao = "INICIAR JOGO"
        if erro_duplicado:
            texto_botao = "Peças duplicadas!"
            
        iniciar_render = fonte_normal.render(texto_botao, True, Config.BRANCO)
        iniciar_rect = iniciar_render.get_rect(center=btn_iniciar.center)
        tela.blit(iniciar_render, iniciar_rect)

        pygame.display.flip()
        relogio.tick(60)

    dados_finais = []
    for i in range(num_jogadores):
        nome = text_boxes[i].get_text().strip()
        if not nome or text_boxes[i].is_default:
            nome = f"Jogador {i + 1}" 
        
        peca = piece_selectors[i].get_selected_piece()
        dados_finais.append((nome, peca))

    pygame.key.set_repeat(0)
    pygame.quit() 
    return dados_finais