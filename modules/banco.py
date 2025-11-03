from typing import List

class Banco:
    """
    Gerencia transações financeiras e recursos do jogo (casas, hotéis, propriedades)
    Atua como intermediário em compras, vendas e leilões
    """
    
    def __init__(self):
        self.casas_disponiveis: int = 32
        self.hoteis_disponiveis: int = 32
        self.propriedades: List = []
    
    # INTEGRAÇÃO COM JOGADOR 
    
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
        from regras import Regras
        regras = Regras()
        salario = regras.obter_salario_inicio()
        jogador.receberDinheiro(salario)
    
    def cobrarTaxa(self, jogador, valor: int) -> bool:
        """
        Cobra uma taxa ou imposto do jogador
        
        espera:
            jogador: Jogador - jogador que pagará a taxa
            valor: int - valor da taxa
        retorna:
            bool - True se pagou, False se ficou falido
        """
        return jogador.pagarAoBanco(valor)
    
    # INTEGRAÇÃO COM TÍTULOS
    
    def venderPropriedade(self, titulo, jogador) -> bool:
        """
        Vende uma propriedade ao jogador (ainda vou fazer)
        
        espera:
            titulo: Titulo - propriedade a vender
            jogador: Jogador - comprador
        retorna:
            bool - True se vendeu, False se jogador não tem dinheiro
        """
        pass
    
    def hipotecarPropriedade(self, titulo, jogador) -> int:
        """
        Hipoteca uma propriedade e retorna o valor ao jogador (ainda vou fazer)
        
        espera:
            titulo: Titulo - propriedade a hipotecar
            jogador: Jogador - proprietário
        retorna:
            int - valor recebido pela hipoteca
        """
        pass
    
    # CONSTRUÇÕES
    
    def comprarCasa(self, propriedade, jogador) -> bool:
        """
        Vende uma casa ao jogador para construir (idem)
        
        espera:
            propriedade: TituloPropriedade - onde construir
            jogador: Jogador - comprador
        retorna:
            bool - True se construiu, False caso contrário
        """
        pass
    
    def comprarHotel(self, propriedade, jogador) -> bool:
        """
        Vende um hotel ao jogador (idem)
        
        espera:
            propriedade: TituloPropriedade - onde construir
            jogador: Jogador - comprador
        retorna:
            bool - True se construiu, False caso contrário
        """
        pass
