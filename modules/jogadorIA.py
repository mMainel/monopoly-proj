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

    def avaliar_negociacao(self, props_oferecidas, props_recebidas, dinheiro_oferecido, dinheiro_recebido) -> bool:
        """
        Avalia se uma proposta de negociação é vantajosa para a IA
        
        Critérios:
        1. Monopólios da IA devem aumentar ou se manter na diferença total
        2. Monopólios ganhos devem ser mais caros que os perdidos
        
        espera:
            props_oferecidas: list - propriedades que IA vai dar
            props_recebidas: list - propriedades que IA vai receber
            dinheiro_oferecido: int - dinheiro que IA vai dar
            dinheiro_recebido: int - dinheiro que IA vai receber
        retorna:
            bool - True se aceita a negociação
        """
        from modules.tituloPropriedade import TituloPropriedade
        
        props_atuais = self.getPropriedades().copy()
        
        for p in props_oferecidas:
            if p in props_atuais:
                props_atuais.remove(p)
        
        props_atuais.extend(props_recebidas)
        
        saldo_futuro = self.saldo - dinheiro_oferecido + dinheiro_recebido
        
        if saldo_futuro < 200:
            return False
        
        monopolios_antes = self._contar_monopolios_e_proximidade(self.getPropriedades())
        
        monopolios_depois = self._contar_monopolios_e_proximidade(props_atuais)
        
        novos_monopolios = monopolios_depois['completos'] - monopolios_antes['completos']
        monopolios_perdidos = monopolios_antes['completos'] - monopolios_depois['completos']
        
        if novos_monopolios > monopolios_perdidos:
            return True
        
        if monopolios_perdidos > 0 and novos_monopolios == 0:
            return False
        
        ganho_proximidade = 0
        valor_grupos_ganhos = 0
        valor_grupos_perdidos = 0
        
        for cor, info in monopolios_depois['grupos'].items():
            antes = monopolios_antes['grupos'].get(cor, {'count': 0, 'total': 0, 'valor_total': 0})
            
            if info['count'] == info['total'] and antes['count'] < antes['total']:
                ganho_proximidade += 3
                valor_grupos_ganhos += info['valor_total']
            
            elif info['count'] > antes['count']:
                ganho_proximidade += 1
                valor_grupos_ganhos += info['valor_total']
            
            elif info['count'] < antes['count']:
                perda = antes['count'] - info['count']
                ganho_proximidade -= perda
                valor_grupos_perdidos += antes['valor_total']
        
        for cor in monopolios_antes['grupos']:
            if cor not in monopolios_depois['grupos']:
                ganho_proximidade -= 2
                valor_grupos_perdidos += monopolios_antes['grupos'][cor]['valor_total']
        
        valor_oferecido = sum(p.getPreco() for p in props_oferecidas if hasattr(p, 'getPreco'))
        valor_recebido = sum(p.getPreco() for p in props_recebidas if hasattr(p, 'getPreco'))
        
        balanco_financeiro = (valor_recebido + dinheiro_recebido) - (valor_oferecido + dinheiro_oferecido)
        
        if ganho_proximidade <= 0:
            return False
        
        if valor_grupos_perdidos > valor_grupos_ganhos:
            if ganho_proximidade < 3:
                return False
        
        if ganho_proximidade > 0 and balanco_financeiro > -300:
            return True
        
        if ganho_proximidade >= 3:
            return True
        
        return False

    def _contar_monopolios_e_proximidade(self, propriedades_lista):
        """
        Analisa monopólios completos e proximidade de completar grupos
        
        espera:
            propriedades_lista: list - lista de propriedades a analisar
        retorna:
            dict - informações sobre monopólios e grupos
        """
        from modules.tituloPropriedade import TituloPropriedade
        from modules.regras import Regras
        
        regras = Regras()
        grupos = {}
        monopolios_completos = 0
        
        for prop in propriedades_lista:
            if isinstance(prop, TituloPropriedade):
                cor = prop.getCor()
                if cor not in grupos:
                    grupos[cor] = {
                        'count': 0,
                        'total': regras._total_propriedades_grupo(cor),
                        'valor_total': 0
                    }
                grupos[cor]['count'] += 1
                grupos[cor]['valor_total'] += prop.getPreco()
        
        for cor, info in grupos.items():
            if info['count'] == info['total']:
                monopolios_completos += 1
        
        return {
            'completos': monopolios_completos,
            'grupos': grupos
        }

    def tentar_construir_casas(self, jogo):
        """
        Tenta construir casas nas propriedades onde tem monopólio
        IA constrói casas de forma equilibrada entre propriedades do mesmo grupo
        Não constrói se ficar com saldo baixo (mínimo R$500)
        
        espera:
            jogo: Jogo - instância do jogo para acessar métodos de construção
        retorna:
            None
        """
        from modules.tituloPropriedade import TituloPropriedade
        
        SALDO_MINIMO_SEGURANCA = 500
        
        grupos_monopolio = {}
        for prop in self.getPropriedades():
            if isinstance(prop, TituloPropriedade):
                if self.possuiMonopolio(prop.getCor()):
                    cor = prop.getCor()
                    if cor not in grupos_monopolio:
                        grupos_monopolio[cor] = []
                    grupos_monopolio[cor].append(prop)
        
        for cor, propriedades in grupos_monopolio.items():
            if any(p.estaHipotecada() for p in propriedades):
                continue
            
            propriedades.sort(key=lambda p: p.getNumCasas())
            propriedades.sort(key=lambda p: p.getNumCasas())
            
            for prop in propriedades:
                if prop.temHotel():
                    continue
                
                if prop.getNumCasas() >= 4:
                    custo = prop.getCustoCasa()
                    if self.saldo >= custo + SALDO_MINIMO_SEGURANCA:
                        if hasattr(jogo, 'construirHotel'):
                            sucesso = jogo.construirHotel(prop, self)
                            if sucesso:
                                continue
                    continue
                
                custo = prop.getCustoCasa()
                
                if self.saldo >= custo + SALDO_MINIMO_SEGURANCA:
                    min_casas = min(p.getNumCasas() for p in propriedades if not p.temHotel())
                    
                    if prop.getNumCasas() == min_casas:
                        if hasattr(jogo, 'construirCasa'):
                            sucesso = jogo.construirCasa(prop, self)
                            if sucesso:
                                continue
                else:
                    break
