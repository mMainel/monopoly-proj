from typing import List
from modules.peca import Peca
from modules.regras import Regras
from modules.tituloPropriedade import TituloPropriedade

class Jogador:
    """
    Representa um jogador no jogo
    Responsável por gerenciar estado financeiro, movimentação, propriedades e situação de cadeia
    """
    
    def __init__(self, nome: str, peca: Peca):
        """
        Inicializa um novo jogador com estado padrão
        """
        self.nome = nome
        self.peca = peca
        self.saldo = Regras.DINHEIRO_INICIAL
        self.posicao = 0  
        self.propriedades: List = []
        self.emCadeia = False
        self.naCadeia = 0
        self.cartasSairCadeia = 0
        self.turnosCadeia = 0
        self.estaFalido = False
    
    # MOVIMENTAÇÃO
    
    def mover(self, espacos: int) -> int:
        """
        Move o jogador um número de espaços no tabuleiro de forma circular
        
        espera:
            espacos: int - número de casas a mover
        retorna:
            int - 1 se passou pelo GO, 0 caso contrário
        """
        if self.emCadeia:
            return 0
        
        posicao_antiga = self.posicao
        self.posicao = (self.posicao + espacos) % 40 
        passou_go = 1 if self.posicao < posicao_antiga else 0
        
        return passou_go
    
    def irPara(self, posicao: int) -> bool:
        """
        Move o jogador diretamente para uma posição específica do tabuleiro
        
        espera:
            posicao: int - posição de destino (0-39)
        retorna:
            bool - True se passou pelo GO, False caso contrário
        """
        posicao_antiga = self.posicao
        self.posicao = posicao % 40
        passou_go = self.posicao < posicao_antiga and posicao >= posicao_antiga
        
        return passou_go
    
    # DINHEIRO
    
    def receberDinheiro(self, valor: int) -> None:
        """
        Adiciona dinheiro ao saldo do jogador
        
        espera:
            valor: int - quantia a receber
        retorna:
            None
        """
        if valor > 0:
            self.saldo += valor
    
    def pagarAoBanco(self, valor: int) -> bool:
        """
        Deduz dinheiro do saldo do jogador. Se nao tiver saldo, tenta levantar fundos
        
        espera:
            valor: int - quantia a pagar
        retorna:
            bool - True se pagou com sucesso, False se ficou falido
        """
        if self.saldo >= valor:
            self.saldo -= valor
            return True
        
        deficit = valor - self.saldo
        
        if self.tentarLevantarFundos(deficit):
            if self.saldo >= valor:
                self.saldo -= valor
                return True
        
        self.saldo -= valor
        
        if self.saldo < 0:
            self.estaFalido = True
            return False
        
        return True
    
    # PROPRIEDADES
    
    def adicionarPropriedade(self, propriedade) -> None:
        """
        Adiciona uma propriedade à carteira do jogador
        
        espera:
            propriedade: Titulo - título de propriedade adquirido
        retorna:
            None
        """
        if propriedade not in self.propriedades:
            self.propriedades.append(propriedade)
    
    def removerPropriedade(self, propriedade) -> bool:
        """
        Remove uma propriedade da carteira do jogador
        
        espera:
            propriedade: Titulo - título a ser removido
        retorna:
            bool - True se removeu, False se não possuía
        """
        if propriedade in self.propriedades:
            self.propriedades.remove(propriedade)
            return True
        return False
    
    # GETTERS
    
    def getPosicao(self) -> int:
        """
        Retorna a posição atual do jogador no tabuleiro
        
        espera:
            nenhum parâmetro
        retorna:
            int - posição atual (0-39)
        """
        return self.posicao
    
    def getSaldo(self) -> int:
        """
        Retorna o saldo atual do jogador
        
        espera:
            nenhum parâmetro
        retorna:
            int - saldo em dinheiro
        """
        return self.saldo
    
    def getNome(self) -> str:
        """
        Retorna o nome do jogador
        
        espera:
            nenhum parâmetro
        retorna:
            str - nome do jogador
        """
        return self.nome
    
    def getPeca(self) -> Peca:
        """
        Retorna a peça do jogador
        
        espera:
            nenhum parâmetro
        retorna:
            Peca - peça escolhida
        """
        return self.peca
    
    def getPropriedades(self) -> List:
        """
        Retorna cópia da lista de propriedades do jogador
        
        espera:
            nenhum parâmetro
        retorna:
            List - lista de títulos de propriedade
        """
        return self.propriedades.copy()
    
    # INTEGRAÇÃO COM TÍTULOS E BANCO

    def possuiMonopolio(self, cor: str) -> bool:
        """
        Verifica se o jogador possui todas as propriedades de um grupo/cor
        
        espera:
            cor: str - nome da cor/grupo a verificar
        retorna:
            bool - True se possui monopólio, False caso contrário
        """
        regras = Regras()
        return regras._tem_conjunto_completo(self, cor)

    def pagarAluguel(self, proprietario, valor: int) -> bool:
        """
        Realiza transferência de aluguel para o proprietário da propriedade
        
        espera:
            proprietario: Jogador - jogador que receberá o pagamento
            valor: int - valor do aluguel
        retorna:
            bool - True se pagou com sucesso, False se ficou falido
        """
        if valor <= 0:
            return True

        if self.saldo >= valor:
            self.saldo -= valor
            proprietario.receberDinheiro(valor)
            return True

        self.estaFalido = True
        return False

    def getPropriedadesPorTipo(self, tipo: type) -> List:
        """
        Filtra propriedades do jogador por tipo de título
        
        espera:
            tipo: type - classe de título (TituloPropriedade, TituloCompanhia, etc)
        retorna:
            List - propriedades que são instâncias do tipo fornecido
        """
        return [p for p in self.propriedades if isinstance(p, tipo)]

    def getTotalCasas(self) -> int:
        """
        Calcula o total de casas construídas em todas as propriedades
        
        espera:
            nenhum parâmetro
        retorna:
            int - soma de casas nas propriedades
        """
        total = 0
        for p in self.propriedades:
            if hasattr(p, 'num_casas'):
                total += p.num_casas
        return total

    def getTotalHoteis(self) -> int:
        """
        Calcula o total de hotéis construídos em todas as propriedades
        
        espera:
            nenhum parâmetro
        retorna:
            int - número de hotéis
        """
        total = 0
        regras = Regras()
        max_casas = regras.obter_max_casas()
        
        for p in self.propriedades:
            if hasattr(p, 'num_hoteis'):
                total += p.num_hoteis
            elif hasattr(p, 'num_casas') and p.num_casas > max_casas:
                total += 1
            elif hasattr(p, 'tem_hotel') and p.tem_hotel:
                total += 1
        
        return total

    def calcularPatrimonio(self) -> int:
        """
        Calcula o patrimônio total: saldo + valor de propriedades e construções
        
        espera:
            nenhum parâmetro
        retorna:
            int - valor total do patrimônio
        """
        patrimonio = self.saldo
        
        for p in self.propriedades:
            if hasattr(p, 'preco'):
                patrimonio += p.preco
            if hasattr(p, 'num_casas') and hasattr(p, 'custo_casa'):
                patrimonio += p.num_casas * p.custo_casa
        
        return patrimonio
    
    # CADEIA
    
    def entrarCadeia(self) -> None:
        """
        Coloca o jogador na cadeia
        
        espera:
            nenhum parâmetro
        retorna:
            None
        """
        self.emCadeia = True
        self.naCadeia = 10
        self.posicao = 10
        self.turnosCadeia = 0
    
    def sairCadeia(self) -> None:
        """
        Remove o jogador da cadeia
        
        espera:
            nenhum parâmetro
        retorna:
            None
        """
        self.emCadeia = False
        self.turnosCadeia = 0
    
    def estaEmCadeia(self) -> bool:
        """
        Verifica se o jogador está preso na cadeia
        
        espera:
            nenhum parâmetro
        retorna:
            bool - True se está na cadeia, False caso contrário
        """
        return self.emCadeia
    
    def getTurnosCadeia(self) -> int:
        """
        Retorna há quantos turnos o jogador está na cadeia
        
        espera:
            nenhum parâmetro
        retorna:
            int - número de turnos na cadeia
        """
        return self.turnosCadeia
    
    def incrementarTurnoCadeia(self) -> None:
        """
        Incrementa o contador de turnos na cadeia
        
        espera:
            nenhum parâmetro
        retorna:
            None
        """
        if self.emCadeia:
            self.turnosCadeia += 1
    
    def podeUsarCartaSairCadeia(self) -> bool:
        """
        Verifica se o jogador pode usar carta para sair da cadeia
        
        espera:
            nenhum parâmetro
        retorna:
            bool - True se está na cadeia E tem carta disponível
        """
        return self.emCadeia and self.cartasSairCadeia > 0
    
    def podePagarFianca(self) -> bool:
        """
        Verifica se o jogador tem dinheiro suficiente para pagar a fiança
        
        espera:
            nenhum parâmetro
        retorna:
            bool - True se tem saldo >= fiança
        """
        regras = Regras()
        fianca = regras.obter_valor_prisao()
        return self.saldo >= fianca
    
    def tentarSairCadeiaDupla(self, foiDupla: bool) -> bool:
        """
        Tenta sair da cadeia tirando dupla nos dados ou após 3 turnos
        
        espera:
            foiDupla: bool - True se tirou dupla nos dados
        retorna:
            bool - True se saiu da cadeia, False se continua preso
        """
        if not self.emCadeia:
            return False
        
        if foiDupla:
            self.sairCadeia()
            return True
        
        if self.turnosCadeia >= 3:
            regras = Regras()
            fianca = regras.obter_valor_prisao()
            if self.pagarAoBanco(fianca):
                self.sairCadeia()
                return True
        
        return False
    
    # CARTAS
    
    def adicionarCartaSairCadeia(self) -> None:
        """
        Adiciona uma carta 'Sair da Cadeia' ao jogador
        
        espera:
            nenhum parâmetro
        retorna:
            None
        """
        self.cartasSairCadeia += 1
    
    def usarCartaSairCadeia(self) -> bool:
        """
        Usa uma carta 'Sair da Cadeia' se o jogador tiver
        
        espera:
            nenhum parâmetro
        retorna:
            bool - True se usou a carta, False se não tinha
        """
        if self.cartasSairCadeia > 0:
            self.cartasSairCadeia -= 1
            return True
        return False
    
    def getCartasSairCadeia(self) -> int:
        """
        Retorna quantidade de cartas 'Sair da Cadeia' disponíveis
        
        espera:
            nenhum parâmetro
        retorna:
            int - número de cartas
        """
        return self.cartasSairCadeia
    
    # FALÊNCIA
    
    def declararFalencia(self) -> None:
        """
        Declara o jogador como falido e zera seu saldo
        
        espera:
            nenhum parâmetro
        retorna:
            None
        """
        self.estaFalido = True
        self.saldo = 0
    
    def verificarFalencia(self) -> bool:
        """
        Verifica se o jogador está falido

        espera:
            nenhum parâmetro
        retorna:
            bool - True se está falido, False caso contrário
        """
        return self.estaFalido
    
    # GESTAO FINANCEIRA
    def obterPropriedadesHipotecaveis(self) -> List:
        """
        Retorna lista de propriedades que podem ser hipotecadas
        
        espera:
            nenhum parâmetro
        retorna:
            List - propriedades sem hipoteca e sem construcoes
        """
        
        hipotecaveis = []
        for prop in self.propriedades:
            if not prop.estaHipotecada():
                if isinstance(prop, TituloPropriedade):
                    if hasattr(prop, 'podeHipotecar') and prop.podeHipotecar():
                        hipotecaveis.append(prop)
                else:
                    hipotecaveis.append(prop)
        
        return hipotecaveis
    
    def obterPropriedadesDeshipotecaveis(self) -> List:
        """
        Retorna lista de propriedades hipotecadas que podem ser reativadas
        
        espera:
            nenhum parâmetro
        retorna:
            List - propriedades hipotecadas
        """
        return [p for p in self.propriedades if p.estaHipotecada()]
    
    def obterPropriedadesComConstrucoes(self) -> List:
        """
        Retorna lista de propriedades com casas ou hoteis que podem ser vendidos
        
        espera:
            nenhum parâmetro
        retorna:
            List - propriedades com construcoes
        """
        
        com_construcoes = []
        for prop in self.propriedades:
            if isinstance(prop, TituloPropriedade):
                if prop.num_casas > 0 or prop.tem_hotel:
                    com_construcoes.append(prop)
        
        return com_construcoes
    
    def tentarLevantarFundos(self, valor_necessario: int) -> bool:
        """
        Tenta levantar fundos vendendo casas e hipotecando propriedades
        
        espera:
            valor_necessario: int - quanto precisa levantar
        retorna:
            bool - True se conseguiu o valor, False caso contrario
        """
        valor_levantado = 0
        
        propriedades_com_construcoes = self.obterPropriedadesComConstrucoes()
        propriedades_com_construcoes.sort(key=lambda p: p.num_casas, reverse=True)
        
        for prop in propriedades_com_construcoes:
            while valor_levantado < valor_necessario and (prop.num_casas > 0 or prop.tem_hotel):
                if prop.tem_hotel:
                    if prop.venderHotel():
                        valor_levantado += prop.getCustoCasa() // 2
                elif prop.num_casas > 0:
                    if prop.venderCasa():
                        valor_levantado += prop.getCustoCasa() // 2
                else:
                    break
            
            if valor_levantado >= valor_necessario:
                return True
        
        propriedades_hipotecaveis = self.obterPropriedadesHipotecaveis()
        propriedades_hipotecaveis.sort(key=lambda p: p.getPreco(), reverse=True)
        
        for prop in propriedades_hipotecaveis:
            if valor_levantado >= valor_necessario:
                break
            
            valor_hipoteca = prop.hipotecar()
            if valor_hipoteca > 0:
                valor_levantado += valor_hipoteca
        
        return valor_levantado >= valor_necessario
