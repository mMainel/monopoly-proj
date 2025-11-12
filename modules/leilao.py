from typing import List, Optional, Tuple

class Leilao:
    """
    Gerencia o processo de leilão de propriedades
    Responsável por controlar lances, validar participantes e determinar vencedor
    """
    
    def __init__(self):
        self.propriedade = None
        self.participantes: List = []
        self.lances: dict = {}
        self.lance_minimo: int = 1
        self.vencedor = None
        self.valor_final: int = 0
        self.ativo: bool = False
    
    # CONTROLE DO LEILÃO
    
    def iniciarLeilao(self, propriedade, jogadores: List) -> None:
        """
        Inicia um leilão para uma propriedade com os jogadores fornecidos
        
        espera:
            propriedade: Propriedade - propriedade a ser leiloada
            jogadores: List[Jogador] - lista de jogadores participantes
        retorna:
            None
        """
        if not jogadores or len(jogadores) == 0:
            raise ValueError("Leilão precisa de pelo menos um participante")
        
        self.propriedade = propriedade
        self.participantes = jogadores.copy()
        self.lances = {jogador: 0 for jogador in jogadores}
        self.lance_minimo = 1
        self.vencedor = None
        self.valor_final = 0
        self.ativo = True
    
    def fazerLance(self, jogador, valor: int) -> bool:
        """
        Registra um lance de um jogador no leilão
        
        espera:
            jogador: Jogador - jogador que está dando o lance
            valor: int - valor do lance
        retorna:
            bool - True se o lance foi aceito, False caso contrário
        """
        if not self.ativo:
            return False
        
        if jogador not in self.participantes:
            return False
        
        if valor < self.lance_minimo:
            return False
        
        lance_atual_maior = max(self.lances.values()) if self.lances else 0
        if valor <= lance_atual_maior:
            return False
        
        if jogador.getSaldo() < valor:
            return False
        
        self.lances[jogador] = valor
        self.lance_minimo = valor + 1
        
        return True
    
    def finalizarLeilao(self) -> Tuple[Optional[object], int]:
        """
        Finaliza o leilão e determina o vencedor

        espera:
            nenhum parâmetro
        retorna:
            Tuple[Jogador, int] - tupla com (vencedor, valor_final) ou (None, 0) se não houve lances
        """
        if not self.ativo:
            return (None, 0)

        self.ativo = False

        if not self.lances or all(valor == 0 for valor in self.lances.values()):
            return (None, 0)

        self.vencedor = max(self.lances, key=self.lances.get)
        self.valor_final = self.lances[self.vencedor]

        if self.valor_final > 0 and self.propriedade:
            if self.vencedor.pagarAoBanco(self.valor_final):
                if hasattr(self.propriedade, 'proprietario'):
                    self.propriedade.proprietario = self.vencedor
                self.vencedor.adicionarPropriedade(self.propriedade)

        return (self.vencedor, self.valor_final)
    
    def desistir(self, jogador) -> bool:
        """
        Remove um jogador do leilão em andamento

        espera:
            jogador: Jogador - jogador que desiste do leilão
        retorna:
            bool - True se desistiu, False se não estava participando
        """
        if not self.ativo:
            return False

        if jogador not in self.participantes:
            return False

        self.participantes.remove(jogador)
        if jogador in self.lances:
            del self.lances[jogador]

        if len(self.participantes) <= 1:
            return True

        return True

    def cancelarLeilao(self) -> None:
        """
        Cancela o leilão em andamento

        espera:
            nenhum parâmetro
        retorna:
            None
        """
        self.ativo = False
        self.lances.clear()
        self.participantes.clear()
        self.vencedor = None
        self.valor_final = 0
    
    # GETTERS
    
    def getLanceMaior(self) -> int:
        """
        Retorna o maior lance atual
        
        espera:
            nenhum parâmetro
        retorna:
            int - valor do maior lance ou 0 se não houver lances
        """
        if not self.lances:
            return 0
        return max(self.lances.values())
    
    def getLiderAtual(self) -> Optional[object]:
        """
        Retorna o jogador com o maior lance atual
        
        espera:
            nenhum parâmetro
        retorna:
            Jogador - jogador líder ou None se não houver lances
        """
        if not self.lances or all(valor == 0 for valor in self.lances.values()):
            return None
        return max(self.lances, key=self.lances.get)
    
    def getLancesRealizados(self) -> dict:
        """
        Retorna o dicionário com todos os lances realizados
        
        espera:
            nenhum parâmetro
        retorna:
            dict - cópia do dicionário de lances {jogador: valor}
        """
        return self.lances.copy()
    
    def estaAtivo(self) -> bool:
        """
        Verifica se o leilão está ativo

        espera:
            nenhum parâmetro
        retorna:
            bool - True se ativo, False caso contrário
        """
        return self.ativo

    def getParticipantes(self) -> List:
        """
        Retorna a lista de participantes do leilão

        espera:
            nenhum parâmetro
        retorna:
            List - cópia da lista de jogadores participantes
        """
        return self.participantes.copy()

    def getPropriedade(self):
        """
        Retorna a propriedade que está sendo leiloada

        espera:
            nenhum parâmetro
        retorna:
            Titulo - propriedade em leilão
        """
        return self.propriedade

    def getVencedor(self):
        """
        Retorna o vencedor do leilão após finalização

        espera:
            nenhum parâmetro
        retorna:
            Jogador - vencedor ou None se ainda não finalizado
        """
        return self.vencedor
