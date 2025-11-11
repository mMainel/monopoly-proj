from modules.peca import Peca

class Config:
    LARGURA_TELA = 1600
    ALTURA_TELA = 900

    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    CINZA_CLARO = (200, 200, 200)
    VERMELHO = (255, 0, 0)
    
    CORES_PECAS = {
        Peca.ARTES: (128, 0, 128),
        Peca.BIOLOGIA: (0, 128, 0),
        Peca.COMPUTACAO: (0, 0, 200),
        Peca.CINEMA: (50, 50, 50),
        Peca.DIREITO: (139, 0, 0),
        Peca.ENGENHARIA: (255, 140, 0),
        Peca.FISICA: (255, 215, 0),
        Peca.NUTRICAO: (154, 205, 50),
        Peca.MEDICINA: (0, 128, 128),
        Peca.ODONTOLOGIA: (173, 216, 230),
        Peca.PEDAGOGIA: (255, 105, 180),
        Peca.QUIMICA: (255, 0, 255),
    }
    AZUL = (0, 0, 255)
    VERDE = (0, 255, 0)
    AMARELO = (255, 255, 0)
    LARANJA = (255, 165, 0)
    ROXO = (128, 0, 128)
    ROSA = (255, 192, 203)
    CIANO = (0, 255, 255)
    MARROM = (165, 42, 42)

    CORES_JOGADORES = [
        VERMELHO, AZUL, VERDE, AMARELO,
        LARANJA, ROXO, ROSA, CIANO
    ]

    RAIO_JOGADOR = 15 

    PROPORCAO_TABULEIRO = 0.7
    PROPORCAO_PAINEL = 0.3

    @classmethod
    def atualizar_dimensoes(cls):
        cls.LARGURA_TABULEIRO = int(cls.LARGURA_TELA * cls.PROPORCAO_TABULEIRO)
        cls.LARGURA_PAINEL = cls.LARGURA_TELA - cls.LARGURA_TABULEIRO - 20
        largura_max = cls.LARGURA_TABULEIRO
        altura_max = cls.ALTURA_TELA - 40
        casa_largura = largura_max // 13
        casa_altura = altura_max // 13
        cls.TAMANHO_CASA_PEQUENA = min(casa_largura, casa_altura)
        cls.TAMANHO_CASA_CANTO = int(cls.TAMANHO_CASA_PEQUENA * 1.5)
        cls.TAMANHO_TABULEIRO = (cls.TAMANHO_CASA_CANTO * 2 + 9 * cls.TAMANHO_CASA_PEQUENA)
        cls.POS_X_INICIO = 20  
        cls.POS_Y_INICIO = (cls.ALTURA_TELA - cls.TAMANHO_TABULEIRO) // 2
        cls.RAIO_JOGADOR = cls.TAMANHO_CASA_PEQUENA // 3
        cls.POS_CASA_PARTIDA_X = cls.POS_X_INICIO + cls.TAMANHO_CASA_CANTO
        cls.POS_CASA_PARTIDA_Y = cls.POS_Y_INICIO + cls.TAMANHO_TABULEIRO - cls.TAMANHO_CASA_CANTO - cls.TAMANHO_CASA_PEQUENA
        cls.POSICAO_INICIAL_JOGADORES = cls.calcular_posicoes_partida()
    
    @classmethod
    def calcular_posicoes_partida(cls):
        posicoes = {}
        casa_x = cls.POS_X_INICIO
        casa_y = cls.POS_Y_INICIO + cls.TAMANHO_TABULEIRO - cls.TAMANHO_CASA_CANTO
        casa_largura = cls.TAMANHO_CASA_CANTO
        casa_altura = cls.TAMANHO_CASA_CANTO
        margem = cls.TAMANHO_CASA_CANTO * 0.15
        area_util_x = casa_largura - 2 * margem
        area_util_y = casa_altura - 2 * margem
        cols, rows = 4, 2
        espacamento_x = area_util_x / (cols - 1)
        espacamento_y = area_util_y / (rows - 1) * 0.5
        i = 0
        for linha in range(rows):
            for coluna in range(cols):
                if i >= 8:
                    break
                pos_x = casa_x + margem + coluna * espacamento_x
                pos_y = casa_y + margem + linha * espacamento_y
                posicoes[i] = (pos_x, pos_y)
                i += 1
        return posicoes

    @classmethod
    def calcular_posicoes_na_casa(cls, numero_casa):
        return cls.POSICAO_INICIAL_JOGADORES

    @classmethod
    def get_coordenadas_casa(cls, numero_casa):
        centro_x = cls.POS_CASA_PARTIDA_X + cls.TAMANHO_CASA_PEQUENA // 2
        centro_y = cls.POS_CASA_PARTIDA_Y + cls.TAMANHO_CASA_PEQUENA // 2
        return (centro_x, centro_y)

Config.atualizar_dimensoes()