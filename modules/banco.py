from typing import List, Optional
from modules.transacao import Transacao
from modules.tipoTransacao import TipoTransacao
from modules.regras import Regras

class Banco:
    """
    Gerencia transações financeiras e recursos do jogo (casas, hotéis, propriedades).
    Atua como intermediário em compras, vendas, leilões e mantém histórico de transações
    """

    def __init__(self):
        self.casas_disponiveis: int = 32
        self.hoteis_disponiveis: int = 12
        self.propriedades: List = []
        self.historico_transacoes: List[Transacao] = []
        self._regras: Regras = Regras()
    
    # INTEGRAÇÃO COM JOGADOR 
    
    def _registrar_transacao(self, tipo: TipoTransacao, valor: int, origem=None, destino=None, descricao: str = "") -> None:
        """
        Registra uma transação no histórico

        espera:
            tipo: TipoTransacao - tipo da transação
            valor: int - valor movimentado
            origem: Jogador - origem do dinheiro
            destino: Jogador - destino do dinheiro
            descricao: str - descrição opcional
        retorna:
            None
        """
        transacao = Transacao(tipo, valor, origem, destino, descricao)
        self.historico_transacoes.append(transacao)

    def transferir(self, origem, destino, valor: int) -> bool:
        """
        Transfere dinheiro entre dois jogadores

        espera:
            origem: Jogador - jogador que paga
            destino: Jogador - jogador que recebe
            valor: int - quantia a transferir
        retorna:
            bool - True se transferiu com sucesso, False se origem ficou falido
        """
        if valor <= 0:
            return True

        if origem.getSaldo() >= valor:
            origem.pagarAoBanco(valor)
            destino.receberDinheiro(valor)
            self._registrar_transacao(TipoTransacao.TRANSFERENCIA, valor, origem, destino)
            return True

        return False
    
    def pagarSalario(self, jogador) -> None:
        """
        Paga o salário ao jogador por passar pelo GO

        espera:
            jogador: Jogador - jogador que receberá o salário
        retorna:
            None
        """
        salario = self._regras.obter_salario_inicio()
        jogador.receberDinheiro(salario)
        self._registrar_transacao(TipoTransacao.SALARIO, salario, None, jogador, "Passou pelo GO")
    
    def cobrarTaxa(self, jogador, valor: int, descricao: str = "Pedágio da Ponte") -> bool:
        """
        Cobra uma taxa ou pedágio do jogador

        espera:
            jogador: Jogador - jogador que pagará a taxa
            valor: int - valor da taxa
            descricao: str - descrição do pedágio
        retorna:
            bool - True se pagou, False se ficou falido
        """
        sucesso = jogador.pagarAoBanco(valor)
        if sucesso:
            self._registrar_transacao(TipoTransacao.IMPOSTO, valor, jogador, None, descricao)
        return sucesso
    
    # INTEGRAÇÃO COM TÍTULOS
    
    def venderPropriedade(self, titulo, jogador) -> bool:
        """
        Vende uma propriedade ao jogador

        espera:
            titulo: Titulo - propriedade a vender
            jogador: Jogador - comprador
        retorna:
            bool - True se vendeu, False se jogador não tem dinheiro
        """
        if titulo.getProprietario() is not None:
            return False

        if jogador.getSaldo() < titulo.getPreco():
            return False

        sucesso = jogador.pagarAoBanco(titulo.getPreco())
        if sucesso:
            titulo.proprietario = jogador
            jogador.adicionarPropriedade(titulo)
            self._registrar_transacao(
                TipoTransacao.COMPRA_PROPRIEDADE,
                titulo.getPreco(),
                jogador,
                None,
                f"Compra de {titulo.getNome()}"
            )
            return True

        return False
    
    def hipotecarPropriedade(self, titulo, jogador) -> int:
        """
        Hipoteca uma propriedade e retorna o valor ao jogador

        espera:
            titulo: Titulo - propriedade a hipotecar
            jogador: Jogador - proprietário
        retorna:
            int - valor recebido pela hipoteca
        """
        if titulo.getProprietario() != jogador:
            return 0

        if titulo.estaHipotecada():
            return 0

        valor = titulo.hipotecar()
        if valor > 0:
            self._registrar_transacao(
                TipoTransacao.HIPOTECA,
                valor,
                None,
                jogador,
                f"Hipoteca de {titulo.getNome()}"
            )

        return valor
    
    # CONSTRUÇÕES
    
    def comprarCasa(self, propriedade, jogador) -> bool:
        """
        Vende uma casa ao jogador para construir

        espera:
            propriedade: TituloPropriedade - onde construir
            jogador: Jogador - comprador
        retorna:
            bool - True se construiu, False caso contrário
        """
        if self.casas_disponiveis <= 0:
            return False

        if propriedade.getProprietario() != jogador:
            return False

        if not hasattr(propriedade, 'construirCasa'):
            return False

        sucesso = propriedade.construirCasa()
        if sucesso:
            self.casas_disponiveis -= 1
            self._registrar_transacao(
                TipoTransacao.CONSTRUCAO,
                propriedade.getCustoCasa(),
                jogador,
                None,
                f"Casa em {propriedade.getNome()}"
            )

        return sucesso

    def comprarHotel(self, propriedade, jogador) -> bool:
        """
        Vende um hotel ao jogador

        espera:
            propriedade: TituloPropriedade - onde construir
            jogador: Jogador - comprador
        retorna:
            bool - True se construiu, False caso contrário
        """
        if self.hoteis_disponiveis <= 0:
            return False

        if propriedade.getProprietario() != jogador:
            return False

        if not hasattr(propriedade, 'construirHotel'):
            return False

        sucesso = propriedade.construirHotel()
        if sucesso:
            self.hoteis_disponiveis -= 1
            self.casas_disponiveis += 4
            self._registrar_transacao(
                TipoTransacao.CONSTRUCAO,
                propriedade.getCustoCasa(),
                jogador,
                None,
                f"Hotel em {propriedade.getNome()}"
            )

        return sucesso

    def venderCasa(self, propriedade, jogador) -> bool:
        """
        Compra de volta uma casa do jogador

        espera:
            propriedade: TituloPropriedade - propriedade com casa
            jogador: Jogador - vendedor
        retorna:
            bool - True se vendeu, False caso contrário
        """
        if propriedade.getProprietario() != jogador:
            return False

        if not hasattr(propriedade, 'venderCasa'):
            return False

        sucesso = propriedade.venderCasa()
        if sucesso:
            self.casas_disponiveis += 1

        return sucesso

    def venderHotel(self, propriedade, jogador) -> bool:
        """
        Compra de volta um hotel do jogador

        espera:
            propriedade: TituloPropriedade - propriedade com hotel
            jogador: Jogador - vendedor
        retorna:
            bool - True se vendeu, False caso contrário
        """
        if propriedade.getProprietario() != jogador:
            return False

        if not hasattr(propriedade, 'venderHotel'):
            return False

        sucesso = propriedade.venderHotel()
        if sucesso:
            self.hoteis_disponiveis += 1
            self.casas_disponiveis -= 4

        return sucesso

    # GETTERS E UTILIDADES

    def getCasasDisponiveis(self) -> int:
        """
        Retorna quantidade de casas disponíveis para compra

        espera:
            nenhum parâmetro
        retorna:
            int - número de casas disponíveis
        """
        return self.casas_disponiveis

    def getHoteisDisponiveis(self) -> int:
        """
        Retorna quantidade de hotéis disponíveis para compra

        espera:
            nenhum parâmetro
        retorna:
            int - número de hotéis disponíveis
        """
        return self.hoteis_disponiveis

    def getHistoricoTransacoes(self) -> List[Transacao]:
        """
        Retorna histórico de todas as transações

        espera:
            nenhum parâmetro
        retorna:
            List[Transacao] - lista de transações
        """
        return self.historico_transacoes.copy()

    def getTransacoesPorJogador(self, jogador) -> List[Transacao]:
        """
        Retorna transações relacionadas a um jogador específico

        espera:
            jogador: Jogador - jogador a filtrar
        retorna:
            List[Transacao] - transações do jogador
        """
        return [
            t for t in self.historico_transacoes
            if t.getOrigem() == jogador or t.getDestino() == jogador
        ]

    def getTransacoesPorTipo(self, tipo: TipoTransacao) -> List[Transacao]:
        """
        Retorna transações de um tipo específico

        espera:
            tipo: TipoTransacao - tipo a filtrar
        retorna:
            List[Transacao] - transações do tipo
        """
        return [t for t in self.historico_transacoes 
                if t.getTipo() == tipo]
