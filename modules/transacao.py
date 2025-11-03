from datetime import datetime
from typing import Optional
from tipoTransacao import TipoTransacao

class Transacao:
    """
    Registra uma transação financeira no jogo
    Armazena informações sobre movimentações de dinheiro entre jogadores e banco
    """

    def __init__(self, tipo: TipoTransacao, valor: int, origem=None, destino=None, descricao: str = ""):
        self.tipo = tipo
        self.valor = valor
        self.origem = origem
        self.destino = destino
        self.descricao = descricao
        self.timestamp = datetime.now()

    def getTipo(self) -> TipoTransacao:
        """
        Retorna o tipo da transação

        espera:
            nenhum parâmetro
        retorna:
            TipoTransacao - tipo da transação
        """
        return self.tipo

    def getValor(self) -> int:
        """
        Retorna o valor da transação

        espera:
            nenhum parâmetro
        retorna:
            int - valor movimentado
        """
        return self.valor

    def getOrigem(self) -> Optional[object]:
        """
        Retorna a origem da transação

        espera:
            nenhum parâmetro
        retorna:
            Jogador - jogador origem ou None se for do banco
        """
        return self.origem

    def getDestino(self) -> Optional[object]:
        """
        Retorna o destino da transação

        espera:
            nenhum parâmetro
        retorna:
            Jogador - jogador destino ou None se for para o banco
        """
        return self.destino

    def getDescricao(self) -> str:
        """
        Retorna a descrição da transação

        espera:
            nenhum parâmetro
        retorna:
            str - descrição detalhada
        """
        return self.descricao

    def getTimestamp(self) -> datetime:
        """
        Retorna o momento em que a transação ocorreu

        espera:
            nenhum parâmetro
        retorna:
            datetime - timestamp da transação
        """
        return self.timestamp

    def __str__(self) -> str:
        """
        Representação em string da transação

        espera:
            nenhum parâmetro
        retorna:
            str - descrição formatada da transação
        """
        origem_str = self.origem.getNome() if self.origem else "Banco"
        destino_str = self.destino.getNome() if self.destino else "Banco"

        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.tipo.value}: ${self.valor} ({origem_str} -> {destino_str})"
