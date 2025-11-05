class Config:
    # --- Configurações da Tela ---
    LARGURA_TELA = 1200
    ALTURA_TELA = 700

    # Cores (RGB)
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    CINZA_CLARO = (200, 200, 200)
    VERMELHO = (255, 0, 0)

    # --- Proporções ---
    PROPORCAO_TABULEIRO = 0.7  # 70% da largura para o tabuleiro
    PROPORCAO_PAINEL = 0.3     # 30% da largura para o painel

    # --- Cálculo de tamanhos base ---
    @classmethod
    def atualizar_dimensoes(cls):
        cls.LARGURA_TABULEIRO = int(cls.LARGURA_TELA * cls.PROPORCAO_TABULEIRO)
        cls.LARGURA_PAINEL = cls.LARGURA_TELA - cls.LARGURA_TABULEIRO - 20

        cls.TAMANHO_CASA_PEQUENA = cls.LARGURA_TABULEIRO // 13
        cls.TAMANHO_CASA_CANTO = int(cls.TAMANHO_CASA_PEQUENA * 1.5)
        cls.TAMANHO_TABULEIRO = (
            cls.TAMANHO_CASA_CANTO * 2 + 9 * cls.TAMANHO_CASA_PEQUENA
        )

        cls.POS_X_INICIO = 20  # sempre encostado à esquerda
        cls.POS_Y_INICIO = (cls.ALTURA_TELA - cls.TAMANHO_TABULEIRO) // 2


# Inicializa proporções ao carregar
Config.atualizar_dimensoes()
