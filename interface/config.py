class Config:
    # --- Configurações da Tela ---
    # Dimensões da tela 
    LARGURA_TELA = 1200
    ALTURA_TELA = 700

    # Cores (RGB)
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    CINZA_CLARO = (200, 200, 200)
    VERMELHO = (255, 0, 0)

    # --- Configurações do Tabuleiro ---
    TAMANHO_CASA_PEQUENA = 50 
    TAMANHO_CASA_CANTO = TAMANHO_CASA_PEQUENA * 1.5 

    TAMANHO_TABULEIRO = TAMANHO_CASA_CANTO * 2 + 9 * TAMANHO_CASA_PEQUENA

    POS_X_INICIO = (LARGURA_TELA - TAMANHO_TABULEIRO) // 2 
    POS_Y_INICIO = (ALTURA_TELA - TAMANHO_TABULEIRO) // 2 