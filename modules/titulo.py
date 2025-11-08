from abc import ABC, abstractmethod
from typing import Optional

class Titulo(ABC):
    """
    Classe abstrata que representa um título de propriedade
    Serve como base para diferentes tipos de propriedades (lotes, companhias, estações)
    """

    def __init__(self, nome: str, preco: int):
        self.nome = nome
        self.preco = preco
        self.proprietario: Optional[object] = None
        self.hipotecada = False

    @abstractmethod
    def calcularAluguel(self) -> int:
        """
        Calcula o valor do aluguel da propriedade

        espera:
            nenhum parâmetro
        retorna:
            int - valor do aluguel
        """
        pass

    def comprar(self, jogador) -> bool:
        """
        Realiza a compra da propriedade por um jogador

        espera:
            jogador: Jogador - jogador que está comprando
        retorna:
            bool - True se comprou, False se já possui proprietário ou sem saldo
        """
        if self.proprietario is not None:
            return False

        if jogador.getSaldo() < self.preco:
            return False

        if jogador.pagarAoBanco(self.preco):
            self.proprietario = jogador
            jogador.adicionarPropriedade(self)
            return True

        return False

    def hipotecar(self) -> int:
        """
        Hipoteca a propriedade, retornando metade do valor ao proprietário

        espera:
            nenhum parâmetro
        retorna:
            int - valor recebido pela hipoteca (50% do preço)
        """
        if not self.hipotecada and self.proprietario is not None:
            self.hipotecada = True
            valor_hipoteca = self.preco // 2
            self.proprietario.receberDinheiro(valor_hipoteca)
            return valor_hipoteca

        return 0
    
    def deshipotecar(self) -> bool:
        """
        Remove a hipoteca pagando 110% do valor da hipoteca

        espera:
            nenhum parâmetro
        retorna:
            bool - True se deshipotecou, False se nao tinha dinheiro ou nao estava hipotecada
        """
        if not self.hipotecada or self.proprietario is None:
            return False
        
        valor_deshipoteca = int(self.preco * 0.55)
        
        if self.proprietario.getSaldo() < valor_deshipoteca:
            return False
        
        if self.proprietario.pagarAoBanco(valor_deshipoteca):
            self.hipotecada = False
            return True
        
        return False

    def transferirPropriedade(self, novo_proprietario) -> None:
        """
        Transfere a propriedade para outro jogador ou devolve ao banco

        espera:
            novo_proprietario: Jogador - novo dono da propriedade (None = banco)
        retorna:
            None
        """
        if self.proprietario is not None:
            self.proprietario.removerPropriedade(self)

        self.proprietario = novo_proprietario

        if novo_proprietario is not None:
            novo_proprietario.adicionarPropriedade(self)

    # GETTERS

    def getNome(self) -> str:
        """
        Retorna o nome da propriedade

        espera:
            nenhum parâmetro
        retorna:
            str - nome do título
        """
        return self.nome

    def getPreco(self) -> int:
        """
        Retorna o preço de compra da propriedade

        espera:
            nenhum parâmetro
        retorna:
            int - preço de compra
        """
        return self.preco

    def getProprietario(self) -> Optional[object]:
        """
        Retorna o proprietário atual da propriedade

        espera:
            nenhum parâmetro
        retorna:
            Jogador - proprietário atual ou None se disponível
        """
        return self.proprietario

    def estaHipotecada(self) -> bool:
        """
        Verifica se a propriedade está hipotecada

        espera:
            nenhum parâmetro
        retorna:
            bool - True se hipotecada, False caso contrário
        """
        return self.hipotecada

    def estaDisponivel(self) -> bool:
        """
        Verifica se a propriedade está disponível para compra

        espera:
            nenhum parâmetro
        retorna:
            bool - True se disponível, False se possui dono
        """
        return self.proprietario is None