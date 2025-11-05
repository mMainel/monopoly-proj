import pygame
from config import Config

class PainelJogadoresUI:
    """
    Classe responsável por desenhar o painel lateral com informações dos jogadores.
    Fica fixo à direita do tabuleiro.
    """

    def __init__(self, tela, jogadores):
        self.tela = tela
        self.jogadores = jogadores
        self.fonte_titulo = pygame.font.Font(None, 36)
        self.fonte_info = pygame.font.Font(None, 28)

        # Define posição e tamanho do painel lateral
        self.largura = 350
        self.margem = 20
        self.x = Config.LARGURA_TELA - self.largura - self.margem
        self.y = Config.POS_Y_INICIO
        self.altura = Config.TAMANHO_TABULEIRO

    def desenhar(self):
        """Desenha o painel de informações dos jogadores."""
        # Fundo do painel
        painel_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(self.tela, Config.CINZA_CLARO, painel_rect)
        pygame.draw.rect(self.tela, Config.PRETO, painel_rect, 3)

        # Título do painel
        titulo = self.fonte_titulo.render("JOGADORES", True, Config.PRETO)
        self.tela.blit(titulo, (self.x + 15, self.y + 15))

        # Espaçamento inicial
        y_atual = self.y + 60

        for jogador in self.jogadores:
            # Nome
            nome_texto = f"{jogador.getNome()}"
            cor_nome = (0, 100, 255) if not jogador.estaFalido else (180, 0, 0)
            nome_render = self.fonte_titulo.render(nome_texto, True, cor_nome)
            self.tela.blit(nome_render, (self.x + 15, y_atual))

            y_atual += 30

            # Saldo
            saldo_texto = f"💰 Saldo: R$ {jogador.getSaldo()}"
            saldo_render = self.fonte_info.render(saldo_texto, True, Config.PRETO)
            self.tela.blit(saldo_render, (self.x + 25, y_atual))
            y_atual += 25

            # Posição no tabuleiro
            pos_texto = f"📍 Posição: {jogador.getPosicao()}"
            pos_render = self.fonte_info.render(pos_texto, True, Config.PRETO)
            self.tela.blit(pos_render, (self.x + 25, y_atual))
            y_atual += 25

            # Status de cadeia
            if jogador.estaEmCadeia():
                cadeia_texto = f"🚔 Preso ({jogador.getTurnosCadeia()} turnos)"
                cadeia_render = self.fonte_info.render(cadeia_texto, True, (200, 50, 50))
                self.tela.blit(cadeia_render, (self.x + 25, y_atual))
                y_atual += 25

            # Quantidade de propriedades
            props = jogador.getPropriedades()
            props_texto = f"🏠 Propriedades: {len(props)}"
            props_render = self.fonte_info.render(props_texto, True, Config.PRETO)
            self.tela.blit(props_render, (self.x + 25, y_atual))
            y_atual += 35

            # Linha divisória entre jogadores
            pygame.draw.line(
                self.tela,
                Config.PRETO,
                (self.x + 10, y_atual),
                (self.x + self.largura - 10, y_atual),
                1
            )

            y_atual += 20
