from modules.peca import Peca

class Config:
    # --- Configurações da Tela ---
    LARGURA_TELA = 1200
    ALTURA_TELA = 700

    # Cores (RGB)
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    CINZA_CLARO = (200, 200, 200)
    VERMELHO = (255, 0, 0)
    
    CORES_PECAS = {
        Peca.ARTES: (128, 0, 128),         # Roxo
        Peca.BIOLOGIA: (0, 128, 0),        # Verde Escuro
        Peca.COMPUTACAO: (0, 0, 200),      # Azul Escuro
        Peca.CINEMA: (50, 50, 50),         # Cinza Chumbo
        Peca.DIREITO: (139, 0, 0),         # Vermelho Escuro
        Peca.ENGENHARIA: (255, 140, 0),    # Laranja
        Peca.FISICA: (255, 215, 0),        # Amarelo Ouro
        Peca.NUTRICAO: (154, 205, 50),     # Verde Limão
        Peca.MEDICINA: (0, 128, 128),      # Verde Água
        Peca.ODONTOLOGIA: (173, 216, 230), # Azul Claro
        Peca.PEDAGOGIA: (255, 105, 180),   # Rosa
        Peca.QUIMICA: (255, 0, 255),       # Magenta
    }

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
