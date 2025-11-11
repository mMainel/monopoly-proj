import pygame
from config import Config

class DialogoConfirmacaoUI:
    def __init__(self, tela, titulo="Confirma?", mensagem="", texto_sim="SIM", texto_nao="NÃO"):
        self.tela = tela
        self.ativo = False
        self.resultado = None
        self.titulo = titulo
        self.mensagem = mensagem
        self.texto_sim = texto_sim
        self.texto_nao = texto_nao

        self.largura = 520
        self.altura = 220
        self.x = (Config.LARGURA_TELA - self.largura) // 2
        self.y = (Config.ALTURA_TELA - self.altura) // 2

        self.fonte_titulo = pygame.font.Font(None, 36)
        self.fonte_texto = pygame.font.Font(None, 26)
        self.fonte_botao = pygame.font.Font(None, 28)

        btn_w = 140
        btn_h = 50
        gap = 30
        cx = self.x + self.largura // 2
        by = self.y + self.altura - 70
        self.btn_sim = pygame.Rect(cx - btn_w - gap//2, by, btn_w, btn_h)
        self.btn_nao = pygame.Rect(cx + gap//2, by, btn_w, btn_h)

    def mostrar(self, titulo, mensagem):
        self.titulo = titulo
        self.mensagem = mensagem
        self.resultado = None
        self.ativo = True

    def handle_event(self, evento):
        if not self.ativo:
            return
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.btn_sim.collidepoint(evento.pos):
                self.resultado = True
                self.ativo = False
            elif self.btn_nao.collidepoint(evento.pos):
                self.resultado = False
                self.ativo = False

    def obter_resposta(self):
        return self.resultado

    def desenhar(self):
        if not self.ativo:
            return
        overlay = pygame.Surface((Config.LARGURA_TELA, Config.ALTURA_TELA))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.tela.blit(overlay, (0, 0))

        rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(self.tela, (250, 250, 250), rect, border_radius=10)
        pygame.draw.rect(self.tela, Config.PRETO, rect, 3, border_radius=10)

        t = self.fonte_titulo.render(self.titulo, True, Config.PRETO)
        self.tela.blit(t, t.get_rect(center=(self.x + self.largura//2, self.y + 40)))

        msg = self.fonte_texto.render(self.mensagem, True, Config.PRETO)
        self.tela.blit(msg, msg.get_rect(center=(self.x + self.largura//2, self.y + 90)))

        mouse = pygame.mouse.get_pos()
        cor_sim = (0, 180, 0) if self.btn_sim.collidepoint(mouse) else (0, 150, 0)
        cor_nao = (180, 0, 0) if self.btn_nao.collidepoint(mouse) else (150, 0, 0)
        pygame.draw.rect(self.tela, cor_sim, self.btn_sim, border_radius=8)
        pygame.draw.rect(self.tela, Config.PRETO, self.btn_sim, 2, border_radius=8)
        pygame.draw.rect(self.tela, cor_nao, self.btn_nao, border_radius=8)
        pygame.draw.rect(self.tela, Config.PRETO, self.btn_nao, 2, border_radius=8)
        ts = self.fonte_botao.render(self.texto_sim, True, (255,255,255))
        tn = self.fonte_botao.render(self.texto_nao, True, (255,255,255))
        self.tela.blit(ts, ts.get_rect(center=self.btn_sim.center))
        self.tela.blit(tn, tn.get_rect(center=self.btn_nao.center))


class DialogoEscolherJogadorUI:
    def __init__(self, tela):
        self.tela = tela
        self.ativo = False
        self.alvo = None
        self.opcoes = []
        self.titulo_font = pygame.font.Font(None, 36)
        self.item_font = pygame.font.Font(None, 28)
        self.largura = 560
        self.altura = 380
        self.x = (Config.LARGURA_TELA - self.largura)//2
        self.y = (Config.ALTURA_TELA - self.altura)//2

    def mostrar(self, jogadores, atual):
        self.alvo = None
        self.ativo = True
        self._montar_opcoes(jogadores, atual)

    def _montar_opcoes(self, jogadores, atual):
        self.opcoes = []
        y = self.y + 90
        for j in jogadores:
            if j == atual:
                continue
            rect = pygame.Rect(self.x + 40, y, self.largura - 80, 48)
            self.opcoes.append((rect, j))
            y += 58

    def handle_event(self, evento):
        if not self.ativo:
            return
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for rect, j in self.opcoes:
                if rect.collidepoint(evento.pos):
                    self.alvo = j
                    self.ativo = False
                    break

    def obter_jogador(self):
        return self.alvo

    def desenhar(self):
        if not self.ativo:
            return
        overlay = pygame.Surface((Config.LARGURA_TELA, Config.ALTURA_TELA))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.tela.blit(overlay, (0, 0))

        rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(self.tela, (245,245,245), rect, border_radius=10)
        pygame.draw.rect(self.tela, Config.PRETO, rect, 3, border_radius=10)
        t = self.titulo_font.render("Quem você quer negociar?", True, Config.PRETO)
        self.tela.blit(t, t.get_rect(center=(self.x + self.largura//2, self.y + 40)))

        mouse = pygame.mouse.get_pos()
        for rect, j in self.opcoes:
            cor = (220,220,220) if rect.collidepoint(mouse) else (200,200,200)
            pygame.draw.rect(self.tela, cor, rect, border_radius=6)
            pygame.draw.rect(self.tela, Config.PRETO, rect, 2, border_radius=6)
            txt = self.item_font.render(j.getNome(), True, Config.PRETO)
            self.tela.blit(txt, txt.get_rect(center=rect.center))


class _InputNumero:
    def __init__(self, x, y, w, h, valor=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.valor = str(valor)
        self.ativo = False
        self.font = pygame.font.Font(None, 28)

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.ativo = self.rect.collidepoint(e.pos)
        if self.ativo and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_BACKSPACE:
                self.valor = self.valor[:-1]
            elif e.unicode.isdigit() and len(self.valor) < 7:
                if self.valor == "0":
                    self.valor = e.unicode
                else:
                    self.valor += e.unicode

    def get_valor(self):
        try:
            return int(self.valor) if self.valor else 0
        except:
            return 0

    def desenhar(self, tela):
        pygame.draw.rect(tela, (255,255,255), self.rect, border_radius=6)
        pygame.draw.rect(tela, (60,60,60), self.rect, 2, border_radius=6)
        txt = self.font.render(self.valor or "0", True, (0,0,0))
        tela.blit(txt, txt.get_rect(center=self.rect.center))


class DialogoNegociacaoUI:
    def __init__(self, tela):
        self.tela = tela
        self.ativo = False
        self.jog_a = None
        self.jog_b = None
        self.selecionadas_a = set()
        self.selecionadas_b = set()
        self.oferta_a = _InputNumero(0,0,0,0,0)
        self.oferta_b = _InputNumero(0,0,0,0,0)
        self.btn_confirmar = None
        self.btn_cancelar = None
        self.font_titulo = pygame.font.Font(None, 34)
        self.font_item = pygame.font.Font(None, 24)

        self.largura = 900
        self.altura = 520
        self.x = (Config.LARGURA_TELA - self.largura)//2
        self.y = (Config.ALTURA_TELA - self.altura)//2

    def mostrar(self, jog_a, jog_b):
        self.jog_a = jog_a
        self.jog_b = jog_b
        self.selecionadas_a = set()
        self.selecionadas_b = set()
        self.ativo = True

        # posicionar inputs e botões
        w = 140; h = 40
        self.oferta_a = _InputNumero(self.x + 160, self.y + self.altura - 90, w, h, 0)
        self.oferta_b = _InputNumero(self.x + self.largura - 160 - w, self.y + self.altura - 90, w, h, 0)
        self.btn_confirmar = pygame.Rect(self.x + self.largura//2 - 160, self.y + self.altura - 60, 140, 40)
        self.btn_cancelar = pygame.Rect(self.x + self.largura//2 + 20, self.y + self.altura - 60, 140, 40)

    def handle_event(self, e):
        if not self.ativo:
            return
        self.oferta_a.handle_event(e)
        self.oferta_b.handle_event(e)
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx, my = e.pos
            # Seleção de propriedades
            for idx, p in enumerate(self.jog_a.getPropriedades()):
                rect = self._rect_item_a(idx)
                if rect.collidepoint((mx, my)):
                    if p in self.selecionadas_a: self.selecionadas_a.remove(p)
                    else: self.selecionadas_a.add(p)
            for idx, p in enumerate(self.jog_b.getPropriedades()):
                rect = self._rect_item_b(idx)
                if rect.collidepoint((mx, my)):
                    if p in self.selecionadas_b: self.selecionadas_b.remove(p)
                    else: self.selecionadas_b.add(p)
            # Botões
            if self.btn_confirmar.collidepoint((mx,my)):
                self.ativo = False
            if self.btn_cancelar.collidepoint((mx,my)):
                self.selecionadas_a.clear(); self.selecionadas_b.clear()
                self.oferta_a.valor = "0"; self.oferta_b.valor = "0"
                self.ativo = False

    def obter_resultado(self):
        return {
            'props_a': list(self.selecionadas_a),
            'props_b': list(self.selecionadas_b),
            'dinheiro_a': self.oferta_a.get_valor(),
            'dinheiro_b': self.oferta_b.get_valor()
        }

    def _rect_item_a(self, idx):
        return pygame.Rect(self.x + 30, self.y + 100 + idx*36, 360, 30)

    def _rect_item_b(self, idx):
        return pygame.Rect(self.x + self.largura - 30 - 360, self.y + 100 + idx*36, 360, 30)

    def desenhar(self):
        if not self.ativo:
            return
        overlay = pygame.Surface((Config.LARGURA_TELA, Config.ALTURA_TELA))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        self.tela.blit(overlay, (0,0))

        rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(self.tela, (245,245,245), rect, border_radius=10)
        pygame.draw.rect(self.tela, Config.PRETO, rect, 3, border_radius=10)

        # Títulos
        ta = self.font_titulo.render(self.jog_a.getNome(), True, Config.PRETO)
        tb = self.font_titulo.render(self.jog_b.getNome(), True, Config.PRETO)
        self.tela.blit(ta, (self.x + 30, self.y + 40))
        self.tela.blit(tb, (self.x + self.largura - 30 - tb.get_width(), self.y + 40))

        # Listas de propriedades
        for idx, p in enumerate(self.jog_a.getPropriedades()):
            nome = p.getNome() if hasattr(p, 'getNome') else 'Prop'
            r = self._rect_item_a(idx)
            sel = p in self.selecionadas_a
            pygame.draw.rect(self.tela, (220,240,220) if sel else (230,230,230), r, border_radius=4)
            pygame.draw.rect(self.tela, (70,70,70), r, 1, border_radius=4)
            self.tela.blit(self.font_item.render(nome, True, (0,0,0)), (r.x+8, r.y+6))

        for idx, p in enumerate(self.jog_b.getPropriedades()):
            nome = p.getNome() if hasattr(p, 'getNome') else 'Prop'
            r = self._rect_item_b(idx)
            sel = p in self.selecionadas_b
            pygame.draw.rect(self.tela, (220,240,220) if sel else (230,230,230), r, border_radius=4)
            pygame.draw.rect(self.tela, (70,70,70), r, 1, border_radius=4)
            self.tela.blit(self.font_item.render(nome, True, (0,0,0)), (r.x+8, r.y+6))

        # Ofertas em dinheiro
        fa = self.font_item.render("Oferece: R$", True, (0,0,0))
        fb = self.font_item.render("Oferece: R$", True, (0,0,0))
        self.tela.blit(fa, (self.x + 30, self.y + self.altura - 84))
        self.tela.blit(fb, (self.x + self.largura - 30 - 360, self.y + self.altura - 84))
        self.oferta_a.desenhar(self.tela)
        self.oferta_b.desenhar(self.tela)

        # Botões
        mouse = pygame.mouse.get_pos()
        cor_ok = (0, 150, 0) if self.btn_confirmar.collidepoint(mouse) else (0,120,0)
        cor_ca = (150, 0, 0) if self.btn_cancelar.collidepoint(mouse) else (120,0,0)
        pygame.draw.rect(self.tela, cor_ok, self.btn_confirmar, border_radius=8)
        pygame.draw.rect(self.tela, Config.PRETO, self.btn_confirmar, 2, border_radius=8)
        pygame.draw.rect(self.tela, cor_ca, self.btn_cancelar, border_radius=8)
        pygame.draw.rect(self.tela, Config.PRETO, self.btn_cancelar, 2, border_radius=8)
        ok = self.font_item.render("CONFIRMAR", True, (255,255,255))
        ca = self.font_item.render("CANCELAR", True, (255,255,255))
        self.tela.blit(ok, ok.get_rect(center=self.btn_confirmar.center))
        self.tela.blit(ca, ca.get_rect(center=self.btn_cancelar.center))
