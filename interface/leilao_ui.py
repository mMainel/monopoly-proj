import pygame
from config import Config

class DialogoLeilaoUI:
    """Interface de leilão incremental entre jogadores."""
    def __init__(self, tela):
        self.tela = tela
        self.ativo = False
        self.leilao = None
        self.jogadores_ordenados = []
        self.indice_atual = 0
        self.mensagem = ""
        self.finalizado = False
        self.resultado = None

        self.largura = 760
        self.altura = 520
        self.x = (Config.LARGURA_TELA - self.largura)//2
        self.y = (Config.ALTURA_TELA - self.altura)//2

        self.font_titulo = pygame.font.Font(None, 40)
        self.font_sub = pygame.font.Font(None, 26)
        self.font_small = pygame.font.Font(None, 22)
        self.font_btn = pygame.font.Font(None, 28)

        # Botões dinâmicos
        self.btn_lance = pygame.Rect(0,0,0,0)
        self.btn_passar = pygame.Rect(0,0,0,0)
        self.btn_finalizar = pygame.Rect(0,0,0,0)
        self.input_valor = _InputValor()

    def iniciar(self, leilao, jogadores, indice_inicial):
        self.leilao = leilao
        self.jogadores_ordenados = jogadores[indice_inicial:] + jogadores[:indice_inicial]
        self.indice_atual = 0
        self.finalizado = False
        self.resultado = None
        self.ativo = True
        self._reposicionar_componentes()
        self.mensagem = f"Leilão iniciado para {leilao.getPropriedade().getNome()}"

    def _reposicionar_componentes(self):
        by = self.y + self.altura - 100
        w = 160; h = 50; gap = 30
        self.btn_lance = pygame.Rect(self.x + 50, by, w, h)
        self.btn_passar = pygame.Rect(self.x + 50 + w + gap, by, w, h)
        self.btn_finalizar = pygame.Rect(self.x + self.largura - 50 - w, by, w, h)
        self.input_valor.rect = pygame.Rect(self.x + self.largura//2 - 90, by, 180, h)

    def handle_event(self, e):
        if not self.ativo or self.finalizado:
            return
        self.input_valor.handle_event(e)
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx,my = e.pos
            jogador_atual = self.jogadores_ordenados[self.indice_atual]
            if self.btn_lance.collidepoint((mx,my)):
                valor = self.input_valor.get_valor()
                # Se valor 0, usar incremento automático
                if valor == 0:
                    valor = max(self.leilao.getLanceMaior(), 0) + 10
                if self.leilao.fazerLance(jogador_atual, valor):
                    self.mensagem = f"{jogador_atual.getNome()} fez lance: R$ {valor}"
                else:
                    self.mensagem = f"Lance inválido de {jogador_atual.getNome()}"
                self._proximo_jogador()
            elif self.btn_passar.collidepoint((mx,my)):
                self.mensagem = f"{jogador_atual.getNome()} passou"
                # Desistir remove jogador
                self.leilao.desistir(jogador_atual)
                self._proximo_jogador(remover=True)
            elif self.btn_finalizar.collidepoint((mx,my)):
                self._finalizar()

    def _proximo_jogador(self, remover=False):
        if self.finalizado:
            return
        if remover:
            self.jogadores_ordenados = [j for j in self.jogadores_ordenados if j in self.leilao.getParticipantes()]
        if len(self.leilao.getParticipantes()) <= 1:
            self._finalizar()
            return
        self.indice_atual = (self.indice_atual + 1) % len(self.jogadores_ordenados)

    def _finalizar(self):
        vencedor, valor = self.leilao.finalizarLeilao()
        if vencedor:
            self.mensagem = f"Vencedor: {vencedor.getNome()} por R$ {valor}"
        else:
            self.mensagem = "Leilão sem vencedor"
        self.finalizado = True
        self.resultado = (vencedor, valor)

    def obter_resultado(self):
        return self.resultado if self.finalizado else None

    def desenhar(self):
        if not self.ativo:
            return
        overlay = pygame.Surface((Config.LARGURA_TELA, Config.ALTURA_TELA))
        overlay.set_alpha(160)
        overlay.fill((0,0,0))
        self.tela.blit(overlay,(0,0))
        rect = pygame.Rect(self.x,self.y,self.largura,self.altura)
        pygame.draw.rect(self.tela,(245,245,245),rect,border_radius=12)
        pygame.draw.rect(self.tela,Config.PRETO,rect,3,border_radius=12)

        prop_nome = self.leilao.getPropriedade().getNome() if self.leilao and self.leilao.getPropriedade() else "Propriedade"
        titulo = self.font_titulo.render(f"Leilão: {prop_nome}", True, Config.PRETO)
        self.tela.blit(titulo,(self.x+30,self.y+30))

        # Informações
        maior = self.leilao.getLanceMaior() if self.leilao else 0
        lider = self.leilao.getLiderAtual()
        lider_nome = lider.getNome() if lider else "-"
        info1 = self.font_sub.render(f"Maior lance: R$ {maior}", True, Config.PRETO)
        info2 = self.font_sub.render(f"Líder: {lider_nome}", True, Config.PRETO)
        self.tela.blit(info1,(self.x+30,self.y+90))
        self.tela.blit(info2,(self.x+30,self.y+120))

        if not self.finalizado:
            atual = self.jogadores_ordenados[self.indice_atual]
            turno = self.font_sub.render(f"Vez: {atual.getNome()} (Saldo: R$ {atual.getSaldo()})", True, (0,0,0))
            self.tela.blit(turno,(self.x+30,self.y+160))

        msg = self.font_small.render(self.mensagem, True, (30,30,30))
        self.tela.blit(msg,(self.x+30,self.y+200))

        # Lista de participantes
        y_list = self.y + 240
        for j in self.leilao.getParticipantes():
            lance = self.leilao.getLancesRealizados().get(j,0)
            line = self.font_small.render(f"{j.getNome():15} Lance: R$ {lance}", True, (0,0,0))
            self.tela.blit(line,(self.x+30,y_list))
            y_list += 24

        # Controles
        mouse = pygame.mouse.get_pos()
        if not self.finalizado:
            self._draw_button(self.btn_lance, "LANCE", mouse, (0,140,0), (0,180,0))
            self._draw_button(self.btn_passar, "PASSAR", mouse, (140,0,0), (180,0,0))
            self._draw_button(self.btn_finalizar, "FINALIZAR", mouse, (0,0,140), (0,0,180))
            self.input_valor.desenhar(self.tela)
        else:
            self._draw_button(self.btn_finalizar, "FECHAR", mouse, (0,0,140), (0,0,180))

    def _draw_button(self, rect, texto, mouse, cor, cor_hover):
        c = cor_hover if rect.collidepoint(mouse) else cor
        pygame.draw.rect(self.tela,c,rect,border_radius=8)
        pygame.draw.rect(self.tela,Config.PRETO,rect,2,border_radius=8)
        t = self.font_btn.render(texto, True, (255,255,255))
        self.tela.blit(t, t.get_rect(center=rect.center))


class _InputValor:
    def __init__(self):
        self.rect = pygame.Rect(0,0,0,0)
        self.valor = ""
        self.ativo = False
        self.font = pygame.font.Font(None, 28)

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.ativo = self.rect.collidepoint(e.pos)
        if self.ativo and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                self.ativo = False
            elif e.key == pygame.K_BACKSPACE:
                self.valor = self.valor[:-1]
            elif e.unicode.isdigit() and len(self.valor) < 6:
                self.valor += e.unicode

    def get_valor(self):
        try:
            return int(self.valor) if self.valor else 0
        except:
            return 0

    def desenhar(self, tela):
        pygame.draw.rect(tela,(255,255,255),self.rect,border_radius=6)
        pygame.draw.rect(tela,(60,60,60),self.rect,2,border_radius=6)
        txt = self.font.render(self.valor or "", True, (0,0,0))
        tela.blit(txt, txt.get_rect(center=self.rect.center))
