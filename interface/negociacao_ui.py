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
        self.font_item = pygame.font.Font(None, 22)

        self.largura = 950
        self.altura = 600
        self.x = (Config.LARGURA_TELA - self.largura)//2
        self.y = (Config.ALTURA_TELA - self.altura)//2

    def mostrar(self, jog_a, jog_b):
        self.jog_a = jog_a
        self.jog_b = jog_b
        self.selecionadas_a = set()
        self.selecionadas_b = set()
        self.ativo = True

        w = 140; h = 40
        self.oferta_a = _InputNumero(self.x + 180, self.y + self.altura - 100, w, h, 0)
        self.oferta_b = _InputNumero(self.x + self.largura - 180 - w, self.y + self.altura - 100, w, h, 0)
        self.btn_confirmar = pygame.Rect(self.x + self.largura//2 - 160, self.y + self.altura - 55, 140, 40)
        self.btn_cancelar = pygame.Rect(self.x + self.largura//2 + 20, self.y + self.altura - 55, 140, 40)

    def handle_event(self, e):
        if not self.ativo:
            return
        self.oferta_a.handle_event(e)
        self.oferta_b.handle_event(e)
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx, my = e.pos
            for idx, p in enumerate(self.jog_a.getPropriedades()):
                rect = self._rect_item_a(idx)
                if rect.collidepoint((mx, my)):
                    if self._pode_trocar(p):
                        if p in self.selecionadas_a: self.selecionadas_a.remove(p)
                        else: self.selecionadas_a.add(p)
            for idx, p in enumerate(self.jog_b.getPropriedades()):
                rect = self._rect_item_b(idx)
                if rect.collidepoint((mx, my)):
                    if self._pode_trocar(p):
                        if p in self.selecionadas_b: self.selecionadas_b.remove(p)
                        else: self.selecionadas_b.add(p)
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
        return pygame.Rect(self.x + 30, self.y + 100 + idx*40, 400, 35)

    def _rect_item_b(self, idx):
        return pygame.Rect(self.x + self.largura - 30 - 400, self.y + 100 + idx*40, 400, 35)

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

        ta = self.font_titulo.render(self.jog_a.getNome(), True, Config.PRETO)
        tb = self.font_titulo.render(self.jog_b.getNome(), True, Config.PRETO)
        self.tela.blit(ta, (self.x + 30, self.y + 40))
        self.tela.blit(tb, (self.x + self.largura - 30 - tb.get_width(), self.y + 40))
        
        saldo_a = self.font_item.render(f"Saldo: R${self.jog_a.getSaldo()}", True, (0, 100, 0))
        saldo_b = self.font_item.render(f"Saldo: R${self.jog_b.getSaldo()}", True, (0, 100, 0))
        self.tela.blit(saldo_a, (self.x + 30, self.y + 70))
        self.tela.blit(saldo_b, (self.x + self.largura - 30 - saldo_b.get_width(), self.y + 70))

        for idx, p in enumerate(self.jog_a.getPropriedades()):
            nome = p.getNome() if hasattr(p, 'getNome') else 'Prop'
            r = self._rect_item_a(idx)
            sel = p in self.selecionadas_a
            pygame.draw.rect(self.tela, (220,240,220) if sel else (230,230,230), r, border_radius=4)
            pygame.draw.rect(self.tela, (70,70,70), r, 1, border_radius=4)
            cor_rgb = self._cor_propriedade(p)
            pygame.draw.rect(self.tela, cor_rgb, pygame.Rect(r.x+6, r.y+5, 20, 20), border_radius=4)
            texto_prop = self._formatar_texto_prop(p, nome)
            cor_txt = (0,0,0)
            if not self._pode_trocar(p):
                cor_txt = (110,0,0)
            self.tela.blit(self.font_item.render(texto_prop, True, cor_txt), (r.x+32, r.y+6))

        for idx, p in enumerate(self.jog_b.getPropriedades()):
            nome = p.getNome() if hasattr(p, 'getNome') else 'Prop'
            r = self._rect_item_b(idx)
            sel = p in self.selecionadas_b
            pygame.draw.rect(self.tela, (220,240,220) if sel else (230,230,230), r, border_radius=4)
            pygame.draw.rect(self.tela, (70,70,70), r, 1, border_radius=4)
            cor_rgb = self._cor_propriedade(p)
            pygame.draw.rect(self.tela, cor_rgb, pygame.Rect(r.x+6, r.y+5, 20, 20), border_radius=4)
            texto_prop = self._formatar_texto_prop(p, nome)
            cor_txt = (0,0,0)
            if not self._pode_trocar(p):
                cor_txt = (110,0,0)
            self.tela.blit(self.font_item.render(texto_prop, True, cor_txt), (r.x+32, r.y+6))

        fa = self.font_item.render("Oferece: R$", True, (0,0,0))
        fb = self.font_item.render("Oferece: R$", True, (0,0,0))
        self.tela.blit(fa, (self.x + 30, self.y + self.altura - 94))
        self.tela.blit(fb, (self.x + self.largura - 30 - 400, self.y + self.altura - 94))
        self.oferta_a.desenhar(self.tela)
        self.oferta_b.desenhar(self.tela)

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

    def _cor_propriedade(self, prop):
        """Mapeia cor da propriedade para RGB igual ao menu de gerenciamento."""
        try:
            if not hasattr(prop, 'getCor'):
                return (180,180,180)
            cor_val = prop.getCor()
            if hasattr(cor_val, 'value'):
                key = str(cor_val.value).strip().lower()
            else:
                key = str(cor_val).strip().lower()
            mapa = {
                'marrom': (128, 64, 0),
                'azul claro': (135, 206, 250),
                'rosa': (255, 192, 203),
                'laranja': (255, 165, 0),
                'vermelho': (255, 0, 0),
                'amarelo': (255, 255, 0),
                'verde': (0, 200, 0),
                'azul escuro': (0, 0, 160),
            }
            return mapa.get(key, (180,180,180))
        except Exception:
            return (180,180,180)

    def _pode_trocar(self, prop):
        """Retorna True se a propriedade pode ser incluída na troca (sem casas/hotel)."""
        try:
            from modules.tituloPropriedade import TituloPropriedade
            if not isinstance(prop, TituloPropriedade):
                # Estações / companhias sem casas podem trocar
                return True
            if getattr(prop, 'tem_hotel', False):
                return False
            if hasattr(prop, 'getNumCasas') and prop.getNumCasas() > 0:
                return False
            return True
        except Exception:
            return True

    def _formatar_texto_prop(self, prop, nome):
        """Formata nome + preço e info de casas/hotel."""
        preco = 0
        try:
            if hasattr(prop, 'getPreco'):
                preco = prop.getPreco()
        except Exception:
            preco = 0
        info_extra = ""
        try:
            from modules.tituloPropriedade import TituloPropriedade
            if isinstance(prop, TituloPropriedade):
                if getattr(prop, 'tem_hotel', False):
                    info_extra = " (hotel)"
                elif hasattr(prop, 'getNumCasas'):
                    nc = prop.getNumCasas()
                    if nc > 0:
                        info_extra = f" ({nc}c)"
        except Exception:
            pass
        
        nome_curto = nome if len(nome) <= 18 else nome[:15] + "..."
        texto = f"{nome_curto} - R${preco}"
        if info_extra:
            texto += info_extra
        if not self._pode_trocar(prop) and info_extra:
            texto += " [X]"
        return texto


class DialogoMenuFimTurnoUI:
    def __init__(self, tela):
        self.tela = tela
        self.ativo = False
        self.opcao = None
        self.font_titulo = pygame.font.Font(None, 36)
        self.font_btn = pygame.font.Font(None, 30)
        self.largura = 520
        self.altura = 320  # Aumentado de 280 para 320
        self.x = (Config.LARGURA_TELA - self.largura)//2
        self.y = (Config.ALTURA_TELA - self.altura)//2
        self.btn_negociar = pygame.Rect(0,0,0,0)
        self.btn_gerenciar = pygame.Rect(0,0,0,0)
        self.btn_passar = pygame.Rect(0,0,0,0)

    def mostrar(self):
        self.ativo = True
        self.opcao = None
        by = self.y + 80
        w = self.largura - 80
        h = 56
        gap = 16
        cx = self.x + self.largura//2
        self.btn_negociar = pygame.Rect(cx - w//2, by, w, h)
        self.btn_gerenciar = pygame.Rect(cx - w//2, by + h + gap, w, h)
        self.btn_passar = pygame.Rect(cx - w//2, by + 2*(h + gap), w, h)

    def handle_event(self, e):
        if not self.ativo:
            return
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.btn_negociar.collidepoint(e.pos):
                self.opcao = 'negociar'
                self.ativo = False
            elif self.btn_gerenciar.collidepoint(e.pos):
                self.opcao = 'gerenciar'
                self.ativo = False
            elif self.btn_passar.collidepoint(e.pos):
                self.opcao = 'passar'
                self.ativo = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.opcao = 'passar'
            self.ativo = False

    def obter_opcao(self):
        return self.opcao

    def desenhar(self):
        if not self.ativo:
            return
        overlay = pygame.Surface((Config.LARGURA_TELA, Config.ALTURA_TELA))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        self.tela.blit(overlay,(0,0))
        rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(self.tela, (245,245,245), rect, border_radius=10)
        pygame.draw.rect(self.tela, Config.PRETO, rect, 3, border_radius=10)
        t = self.font_titulo.render("O que deseja fazer?", True, Config.PRETO)
        self.tela.blit(t, t.get_rect(center=(self.x + self.largura//2, self.y + 36)))
        mouse = pygame.mouse.get_pos()
        self._btn(self.btn_negociar, "Negociar", mouse)
        self._btn(self.btn_gerenciar, "Gerenciar propriedades", mouse)
        self._btn(self.btn_passar, "Passar turno", mouse)

    def _btn(self, rect, texto, mouse):
        cor = (60,140,220) if rect.collidepoint(mouse) else (40,120,200)
        pygame.draw.rect(self.tela, cor, rect, border_radius=8)
        pygame.draw.rect(self.tela, Config.PRETO, rect, 2, border_radius=8)
        tx = self.font_btn.render(texto, True, (255,255,255))
        self.tela.blit(tx, tx.get_rect(center=rect.center))


class DialogoGerenciarPropriedadesUI:
    def __init__(self, tela):
        self.tela = tela
        self.ativo = False
        self.jogo = None
        self.jogador = None
        self.font_titulo = pygame.font.Font(None, 36)
        self.font_item = pygame.font.Font(None, 24)
        self.largura = 720
        self.altura = 520
        self.x = (Config.LARGURA_TELA - self.largura)//2
        self.y = (Config.ALTURA_TELA - self.altura)//2
        self.btn_fechar = pygame.Rect(0,0,0,0)
        self._botoes = []
        self._scroll = 0
        self._scroll_max = 0

    def mostrar(self, jogo, jogador):
        self.jogo = jogo
        self.jogador = jogador
        self.ativo = True
        self.btn_fechar = pygame.Rect(self.x + self.largura - 140, self.y + 20, 120, 40)
        self._botoes = []
        self._scroll = 0
        self._scroll_max = 0

    def handle_event(self, e):
        if not self.ativo:
            return
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.btn_fechar.collidepoint(e.pos):
                self.ativo = False
            else:
                mx, my = e.pos
                for rect, acao, prop in self._botoes:
                    if rect.collidepoint((mx, my)):
                        self._executar_acao(acao, prop)
                        break
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.ativo = False
        # Scroll com roda do mouse
        if e.type == pygame.MOUSEWHEEL:
            if self._scroll_max > 0:
                self._scroll -= e.y * 40  # e.y é +1 para rodar para cima
                if self._scroll < 0:
                    self._scroll = 0
                if self._scroll > self._scroll_max:
                    self._scroll = self._scroll_max
        if e.type == pygame.MOUSEBUTTONDOWN and e.button in (4,5):
            delta = 40 if e.button == 5 else -40
            if self._scroll_max > 0:
                self._scroll += delta
                if self._scroll < 0:
                    self._scroll = 0
                if self._scroll > self._scroll_max:
                    self._scroll = self._scroll_max

    def desenhar(self):
        if not self.ativo:
            return
        overlay = pygame.Surface((Config.LARGURA_TELA, Config.ALTURA_TELA))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        self.tela.blit(overlay,(0,0))
        rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(self.tela, (245,245,245), rect, border_radius=10)
        pygame.draw.rect(self.tela, Config.PRETO, rect, 3, border_radius=10)
        t = self.font_titulo.render("Suas propriedades", True, Config.PRETO)
        self.tela.blit(t, (self.x + 30, self.y + 26))
        # Preparar grupos por cor
        grupos = {}
        for p in self.jogador.getPropriedades():
            cor_key = self._normalizar_cor(p)
            grupos.setdefault(cor_key, []).append(p)
        ordem_cores = [
            'marrom','azul claro','rosa','laranja','vermelho','amarelo','verde','azul escuro'
        ]
        # Ordenar grupos conforme ordem_cores
        itens_ordenados = []
        for cor in ordem_cores:
            if cor in grupos:
                itens_ordenados.append((cor, grupos[cor]))
        # Adicionar quaisquer cores inesperadas
        for cor, props in grupos.items():
            if cor not in ordem_cores:
                itens_ordenados.append((cor, props))

        area_list = pygame.Rect(self.x + 20, self.y + 70, self.largura - 40, self.altura - 140)
        clip_surface = pygame.Surface(area_list.size)
        clip_surface.fill((230,230,230))
        self.tela.blit(clip_surface, area_list.topleft)
        pygame.draw.rect(self.tela, Config.PRETO, area_list, 1, border_radius=6)
        # Desenhar conteúdos com scroll
        y_cursor = area_list.y + 10 - self._scroll
        self._botoes = []
        for cor, props in itens_ordenados:
            # Espaço entre grupos (removendo cabeçalho textual da cor)
            y_cursor += 12
            for p in props:
                nome = p.getNome() if hasattr(p, 'getNome') else 'Propriedade'
                cor_rgb = self._cor_propriedade(p)
                linha_rect = pygame.Rect(area_list.x + 10, y_cursor, area_list.width - 20, 34)
                if linha_rect.bottom >= area_list.y and linha_rect.top <= area_list.bottom:
                    pygame.draw.rect(self.tela, (245,245,245), linha_rect, border_radius=6)
                    pygame.draw.rect(self.tela, Config.PRETO, linha_rect, 1, border_radius=6)
                    pygame.draw.rect(self.tela, cor_rgb, pygame.Rect(linha_rect.x + 6, linha_rect.y + 6, 22, 22), border_radius=4)
                    tx = self.font_item.render(nome, True, (0,0,0))
                    self.tela.blit(tx, (linha_rect.x + 36, linha_rect.y + 6))
                    # Botões
                    btn_w, btn_h, gap = 110, 24, 6
                    bx = linha_rect.right - (btn_w * 4 + gap * 3) - 10
                    by = linha_rect.y + (linha_rect.height - btn_h)//2
                    rect_comp = pygame.Rect(bx, by, btn_w, btn_h)
                    rect_vend = pygame.Rect(bx + (btn_w + gap), by, btn_w, btn_h)
                    rect_hipo = pygame.Rect(bx + 2*(btn_w + gap), by, btn_w, btn_h)
                    rect_deshipo = pygame.Rect(bx + 3*(btn_w + gap), by, btn_w, btn_h)
                    habil_compra = self._pode_comprar_casa(p)
                    habil_vender = self._pode_vender_casa(p)
                    habil_hipo = self._pode_hipotecar(p)
                    habil_deshipo = self._pode_deshipotecar(p)
                    texto_comprar = "Comprar Hotel" if (hasattr(p, 'getNumCasas') and p.getNumCasas() >= 4) else "Comprar"
                    self._desenhar_botao(rect_comp, texto_comprar, habil_compra)
                    self._desenhar_botao(rect_vend, "Vender", habil_vender)
                    self._desenhar_botao(rect_hipo, "Hipotecar", habil_hipo)
                    self._desenhar_botao(rect_deshipo, "Deshipotecar", habil_deshipo)
                    if habil_compra:
                        self._botoes.append((rect_comp, 'comprar', p))
                    if habil_vender:
                        self._botoes.append((rect_vend, 'vender', p))
                    if habil_hipo:
                        self._botoes.append((rect_hipo, 'hipotecar', p))
                    if habil_deshipo:
                        self._botoes.append((rect_deshipo, 'deshipotecar', p))
                y_cursor += 40
        # Calcular scroll_max
        conteudo_altura = y_cursor - (area_list.y + 10)
        visivel = area_list.height - 20
        if conteudo_altura > visivel:
            self._scroll_max = conteudo_altura - visivel
        else:
            self._scroll_max = 0

        # botão fechar
        mouse = pygame.mouse.get_pos()
        cor_b = (140,0,0) if self.btn_fechar.collidepoint(mouse) else (120,0,0)
        pygame.draw.rect(self.tela, cor_b, self.btn_fechar, border_radius=8)
        pygame.draw.rect(self.tela, Config.PRETO, self.btn_fechar, 2, border_radius=8)
        txb = self.font_item.render("Fechar", True, (255,255,255))
        self.tela.blit(txb, txb.get_rect(center=self.btn_fechar.center))

    def _cor_propriedade(self, prop):
        """Resolve a cor da propriedade a partir do grupo. Aceita string ou enum."""
        try:
            if not hasattr(prop, 'getCor'):
                return (180,180,180)
            cor_val = prop.getCor()

            # Normaliza para string comparável
            if hasattr(cor_val, 'value'):
                key = str(cor_val.value).strip().lower()
            else:
                key = str(cor_val).strip().lower()

            mapa = {
                'marrom': (128, 64, 0),
                'azul claro': (135, 206, 250),
                'rosa': (255, 192, 203),
                'laranja': (255, 165, 0),
                'vermelho': (255, 0, 0),
                'amarelo': (255, 255, 0),
                'verde': (0, 200, 0),
                'azul escuro': (0, 0, 160),
            }
            return mapa.get(key, (180,180,180))
        except Exception:
            return (180,180,180)

    def _normalizar_cor(self, prop):
        try:
            if not hasattr(prop, 'getCor'):
                return 'outros'
            cor_val = prop.getCor()
            if hasattr(cor_val, 'value'):
                key = str(cor_val.value).strip().lower()
            else:
                key = str(cor_val).strip().lower()
            return key
        except:
            return 'outros'

    def _desenhar_botao(self, rect, texto, habilitado):
        cor = (40,120,200) if habilitado else (160,160,160)
        pygame.draw.rect(self.tela, cor, rect, border_radius=6)
        pygame.draw.rect(self.tela, Config.PRETO, rect, 1, border_radius=6)
        tx = self.font_item.render(texto, True, (255,255,255) if habilitado else (230,230,230))
        self.tela.blit(tx, tx.get_rect(center=rect.center))

    def _pode_comprar_casa(self, prop):
        try:
            from modules.tituloPropriedade import TituloPropriedade
            if not isinstance(prop, TituloPropriedade):
                return False
            if not self.jogador.possuiMonopolio(prop.getCor()):
                return False
            if hasattr(prop, 'tem_hotel') and prop.tem_hotel:
                return False
            if hasattr(prop, 'estaHipotecada') and prop.estaHipotecada():
                return False
            return True
        except Exception:
            return False

    def _pode_vender_casa(self, prop):
        try:
            if hasattr(prop, 'temHotel') and prop.temHotel():
                return True
            if hasattr(prop, 'getNumCasas') and prop.getNumCasas() > 0:
                return True
            return False
        except Exception:
            return False

    def _pode_hipotecar(self, prop):
        try:
            if hasattr(prop, 'estaHipotecada') and prop.estaHipotecada():
                return False
            # Permite hipotecar para títulos não-construtíveis (estações/companhias)
            from modules.tituloPropriedade import TituloPropriedade
            if not isinstance(prop, TituloPropriedade):
                return True
            # Para propriedades coloridas, respeitar restrições
            if hasattr(prop, 'podeHipotecar'):
                return prop.podeHipotecar()
            sem_casas = hasattr(prop, 'getNumCasas') and prop.getNumCasas() == 0
            sem_hotel = not getattr(prop, 'tem_hotel', False)
            return sem_casas and sem_hotel
        except Exception:
            return False

    def _executar_acao(self, acao, prop):
        try:
            if acao == 'comprar':
                if hasattr(prop, 'getNumCasas') and prop.getNumCasas() >= 4:
                    if hasattr(self.jogo, 'construirHotel'):
                        self.jogo.construirHotel(prop, self.jogador)
                else:
                    if hasattr(self.jogo, 'construirCasa'):
                        self.jogo.construirCasa(prop, self.jogador)
            elif acao == 'vender':
                if hasattr(prop, 'temHotel') and prop.temHotel():
                    if hasattr(self.jogo, 'venderHotel'):
                        self.jogo.venderHotel(prop, self.jogador)
                else:
                    if hasattr(self.jogo, 'venderCasa'):
                        self.jogo.venderCasa(prop, self.jogador)
            elif acao == 'hipotecar':
                if hasattr(self.jogo, 'hipotecarPropriedade'):
                    self.jogo.hipotecarPropriedade(prop, self.jogador)
            elif acao == 'deshipotecar':
                if hasattr(self.jogo, 'deshipotecarPropriedade'):
                    self.jogo.deshipotecarPropriedade(prop, self.jogador)
        except Exception:
            pass

    def _pode_deshipotecar(self, prop):
        try:
            if hasattr(prop, 'estaHipotecada') and prop.estaHipotecada():
                # custo 55% do preço
                custo = int(getattr(prop, 'getPreco', lambda:0)() * 0.55)
                return self.jogador.getSaldo() >= custo
            return False
        except:
            return False
