import pygame
from config import Config
from collections import deque

class EventoUI:
    def __init__(self, tela):
        self.tela = tela
        self.eventos = deque(maxlen=20)
        self.fonte = pygame.font.Font(None, 24)
        self.largura = 175
        self.altura = 300

        board_end_x = Config.POS_X_INICIO + Config.TAMANHO_TABULEIRO
        largura_tela = Config.LARGURA_TELA
        proporcao_painel = 0.30
        margem_painel = 16
        largura_painel_calc = max(240, int(largura_tela * proporcao_painel))
        largura_painel_calc = min(int(largura_tela * 0.45), largura_painel_calc)
        panel_start_x = largura_tela - largura_painel_calc - margem_painel
        
        gap_width = panel_start_x - board_end_x
        centro_gap_x = board_end_x + (gap_width // 2)
        
        self.x = centro_gap_x - self.largura // 2
        self.y = Config.POS_Y_INICIO + 20

    def adicionar_evento(self, texto):
        self.eventos.append(texto)
    
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
        
        fonte_evento = pygame.font.Font(None, 20)
        largura_disponivel = self.largura - 20
        altura_linha = 20
        y_offset = 40
        
        altura_disponivel = self.altura - y_offset - 10
        max_linhas = int(altura_disponivel / altura_linha)
        
        eventos_para_mostrar = list(reversed(self.eventos))[:max_linhas]
        
        for evento in eventos_para_mostrar:
            texto_cortado = evento
            texto_render = fonte_evento.render(texto_cortado, True, Config.BRANCO)
            
            while texto_render.get_width() > largura_disponivel and len(texto_cortado) > 3:
                texto_cortado = texto_cortado[:-1]
                texto_render = fonte_evento.render(texto_cortado + "...", True, Config.BRANCO)
            
            if len(texto_cortado) <= 3:
                texto_render = fonte_evento.render("...", True, Config.BRANCO)
            
            self.tela.blit(texto_render, (self.x + 10, self.y + y_offset))
            y_offset += altura_linha


class PopupEventosUI:
    """
    Popup não-modal e temporário para destacar eventos importantes (cartas, vá para a cadeia, etc.).
    """
    def __init__(self, tela):
        self.tela = tela
        self.fonte_titulo = pygame.font.Font(None, 42)
        self.fonte_texto = pygame.font.Font(None, 28)
        self.fila = []
        self.duracao_padrao = 2200  # ms

    def mostrar(self, mensagem: str, cor=(30, 30, 30), duracao_ms: int | None = None):
        try:
            dur = duracao_ms if duracao_ms is not None else self.duracao_padrao
            self.fila.append({
                'msg': mensagem,
                'inicio': pygame.time.get_ticks(),
                'duracao': dur,
                'cor': cor
            })
        except Exception:
            pass

    def desenhar(self):
        agora = pygame.time.get_ticks()
        self.fila = [p for p in self.fila if agora - p['inicio'] < p['duracao']]
        if not self.fila:
            return
        p = self.fila[0]
        tempo = agora - p['inicio']
        alpha = 230
        rest = p['duracao'] - tempo
        if rest < 400:
            alpha = max(0, int(230 * (rest / 400)))
        msg = p['msg']
        max_largura_base = 900
        fonte_base = self.fonte_titulo
        palavras = msg.split(' ')
        linhas = []
        linha_atual = ''
        for palavra in palavras:
            teste = (linha_atual + ' ' + palavra).strip()
            if fonte_base.size(teste)[0] <= max_largura_base - 60:  # margem horizontal
                linha_atual = teste
            else:
                if linha_atual:
                    linhas.append(linha_atual)
                linha_atual = palavra
        if linha_atual:
            linhas.append(linha_atual)
        fonte_render = fonte_base
        if len(linhas) > 2:
            fonte_render = pygame.font.Font(None, 34)
        if len(linhas) > 4:
            fonte_render = pygame.font.Font(None, 28)
        larguras_linhas = [fonte_render.size(l)[0] for l in linhas]
        largura_texto = max(larguras_linhas) if larguras_linhas else 400
        largura = min(max(largura_texto + 60, 500), 1000)
        altura = 40 + len(linhas) * (fonte_render.get_height() + 6)
        altura = max(120, min(altura, 280))
        x = (Config.LARGURA_TELA - largura) // 2
        y = (Config.ALTURA_TELA - altura) // 2
        overlay = pygame.Surface((Config.LARGURA_TELA, Config.ALTURA_TELA))
        overlay.set_alpha(80)
        overlay.fill((0, 0, 0))
        self.tela.blit(overlay, (0, 0))
        caixa = pygame.Surface((largura, altura), pygame.SRCALPHA)
        caixa.fill((0, 0, 0, 0))
        bg = pygame.Surface((largura, altura))
        bg.set_alpha(alpha)
        bg.fill((245, 245, 245))
        caixa.blit(bg, (0, 0))
        pygame.draw.rect(caixa, Config.PRETO, pygame.Rect(0, 0, largura, altura), 3, border_radius=14)
        y_linha = (altura - len(linhas) * fonte_render.get_height()) // 2
        for linha in linhas:
            texto = fonte_render.render(linha, True, (20, 20, 20))
            caixa.blit(texto, texto.get_rect(center=(largura // 2, y_linha + fonte_render.get_height()//2)))
            y_linha += fonte_render.get_height() + 6
        self.tela.blit(caixa, (x, y))


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

class DialogoInfoPropriedadeUI:
    def __init__(self, tela):
        self.tela = tela
        self.ativo = False
        self.propriedade = None
        self.font_titulo = pygame.font.Font(None, 34)
        self.font_texto = pygame.font.Font(None, 22)
        self.largura = 520
        self.altura = 400
        self.x = (Config.LARGURA_TELA - self.largura)//2
        self.y = (Config.ALTURA_TELA - self.altura)//2
        self.btn_fechar = pygame.Rect(0,0,0,0)

    def mostrar(self, propriedade):
        self.propriedade = propriedade
        self.ativo = True
        self.btn_fechar = pygame.Rect(self.x + self.largura - 130, self.y + 20, 110, 40)

    def handle_event(self, e):
        if not self.ativo:
            return
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.btn_fechar.collidepoint(e.pos):
                self.ativo = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.ativo = False

    def desenhar(self):
        if not self.ativo or not self.propriedade:
            return
        overlay = pygame.Surface((Config.LARGURA_TELA, Config.ALTURA_TELA))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        self.tela.blit(overlay,(0,0))
        rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(self.tela, (245,245,245), rect, border_radius=10)
        pygame.draw.rect(self.tela, Config.PRETO, rect, 3, border_radius=10)

        nome = self.propriedade.getNome() if hasattr(self.propriedade, 'getNome') else 'Propriedade'
        t = self.font_titulo.render(nome, True, Config.PRETO)
        self.tela.blit(t, t.get_rect(center=(self.x + self.largura//2, self.y + 50)))

        linhas = []
        # Tipo específico
        tipo_str = None
        try:
            from modules.tituloPropriedade import TituloPropriedade
            from modules.tituloCompanhia import TituloCompanhia
            from modules.tituloEstacao import TituloEstacao
            if isinstance(self.propriedade, TituloPropriedade):
                tipo_str = "Propriedade"
            elif isinstance(self.propriedade, TituloCompanhia):
                tipo_str = "Companhia"
            elif isinstance(self.propriedade, TituloEstacao):
                tipo_str = "Estação"
        except Exception:
            pass

        try:
            preco = self.propriedade.getPreco()
            linhas.append(f"Preço: R$ {preco}")
        except:
            pass

        # Monta linhas de acordo com o tipo
        try:
            from modules.tituloPropriedade import TituloPropriedade
            from modules.tituloCompanhia import TituloCompanhia
            from modules.tituloEstacao import TituloEstacao
            prop = self.propriedade
            if isinstance(prop, TituloPropriedade):
                if hasattr(prop, 'getAluguelBase'):
                    linhas.append(f"Aluguel base: R$ {prop.getAluguelBase()}")
                if hasattr(prop, 'getAlugueis'):
                    alugueis = prop.getAlugueis()
                    # alugueis indices: [0]=aluguel com 0 casas? Em TituloPropriedade, lista passou valores [aluguel_base?], mas já temos base
                    # Exibir 1 a 4 casas e hotel (5º)
                    if len(alugueis) >= 5:
                        for i in range(1, 5):
                            linhas.append(f"Com {i} casa(s): R$ {alugueis[i]}")
                        # Hotel
                        linhas.append(f"Com hotel: R$ {alugueis[5] if len(alugueis) > 5 else alugueis[-1]}")
                if hasattr(prop, 'getCustoCasa'):
                    linhas.append(f"Custo casa/hotel: R$ {prop.getCustoCasa()}")
            elif isinstance(prop, TituloEstacao):
                # Estação: aluguel por 1-4 estações
                try:
                    alugueis = prop.getAlugueis()
                    linhas.append("Aluguéis por número de estações:")
                    linhas.append(f" - 1 estação: R$ {alugueis[0]}")
                    linhas.append(f" - 2 estações: R$ {alugueis[1]}")
                    linhas.append(f" - 3 estações: R$ {alugueis[2]}")
                    linhas.append(f" - 4 estações: R$ {alugueis[3]}")
                except:
                    pass
            elif isinstance(prop, TituloCompanhia):
                # Companhia: fórmula baseada nos dados e fatores
                try:
                    linhas.append("Aluguel: soma dos dados × fator")
                    linhas.append(f" - 1 companhia: ×{prop.getFatorUmaCompanhia()}")
                    linhas.append(f" - 2 companhias: ×{prop.getFatorDuasCompanhias()}")
                except:
                    pass
        except Exception:
            pass

        # Status hipoteca e valores comuns
        try:
            if hasattr(self.propriedade, 'estaHipotecada') and self.propriedade.estaHipotecada():
                linhas.append("Status: HIPOTECADA")
        except:
            pass
        try:
            valor_hipoteca = int(self.propriedade.getPreco() / 2)
            linhas.append(f"Hipoteca: R$ {valor_hipoteca}")
        except:
            pass
        if tipo_str:
            linhas.insert(0, f"Tipo: {tipo_str}")

        y_text = self.y + 100
        for linha in linhas:
            r = self.font_texto.render(linha, True, Config.PRETO)
            self.tela.blit(r, (self.x + 40, y_text))
            y_text += 28

        mouse = pygame.mouse.get_pos()
        cor_b = (140,0,0) if self.btn_fechar.collidepoint(mouse) else (120,0,0)
        pygame.draw.rect(self.tela, cor_b, self.btn_fechar, border_radius=8)
        pygame.draw.rect(self.tela, Config.PRETO, self.btn_fechar, 2, border_radius=8)
        txb = self.font_texto.render("Fechar", True, (255,255,255))
        self.tela.blit(txb, txb.get_rect(center=self.btn_fechar.center))