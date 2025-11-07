import pygame

class BotaoDadoUI:
    def __init__(self, tela, jogo):
        """
        Inicializa o botão "Rodar Dado".
        :param tela: Superfície do Pygame onde o botão será desenhado.
        :param jogo: Instância do jogo para acessar jogadores e lógica.
        """
        self.tela = tela
        self.jogo = jogo
        self.turno_atual = 0  # Índice do jogador atual

        # Configuração do botão
        self.largura = 200
        self.altura = 60
        self.rect = pygame.Rect(
            (self.tela.get_width() - self.largura) // 2,
            (self.tela.get_height() - self.altura) // 2,
            self.largura,
            self.altura
        )
        self.fonte = pygame.font.Font(None, 36)
        self.texto = self.fonte.render("Rodar Dado", True, pygame.Color("white"))
        self.texto_rect = self.texto.get_rect(center=self.rect.center)

    def desenhar(self):
        """Desenha o botão na tela."""
        pygame.draw.rect(self.tela, pygame.Color("blue"), self.rect)
        self.tela.blit(self.texto, self.texto_rect)

    def handle_event(self, evento):
        """
        Processa eventos relacionados ao botão.
        :param evento: Evento do Pygame.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.rodar_dado()

    def rodar_dado(self):
        """Lógica de rodar o dado e mover o jogador."""
        jogador_atual = self.jogo.jogadores[self.turno_atual]
        resultado_dados = self.jogo.dados.lancar()
        self.jogo._mover_jogador(jogador_atual, resultado_dados)

        # Processar eventos da casa onde o jogador parou
        self.jogo.tabuleiro.executarAcaoEspaco(jogador_atual.posicao, jogador_atual, self.jogo)

        # Passar o turno para o próximo jogador
        self.turno_atual = (self.turno_atual + 1) % len(self.jogo.jogadores)