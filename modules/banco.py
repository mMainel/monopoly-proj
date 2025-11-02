from __future__ import annotations
from typing import List,Dict, TYPE_CHECKING, Sequence


from modules.titulo import titulo, tituloCompanhia, tituloPropriedade
from modules.leilao import leilao
from modules.transacao import transacao, tipoTransacao

class banco:
    
    SALARIO : int = 200
    # Sequence[titulo] é usado aqui pois List[titulo] não reconhece as heranças de titulo também como titulo
    def __init__(self, propriedades: Sequence[titulo]) -> None:
        propriedades = propriedades or []
        self.casasDisponiveis: int = 32
        self.hoteisDisponiveis: int = 12
        self.propriedadesDisponiveis: List[titulo] = list(propriedades)
    
    def vender_propriedade(self, titulo: titulo, jogador: object) -> bool:
        """Realiza a venda de uma propriedade sem posse do banco para um jogador.
        Args:
            titulo (titulo): O título da propriedade a ser vendida.
            jogador (object): O jogador que está comprando a propriedade.
        Returns:
            bool: True se a venda foi realizada com sucesso, False caso contrário.
        """
        if titulo not in self.propriedadesDisponiveis:
            return False  # Propriedade não está disponível para venda
        
        valor = titulo.valorHipoteca
        saldo_comprador = jogador.dinheiro 
        
        if saldo_comprador >= valor: # Verifica se o jogador tem dinheiro suficiente
            jogador.debitar(valor)
            titulo.transferir_proprietario(jogador)
            jogador.propriedades.append(titulo) 
            self.propriedadesDisponiveis.remove(titulo)
            return True # Venda realizada com sucesso
        return False # Venda não realizada devido a saldo insuficiente
        
    #Metodos vender\comprar construções mudei o parametro de propriedade para titulo por questões de coerencia com a classe tituloPropriedade
    def vender_casa(self, titulo: titulo|tituloPropriedade)-> bool:
        """Vende uma casa para uma propriedade, se houver disponibilidade."""
        if self.casasDisponiveis > 0:
            titulo.contruir_casa()
            self.casasDisponiveis -= 1
            #print(f"Casa construída em {propriedade.nome}. Casas restantes no banco: {self.hotelsDisponiveis}")
            return True
        else:
            #print("Banco sem casas disponíveis.")
            return False
            
    def vender_hotel(self, titulo: titulo|tituloPropriedade) -> bool:
        """Vende um hotel para uma propriedade, se houver disponibilidade."""
        if self.hoteisDisponiveis > 0:
            self.hoteisDisponiveis -= 1
            titulo.construir_hotel()
            #print(f"hotel construída em {propriedade.nome}. hotel restantes no banco: {self.hoteisDisponiveis}")
            return True
        else:
            #print("Banco sem hotel disponíveis.")
            return False
            
    def comprar_construcao(self, tipo:str, titulo: titulo) -> None:
        """compra uma construção (casa ou hotel) de volta do jogador para o banco."""
        if tipo == "casa":
            self.casasDisponiveis += 1
        elif tipo == "hotel":
            self.hoteisDisponiveis += 1
        titulo.vender_construcao(tipo)
        
        
    def pagar_salario(self, jogador: object) -> None:
        """Paga o salário ao jogador."""
        jogador.creditar(self.SALARIO)
    
    def cobrar_taxa(self, jogador: object, valor: int) -> None:
        """Cobra uma taxa do jogador."""
        jogador.debitar(valor)
    
    def hipotecar(self, titulo: titulo)-> None:
        """Hipotecar um título."""
        if not titulo.hipotecado:
            valor = titulo.valorHipoteca
            titulo.hipotecar()
            titulo.proprietario.creditar(valor)
        
    def resgatar_hipoteca(self, titulo: titulo) -> None:
        """Resgatar a hipoteca de um título."""
        if titulo.hipotecado:
            custo = int(titulo.valor_hipoteca * 1.1)
            jogador = titulo.proprietario
            if jogador.dinheiro >= custo:
                jogador.dinheiro -= custo
                titulo.resgatar_hipoteca()
                #print(f"{jogador.nome} resgatou a hipoteca de {titulo.propriedade.nome} pagando ${custo}.")
            # else:
            #     print(f"{jogador.nome} não tem dinheiro suficiente para resgatar a hipoteca.")
    
    def realizar_leilao(self, propriedade: object, jogadores: List[object]) -> leilao:
        """Realiza um leilão para uma propriedade entre os jogadores interessados."""
        
        leilao_atual = leilao(propriedade, jogadores)
        
        vencedor = leilao_atual.iniciar_leilao()
        vencedor.debitar(leilao_atual.lance_atual)
        return leilao_atual