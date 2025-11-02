from __future__ import annotations
from typing import List


class leilao:
    """Leião realizado pelo banco para uma propriedade."""
    def __init__(self, propriedade: object, participantes: List[object]):
        self.propriedade = propriedade
        self.participantes = participantes
        self.lance_atual: int = 0
        self.vencedor: object = None
    
    def iniciar_leilao(self) -> object:
        """Realiza o leilão entre os participantes. Leilão só termina quando nenhum jogador quiser mais dar lances.
        Returns:
            object: Jogador vencedor do leilão.
        """
        maior_lance = (0, None) # Tupla de (lance, jogador)
        lance = 0
        count = 0
        while lance == maior_lance[0] or maior_lance[1] is None:
            #print("Nova rodada de lances no leilão.", count)
            count += 1
            lance_rodada = (0, None)
            for jogador in self.participantes: # Enquanto jogador quiser participar
                #print(f"Vez de {jogador.nome} no leilão.")
                lancej = jogador.realizarlance()
                if lancej > jogador.dinheiro:
                    lancej = jogador.dinheiro  # Limita o lance ao dinheiro disponível
                if lancej > lance_rodada[0]:
                    lance_rodada = (lancej, jogador)
                #print(f"{jogador.nome} deu um lance de {lancej}., lance atual é {maior_lance[0]}")
            lance = lance_rodada[0]
            if lance > maior_lance[0]:
                maior_lance = lance_rodada
            elif lance == maior_lance[0]:
                # Empate da rodada anterior, mantém o maior_lance atual primeiro a fazer lance ganha
                break
        #print(f"Leilão encerrado. Vencedor: {maior_lance[1].nome} com lance de {maior_lance[0]}.")
        self.lance_atual, self.vencedor = maior_lance
        return self.vencedor
        