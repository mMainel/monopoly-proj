# interface/tabuleiro_ui.py

import pygame

# --- Configurações de Tela e Cores ---

# Dimensões da tela - Ajuste conforme a necessidade
LARGURA_TELA = 800
ALTURA_TELA = 800

# Cores (RGB)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_CLARO = (200, 200, 200)
VERMELHO = (255, 0, 0)

# --- Configurações do Tabuleiro ---

# O tabuleiro será quadrado e ocupará a maior parte da tela.
# Lados externos (10 casas + 1 canto + 1 canto)
NUM_CASAS_LADO = 11  # Canto + 9 casas + Canto
TAMANHO_BORDA = 50   # Margem ao redor do tabuleiro
TAMANHO_TABULEIRO = LARGURA_TELA - (2 * TAMANHO_BORDA)
TAMANHO_CASA_PEQUENA = TAMANHO_TABULEIRO // NUM_CASAS_LADO
TAMANHO_CASA_CANTO = TAMANHO_CASA_PEQUENA * 2 # Casas de canto são o dobro

# Ajusta o tamanho da casa pequena para que o tabuleiro caiba perfeitamente
# (Ajuste para a proporção 4 cantos + 4 lados de 9 casas)
TAMANHO_CASA_PEQUENA = (TAMANHO_TABULEIRO - 4 * TAMANHO_CASA_CANTO) // 36 # Aproximação inicial
# Vamos simplificar: 4 cantos + 4x9 casas = 40 casas totais.
# Em cada lado há 1 canto + 9 casas, mas o canto é compartilhado.
# Para um lado: 1 canto + 9 casas. Os 4 cantos formam a 'esquina'.
# 4 cantos e 4 * 9 = 36 casas normais. Total de 40.
# O lado tem 10 divisões: 1 canto + 9 casas.
TAMANHO_CASA_PEQUENA = int((TAMANHO_TABULEIRO - 2 * TAMANHO_CASA_CANTO) / 9) # 9 casas pequenas no lado

# Ajuste fino:
# 1 lado = 1 canto + 9 casas pequenas.
# Se TAMANHO_CASA_CANTO = 100, e TAMANHO_CASA_PEQUENA = 50.
# Lado = 100 + 9*50 = 550.
TAMANHO_CASA_PEQUENA = 60
TAMANHO_CASA_CANTO = 120 # O canto será o dobro da casa pequena (2x2)
TAMANHO_TABULEIRO = TAMANHO_CASA_CANTO * 2 + 9 * TAMANHO_CASA_PEQUENA # Tamanho total (120 + 540 + 120 = 780)

# Ponto de início do desenho do tabuleiro (canto superior esquerdo)
POS_X_INICIO = (LARGURA_TELA - TAMANHO_TABULEIRO) // 2
POS_Y_INICIO = (ALTURA_TELA - TAMANHO_TABULEIRO) // 2


class Tabuleiro:
    """
    Classe responsável por desenhar a interface do tabuleiro no Pygame.
    """
    def __init__(self, jogo):
        """
        Inicializa o Pygame e a janela.
        :param jogo: A instância da sua classe Jogo (lógica).
        """
        pygame.init()
        self.jogo = jogo
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Monopoly Uffiano - Pygame")
        self.relogio = pygame.time.Clock()
        self.rodando = True
        
        # O self.jogo precisa ser um Observador do jogo para receber atualizações,
        # mas para a UI inicial, basta ter a referência.

    def desenhar_tabuleiro_estrutura(self):
        """Desenha a estrutura do tabuleiro (quadrado externo e divisões)."""
        
        # 1. Desenhar fundo
        self.tela.fill(BRANCO)
        
        # 2. Quadrado principal do tabuleiro
        tab_rect = pygame.Rect(POS_X_INICIO, POS_Y_INICIO, TAMANHO_TABULEIRO, TAMANHO_TABULEIRO)
        pygame.draw.rect(self.tela, CINZA_CLARO, tab_rect) # Fundo do tabuleiro
        pygame.draw.rect(self.tela, PRETO, tab_rect, 3)    # Borda externa
        
        # 3. Desenhar o "miolo" (o centro)
        miolo_tam = TAMANHO_TABULEIRO - 2 * TAMANHO_CASA_CANTO
        miolo_x = POS_X_INICIO + TAMANHO_CASA_CANTO
        miolo_y = POS_Y_INICIO + TAMANHO_CASA_CANTO
        miolo_rect = pygame.Rect(miolo_x, miolo_y, miolo_tam, miolo_tam)
        pygame.draw.rect(self.tela, BRANCO, miolo_rect) # Centro branco
        pygame.draw.rect(self.tela, PRETO, miolo_rect, 1) # Borda do centro
        
        # 4. Desenhar as 40 casas
        # A lógica para desenhar e posicionar as 40 casas é complexa.
        # Para este código inicial, vamos focar nos cantos e nas linhas básicas.
        
        # Coordenadas das casas de canto (Top-Left corner)
        cantos = [
            (POS_X_INICIO, POS_Y_INICIO), # Canto Superior Esquerdo (CSE)
            (POS_X_INICIO + TAMANHO_TABULEIRO - TAMANHO_CASA_CANTO, POS_Y_INICIO), # Canto Superior Direito (CSD)
            (POS_X_INICIO + TAMANHO_TABULEIRO - TAMANHO_CASA_CANTO, POS_Y_INICIO + TAMANHO_TABULEIRO - TAMANHO_CASA_CANTO), # Canto Inferior Direito (CID)
            (POS_X_INICIO, POS_Y_INICIO + TAMANHO_TABULEIRO - TAMANHO_CASA_CANTO) # Canto Inferior Esquerdo (CIE)
        ]
        
        # Desenhar Casas de Canto
        for x, y in cantos:
            rect = pygame.Rect(x, y, TAMANHO_CASA_CANTO, TAMANHO_CASA_CANTO)
            pygame.draw.rect(self.tela, VERMELHO, rect) # Canto (apenas para destaque inicial)
            pygame.draw.rect(self.tela, PRETO, rect, 1) # Borda do canto
            
        # Desenhar Casas Pequenas (Lado Superior, 9 casas)
        for i in range(1, 10):
            x = POS_X_INICIO + TAMANHO_CASA_CANTO + (i - 1) * TAMANHO_CASA_PEQUENA
            y = POS_Y_INICIO
            rect = pygame.Rect(x, y, TAMANHO_CASA_PEQUENA, TAMANHO_CASA_CANTO) # Casas superiores são verticais
            pygame.draw.rect(self.tela, CINZA_CLARO, rect)
            pygame.draw.rect(self.tela, PRETO, rect, 1)

        # Desenhar Casas Pequenas (Lado Esquerdo, 9 casas)
        for i in range(1, 10):
            x = POS_X_INICIO
            y = POS_Y_INICIO + TAMANHO_CASA_CANTO + (i - 1) * TAMANHO_CASA_PEQUENA
            rect = pygame.Rect(x, y, TAMANHO_CASA_CANTO, TAMANHO_CASA_PEQUENA) # Casas esquerdas são horizontais
            pygame.draw.rect(self.tela, CINZA_CLARO, rect)
            pygame.draw.rect(self.tela, PRETO, rect, 1)

        # ... (Outros lados - para um esboço inicial, os dois lados já dão a ideia)
        # O desenho completo exige um loop mais inteligente ou mapeamento.
        
        # 5. Exemplo de texto no centro
        fonte = pygame.font.Font(None, 40)
        texto = fonte.render("MONOPOLY UFFIANO", True, PRETO)
        texto_rect = texto.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
        self.tela.blit(texto, texto_rect)

    def loop_principal(self):
        """Loop principal do Pygame."""
        while self.rodando:
            # 1. Processamento de Eventos (Inputs)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                
                # Aqui iriam os eventos de clique/teclado para interagir com a Lógica do Jogo

            # 2. Lógica do Jogo (No futuro, chamaríamos métodos do self.jogo)
            # Ex: self.jogo.executar_turno() se o input for 'lançar dados'

            # 3. Desenho (Renderização)
            self.desenhar_tabuleiro_estrutura()

            # 4. Atualizar a tela
            pygame.display.flip()
            
            # Limitar o FPS
            self.relogio.tick(30)

        pygame.quit()


# --- Função para rodar a UI ---
# Se for executado diretamente, apenas exibe a UI
if __name__ == '__main__':
    # Cria um objeto 'mock' para simular a classe Jogo, já que ainda não podemos importar
    class MockJogo:
        def __init__(self):
            print("Mock Jogo criado.")

    ui = Tabuleiro(MockJogo())
    ui.loop_principal()