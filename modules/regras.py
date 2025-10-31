from typing import Optional

class Regras:
    """
    Centraliza as regras e validações do Monopoly
    """
    
    DINHEIRO_INICIAL: int = 1500
    SALARIO_VOLTA: int = 200
    FIANCA_CADEIA: int = 50
    MAX_CASAS: int = 4
    MAX_DUPLAS: int = 2
    
    def validar_compra(self, jogador: object, propriedade: object) -> bool:
        """
        Verifica se um jogador pode comprar uma propriedade
        """
        if propriedade.proprietario is not None:
            return False
        
        if jogador.dinheiro < propriedade.preco:
            return False
        
        return True
    
    def validar_construcao(self, jogador: object, propriedade: object) -> bool:
        """
        Verifica se pode construir casa/hotel em uma propriedade
        """
        if propriedade.proprietario != jogador:
            return False
        
        if not hasattr(propriedade, 'num_casas'):
            return False
        
        if propriedade.num_casas >= self.MAX_CASAS:
            return False
        
        if jogador.dinheiro < propriedade.custo_casa:
            return False
        
        return True
    
    def calcular_aluguel(self, propriedade: object) -> int:
        """
        Calcula o valor do aluguel de uma propriedade
        """
        if not hasattr(propriedade, 'num_casas'):
            return propriedade.aluguel_base
        
        if propriedade.num_casas > 0:
            if hasattr(propriedade, 'alugueis') and len(propriedade.alugueis) >= propriedade.num_casas:
                return propriedade.alugueis[propriedade.num_casas - 1]
        
        return propriedade.aluguel_base
    
    def obter_saldo_inicial(self) -> int:
        """
        Retorna o saldo inicial de cada jogador
        """
        return self.DINHEIRO_INICIAL
    
    def obter_salario_inicio(self) -> int:
        """
        Retorna o valor recebido ao passar pelo Início
        """
        return self.SALARIO_VOLTA
    
    def obter_valor_prisao(self) -> int:
        """
        Retorna o valor da fiança para sair da prisão
        """
        return self.FIANCA_CADEIA
    
    def obter_max_casas(self) -> int:
        """
        Retorna o número máximo de casas por propriedade
        """
        return self.MAX_CASAS
    
    def obter_max_duplas(self) -> int:
        """
        Retorna o número máximo de duplas consecutivas antes de ir preso
        """
        return self.MAX_DUPLAS
    
    def _tem_conjunto_completo(self, jogador: object, cor: str) -> bool:
        """
        Verifica se jogador possui todas as propriedades de uma cor
        Implementação futura so
        """
        return False