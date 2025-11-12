from abc import ABC, abstractmethod
from typing import Optional

class Espaco(ABC):
    """
    Classe abstrata que representa um espaço no tabuleiro
    Cada casa do tabuleiro é um tipo específico de espaço
    """

    def __init__(self, nome: str, posicao: int):
        self.nome = nome
        self.posicao = posicao

    @abstractmethod
    def acao(self, jogador, jogo) -> None:
        """
        Executa a ação quando um jogador cai neste espaço

        espera:
            jogador: Jogador - jogador que caiu no espaço
            jogo: Jogo - instância do jogo para acessar regras e banco
        retorna:
            None
        """
        pass

    def getNome(self) -> str:
        """
        Retorna o nome do espaço

        espera:
            nenhum parâmetro
        retorna:
            str - nome do espaço
        """
        return self.nome

    def getPosicao(self) -> int:
        """
        Retorna a posição do espaço no tabuleiro

        espera:
            nenhum parâmetro
        retorna:
            int - posição (0-39)
        """
        return self.posicao

class EspacoPropriedade(Espaco):
    """
    Espaço que contém uma propriedade comprável
    """

    def __init__(self, nome: str, posicao: int, titulo):
        super().__init__(nome, posicao)
        self.titulo = titulo

    def acao(self, jogador, jogo) -> None:
        """
        Verifica se propriedade tem dono e cobra aluguel ou oferece compra

        espera:
            jogador: Jogador - jogador que caiu aqui
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        if self.titulo.getProprietario() is None:
            jogo.propriedade_disponivel_compra = self.titulo
        elif self.titulo.getProprietario() != jogador:
            jogo.tratarPagamentoAluguel(jogador, self.titulo)

    def getTitulo(self):
        """
        Retorna o título associado a este espaço

        espera:
            nenhum parâmetro
        retorna:
            Titulo - título da propriedade
        """
        return self.titulo

class EspacoInicio(Espaco):
    """
    Espaço GO - início do tabuleiro (posição 0)
    """

    def __init__(self):
        super().__init__("GO", 0)

    def acao(self, jogador, jogo) -> None:
        """
        Não faz nada, pois o salário é pago ao passar pelo GO

        espera:
            jogador: Jogador - jogador
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        pass

class EspacoCadeia(Espaco):
    """
    Espaço da cadeia (posição 10) - apenas visitando
    """

    def __init__(self):
        super().__init__("Cadeia (Visitando)", 10)

    def acao(self, jogador, jogo) -> None:
        """
        Apenas visitando, não acontece nada

        espera:
            jogador: Jogador - jogador
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        pass

class EspacoVaParaCadeia(Espaco):
    """
    Espaço que envia o jogador para a cadeia (posição 30)
    """

    def __init__(self):
        super().__init__("Vá para Cadeia", 30)

    def acao(self, jogador, jogo) -> None:
        """
        Envia o jogador para a cadeia

        espera:
            jogador: Jogador - jogador a ser preso
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        jogador.entrarCadeia()
        # Publica evento para UI/observadores
        try:
            from modules.eventoJogo import TipoEvento
            if hasattr(jogo, '_publicar_evento'):
                jogo._publicar_evento(TipoEvento.JOGADOR_PRESO, {
                    'jogador': jogador,
                    'motivo': 'va_para_cadeia'
                })
        except Exception:
            pass

class EspacoEstacionamentoGratuito(Espaco):
    """
    Espaço de estacionamento gratuito (posição 20)
    """
    def __init__(self):
        super().__init__("Estacionamento Gratuito", 20)

    def acao(self, jogador, jogo) -> None:
        """
        Não faz nada - apenas descanso

        espera:
            jogador: Jogador - jogador
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        pass

class EspacoImposto(Espaco):
    """
    Espaço que cobra pedágio da ponte do jogador
    """

    def __init__(self, nome: str, posicao: int, valor: int):
        super().__init__(nome, posicao)
        self.valor = valor

    def acao(self, jogador, jogo) -> None:
        """
        Cobra pedágio da ponte do jogador

        espera:
            jogador: Jogador - jogador que deve pagar
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        if jogo.banco:
            sucesso = jogo.banco.cobrarTaxa(jogador, self.valor, self.nome)
            # Publicar evento para UI (popup e feed)
            try:
                from modules.eventoJogo import TipoEvento
                if hasattr(jogo, '_publicar_evento'):
                    jogo._publicar_evento(TipoEvento.JOGADOR_PAGOU_TAXA, {
                        'jogador': jogador,
                        'valor': self.valor,
                        'motivo': self.nome,
                        'sucesso': sucesso,
                    })
            except Exception:
                pass
        else:
            jogador.pagarAoBanco(self.valor)

    def getValor(self) -> int:
        """
        Retorna o valor do pedágio da ponte

        espera:
            nenhum parâmetro
        retorna:
            int - valor do pedágio da ponte
        """
        return self.valor

class EspacoCarta(Espaco):
    """
    Espaço de carta Sorte ou Cofre
    ATUALIZADO: Agora publica eventos quando cartas são pegas
    """

    def __init__(self, nome: str, posicao: int, tipo_carta: str):
        super().__init__(nome, posicao)
        self.tipo_carta = tipo_carta

    def acao(self, jogador, jogo) -> None:
        """
        Sorteia e executa uma carta do baralho correspondente
        ATUALIZADO: Publica eventos para a UI

        espera:
            jogador: Jogador - jogador
            jogo: Jogo - instância do jogo
        retorna:
            None
        """
        if hasattr(jogo, 'tabuleiro') and jogo.tabuleiro:
            baralho = jogo.tabuleiro.getBaralho(self.tipo_carta)
            if baralho and not baralho.estaVazio():
                carta = baralho.sacarCarta()
                if carta:
                    # ===== PUBLICAR EVENTO: Carta foi pega =====
                    if hasattr(jogo, '_publicar_evento'):
                        from modules.eventoJogo import TipoEvento
                        
                        # Determinar tipo de evento baseado no tipo de carta
                        if self.tipo_carta.lower() in ['sorte', 'sorte ou revés', 'chance']:
                            tipo_evento = TipoEvento.CARTA_SORTE_PEGA
                        else:  # Cofre, Community Chest, etc
                            tipo_evento = TipoEvento.CARTA_COFRE_PEGA
                        
                        # Publicar evento
                        jogo._publicar_evento(tipo_evento, {
                            'jogador': jogador,
                            'descricao': carta.getDescricao() if hasattr(carta, 'getDescricao') else 'Carta',
                            'tipo_carta': self.tipo_carta
                        })
                    
                    # ===== EXECUTAR AÇÃO DA CARTA =====
                    # Passa 'jogo' como segundo parâmetro para permitir que cartas publiquem eventos
                    if hasattr(carta, 'executar'):
                        # Verificar se o método aceita o parâmetro jogo
                        import inspect
                        sig = inspect.signature(carta.executar)
                        if len(sig.parameters) >= 2:
                            carta.executar(jogador, jogo)
                        else:
                            carta.executar(jogador)
                    
                    # ===== DEVOLVER CARTA AO BARALHO =====
                    # Não devolver se for carta "Sair da Cadeia"
                    if not self._eh_carta_sair_cadeia(carta):
                        baralho.retornarCarta(carta)
    
    def _eh_carta_sair_cadeia(self, carta) -> bool:
        """
        Verifica se a carta é do tipo "Sair da Cadeia"
        
        espera:
            carta: Carta - carta a verificar
        retorna:
            bool - True se for carta "Sair da Cadeia"
        """
        # Verifica pelo tipo da classe
        from modules.carta import CartaSairCadeia
        if isinstance(carta, CartaSairCadeia):
            return True
        
        # Verifica pelo método (fallback)
        if hasattr(carta, 'ehCartaSairCadeia'):
            return carta.ehCartaSairCadeia()
        
        # Verifica pela descrição (último recurso)
        if hasattr(carta, 'getDescricao'):
            descricao = carta.getDescricao().lower()
            if 'sair da cadeia' in descricao or 'saiu da cadeia' in descricao:
                return True
        
        return False

    def getTipoCarta(self) -> str:
        """
        Retorna o tipo de carta deste espaço

        espera:
            nenhum parâmetro
        retorna:
            str - tipo da carta ("Sorte" ou "Cofre")
        """
        return self.tipo_carta