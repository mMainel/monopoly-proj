from __future__ import annotations

class titulo():
    """Classe abstrata mínima para títulos (propriedades/companhias)."""
    def __init__(self, proprietario: object, hipotecado: bool, valorHipoteca: int) -> None:
        self.proprietario = proprietario
        self.hipotecado = hipotecado
        self.valorHipoteca = valorHipoteca

    def hipotecar(self) -> None:
        """Realiza a hipodeta, Banco realiza o pagamento ao proprietário."""
        self.hipotecado = True
    
    def resgatar_hipoteca(self) -> None:
        """Resgata a hipoteca, proprietário paga ao Banco. Banco realiza a transação."""
        self.hipotecado = False
        
    def transferir_proprietario(self, novo_proprietario: object) -> None:
        self.proprietario = novo_proprietario
    
    def __repr__(self) -> str:
        return f"Titulo(proprietario={self.proprietario!r}, preco={self.valorHipoteca!r})"
    
class tituloPropriedade(titulo):
    
    def __init__(self, proprietario: object, hipotecado: bool, valorHipoteca: int, propriedade:object, valor_casa: int, valor_hotel: int, aluguel_por_construcao:int=10) -> None:
        super().__init__(proprietario, hipotecado, valorHipoteca)
        self.propriedade = propriedade
        self.valor_casa = valor_casa
        self.valor_hotel = valor_hotel
        self.aluguel_por_construcao = aluguel_por_construcao
    
    def obter_aluguel_atual(self) -> int:
        return self.propriedade.calcula_aluguel()
        
    def contruir_casa(self) -> None:
        self.propriedade.casas += 1
    
    def construir_hotel(self) -> None:
        self.propriedade.hotel += 1
    
    def vender_construcao(self, tipo:str) -> None:
        if tipo == "casa" and self.propriedade.casas > 0:
            self.propriedade.casas -= 1
        elif tipo == "hotel" and self.propriedade.hotel > 0:
            self.propriedade.hotel -= 1
    
class tituloCompanhia(titulo):
    
    def __init__(self, proprietario: object, hipotecado: bool, valorHipoteca:int, companhia: object) -> None:
        super().__init__(proprietario, hipotecado, valorHipoteca)
        self.companhia = companhia
    
    def obter_aluguel(self, valor_dado: int, quantidade: int) -> int:
        return self.companhia.calcula_aluguel(valor_dado, quantidade)