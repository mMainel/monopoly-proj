from modules.jogador import Jogador
from modules.peca import Peca
import random

class JogadorIA(Jogador):
    """
    Jogador controlado por IA simples (dummy)
    Toma decisões básicas automaticamente
    """

    def __init__(self, nome: str, peca: Peca):
        super().__init__(nome, peca)
        self.eh_ia = True

    def decidir_comprar_propriedade(self, propriedade) -> bool:
        """
        Decide se deve comprar uma propriedade
        IA dummy: compra se tiver dinheiro suficiente e sobrar pelo menos 200

        espera:
            propriedade: Titulo - propriedade disponível
        retorna:
            bool - True se decidiu comprar
        """
        preco = propriedade.getPreco() if hasattr(propriedade, 'getPreco') else propriedade.preco
        return self.saldo >= (preco + 200)

    def decidir_construir_casa(self, propriedade) -> bool:
        """
        Decide se deve construir casa em uma propriedade
        IA dummy: constrói se tiver dinheiro e sobrar pelo menos 300

        espera:
            propriedade: TituloPropriedade - propriedade onde pode construir
        retorna:
            bool - True se decidiu construir
        """
        if not hasattr(propriedade, 'custo_casa'):
            return False

        custo = propriedade.getCustoCasa() if hasattr(propriedade, 'getCustoCasa') else propriedade.custo_casa
        return self.saldo >= (custo + 300)

    def decidir_pagar_fianca(self) -> bool:
        """
        Decide se deve pagar fiança para sair da cadeia
        IA dummy: paga se tiver mais de 500 de saldo

        espera:
            nenhum parâmetro
        retorna:
            bool - True se decidiu pagar
        """
        return self.saldo > 500

    def escolher_opcao_cadeia(self) -> str:
        """
        Escolhe como tentar sair da cadeia
        IA dummy: usa carta se tiver, senão paga se tiver dinheiro, senão tenta dupla

        espera:
            nenhum parâmetro
        retorna:
            str - "carta", "fianca" ou "dupla"
        """
        if self.podeUsarCartaSairCadeia():
            return "carta"
        elif self.decidir_pagar_fianca():
            return "fianca"
        else:
            return "dupla"

    def escolher_propriedade_construir(self, propriedades_disponiveis: list):
        """
        Escolhe em qual propriedade construir
        IA dummy: escolhe aleatoriamente entre as disponíveis

        espera:
            propriedades_disponiveis: list - lista de propriedades onde pode construir
        retorna:
            Titulo - propriedade escolhida ou None
        """
        if not propriedades_disponiveis:
            return None
        return random.choice(propriedades_disponiveis)

    def decidir_dar_lance(self, propriedade, lance_atual: int) -> int:
        """
        Decide se deve dar lance em um leilao e qual valor
        IA dummy: da lances incrementais ate 70% do preco original
        
        espera:
            propriedade: Titulo - propriedade em leilao
            lance_atual: int - maior lance atual
        retorna:
            int - valor do lance ou 0 se nao quer dar lance
        """
        preco = propriedade.getPreco() if hasattr(propriedade, 'getPreco') else propriedade.preco
        limite = int(preco * 0.7)
        
        if lance_atual >= limite:
            return 0
        
        incremento = max(10, preco // 20)
        novo_lance = lance_atual + incremento
        
        if novo_lance > limite or self.saldo < novo_lance + 100:
            return 0
        
        return novo_lance
    
    def decidir_hipotecar(self) -> bool:
        """
        Decide se deve hipotecar propriedades quando precisa de dinheiro
        IA dummy: hipoteca se saldo estiver abaixo de 100
        
        espera:
            nenhum parametro
        retorna:
            bool - True se deve hipotecar
        """
        return self.saldo < 100
    
    def decidir_vender_casa(self) -> bool:
        """
        Decide se deve vender casas quando precisa de dinheiro
        IA dummy: vende se saldo estiver abaixo de 50
        
        espera:
            nenhum parametro
        retorna:
            bool - True se deve vender
        """
        return self.saldo < 50

