from typing import List
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.dados import Dados
from modules.regras import Regras
from modules.eventoJogo import EventoJogo, TipoEvento
from modules.observador import Observador
from modules.jogador import Jogador
from modules.jogadorIA import JogadorIA
from modules.banco import Banco
from modules.tabuleiro import Tabuleiro
from modules.peca import Peca
from modules.leilao import Leilao

class Jogo:
    """
    Classe principal que orquestra o fluxo do jogo Monopoly
    Gerencia turnos, movimentação, eventos e integração entre componentes
    """

    def __init__(self):
        self.tabuleiro: Tabuleiro = Tabuleiro()
        self.jogadores: List[Jogador] = []
        self.jogadorAtual: Jogador = None
        self.banco: Banco = Banco()
        self.dados: Dados = Dados()
        self.turno: int = 0
        self.propriedade_disponivel_compra = None
        self.leilao_ativo: Leilao = None

        self._observadores: List[Observador] = []
        self._regras: Regras = Regras()
        self._contador_duplas: int = 0
        self._jogo_ativo: bool = False

    def adicionar_observador(self, observador: Observador) -> None:
        """
        Adiciona um observador para receber eventos do jogo

        espera:
            observador: Observador - observador a ser registrado
        retorna:
            None
        """
        self._observadores.append(observador)

    def remover_observador(self, observador: Observador) -> None:
        """
        Remove um observador da lista de notificações

        espera:
            observador: Observador - observador a ser removido
        retorna:
            None
        """
        if observador in self._observadores:
            self._observadores.remove(observador)

    def _publicar_evento(self, tipo: TipoEvento, dados: dict) -> None:
        """
        Publica um evento para todos os observadores

        espera:
            tipo: TipoEvento - tipo do evento ocorrido
            dados: dict - dados do evento
        retorna:
            None
        """
        evento = EventoJogo(tipo=tipo, dados=dados)
        for observador in self._observadores:
            observador.notificar(evento)

    def iniciar_jogo(self, nomes_jogadores: List[str] = None) -> None:
        """
        Inicializa o jogo com jogadores reais e IA
        Se apenas 1 nome for fornecido, adiciona uma IA automaticamente

        espera:
            nomes_jogadores: List[str] - nomes dos jogadores (mínimo 1, máximo 8)
        retorna:
            None
        """
        if nomes_jogadores is None:
            nomes_jogadores = ["Jogador 1"]

        if len(nomes_jogadores) < 1:
            raise ValueError("O jogo precisa de pelo menos 1 jogador")

        if len(nomes_jogadores) == 1:
            nomes_jogadores.append("IA")

        if len(nomes_jogadores) > 8:
            raise ValueError("O jogo suporta no máximo 8 jogadores")

        pecas_disponiveis = list(Peca)
        self.jogadores = []

        for i, nome in enumerate(nomes_jogadores):
            peca = pecas_disponiveis[i % len(pecas_disponiveis)]

            if nome == "IA":
                jogador = JogadorIA(nome, peca)
            else:
                jogador = Jogador(nome, peca)

            self.jogadores.append(jogador)

        self.jogadorAtual = self.jogadores[0]
        self.turno = 1
        self._jogo_ativo = True

        self.tabuleiro.inicializar_cartas_completas(self)

        self._publicar_evento(TipoEvento.TURNO_INICIADO, {
            'turno': self.turno,
            'jogador': self.jogadorAtual
        })
    
    def executar_turno(self) -> None:
        """
        Executa um turno completo do jogador atual

        espera:
            nenhum parâmetro
        retorna:
            None
        """
        if not self._jogo_ativo:
            raise RuntimeError("O jogo não foi iniciado")
        
        self._publicar_evento(TipoEvento.TURNO_INICIADO, {
            'turno': self.turno,
            'jogador': self.jogadorAtual
        })
        
        resultado_dados = self.dados.lancar()
        soma = self.dados.soma_dados()
        
        self._publicar_evento(TipoEvento.DADOS_LANCADOS, {
            'jogador': self.jogadorAtual,
            'dados': resultado_dados,
            'soma': soma
        })
        
        if self.dados.isDupla():
            self._contador_duplas += 1
            self._publicar_evento(TipoEvento.DUPLA_LANCADA, {
                'jogador': self.jogadorAtual,
                'contador_duplas': self._contador_duplas
            })
            
            if self._contador_duplas >= self._regras.obter_max_duplas():
                self._enviar_para_prisao(self.jogadorAtual)
                self.proximo_turno()
                return
        else:
            self._contador_duplas = 0
        
        self._mover_jogador(self.jogadorAtual, soma)
        
        if not self.dados.isDupla():
            self.proximo_turno()
    
    def proximo_turno(self) -> None:
        """
        Avança para o próximo jogador

        espera:
            nenhum parâmetro
        retorna:
            None
        """
        self._publicar_evento(TipoEvento.TURNO_FINALIZADO, {
            'turno': self.turno,
            'jogador': self.jogadorAtual
        })
        
        self._contador_duplas = 0
        
        indice_atual = self.jogadores.index(self.jogadorAtual)
        proximo_indice = (indice_atual + 1) % len(self.jogadores)
        self.jogadorAtual = self.jogadores[proximo_indice]
        
        if proximo_indice == 0:
            self.turno += 1
    
    def _mover_jogador(self, jogador: Jogador, casas: int) -> None:
        """
        Move o jogador no tabuleiro e processa a casa de destino

        espera:
            jogador: Jogador - jogador a ser movido
            casas: int - número de casas a mover
        retorna:
            None
        """
        posicao_anterior = jogador.posicao
        passou_inicio = jogador.mover(casas)

        if passou_inicio:
            self._processar_passagem_inicio(jogador)

        self._publicar_evento(TipoEvento.JOGADOR_MOVEU, {
            'jogador': jogador,
            'posicao_anterior': posicao_anterior,
            'posicao_nova': jogador.posicao,
            'casas': casas
        })

        self.tabuleiro.executarAcaoEspaco(jogador.posicao, jogador, self)
    
    def _processar_passagem_inicio(self, jogador: Jogador) -> None:
        """
        Processa quando jogador passa pelo Início

        espera:
            jogador: Jogador - jogador que passou pelo Início
        retorna:
            None
        """
        self.banco.pagarSalario(jogador)

        self._publicar_evento(TipoEvento.PASSOU_INICIO, {
            'jogador': jogador,
            'valor': self._regras.obter_salario_inicio()
        })

    def _enviar_para_prisao(self, jogador: Jogador) -> None:
        """
        Envia jogador para a prisão

        espera:
            jogador: Jogador - jogador a ser preso
        retorna:
            None
        """
        jogador.entrarCadeia()

        self._publicar_evento(TipoEvento.JOGADOR_PRESO, {
            'jogador': jogador,
            'motivo': 'tres_duplas'
        })

    def verificar_vencedor(self) -> Jogador:
        """
        Verifica se há um vencedor

        espera:
            nenhum parâmetro
        retorna:
            Jogador - vencedor ou None se jogo ainda está em andamento
        """
        jogadores_ativos = [j for j in self.jogadores if not j.verificarFalencia()]

        if len(jogadores_ativos) == 1:
            return jogadores_ativos[0]

        return None

    def finalizar_jogo(self) -> None:
        """
        Finaliza o jogo

        espera:
            nenhum parâmetro
        retorna:
            None
        """
        vencedor = self.verificar_vencedor()
        self._jogo_ativo = False

        self._publicar_evento(TipoEvento.JOGADOR_FALIU, {
            'vencedor': vencedor,
            'turno_final': self.turno
        })

    def esta_ativo(self) -> bool:
        """
        Verifica se o jogo está ativo

        espera:
            nenhum parâmetro
        retorna:
            bool - True se ativo, False se finalizado
        """
        return self._jogo_ativo
    
    # INTEGRAÇÃO COM JOGADOR E PROPRIEDADES
    
    def tratarCompraPropriedade(self, jogador, propriedade) -> bool:
        """
        Orquestra a compra de uma propriedade pelo jogador
        Valida com Regras, executa transação via Banco e publica eventos
        
        espera:
            jogador: Jogador - jogador que deseja comprar
            propriedade: Propriedade - propriedade a ser comprada
        retorna:
            bool - True se comprou com sucesso, False caso contrário
        """
        if not self._regras.validar_compra(jogador, propriedade):
            return False
        
        if self.banco and hasattr(self.banco, 'venderPropriedade'):
            sucesso = self.banco.venderPropriedade(propriedade, jogador)
        else:
            if jogador.pagarAoBanco(propriedade.getPreco()):
                jogador.adicionarPropriedade(propriedade)
                propriedade.proprietario = jogador
                sucesso = True
            else:
                sucesso = False

        if sucesso:
            self._publicar_evento(TipoEvento.PROPRIEDADE_COMPRADA, {
                'jogador': jogador,
                'propriedade': propriedade,
                'valor': propriedade.getPreco()
            })

        return sucesso
    
    def tratarPagamentoAluguel(self, jogador, propriedade) -> None:
        """
        Processa o pagamento de aluguel quando jogador cai em propriedade de outro
        
        espera:
            jogador: Jogador - jogador que deve pagar
            propriedade: Propriedade - propriedade onde caiu
        retorna:
            None
        """
        if not hasattr(propriedade, 'proprietario') or propriedade.proprietario is None:
            return
        
        if propriedade.proprietario == jogador:
            return
        
        aluguel = self._regras.calcular_aluguel(propriedade)
        
        if self.banco and hasattr(self.banco, 'transferir'):
            sucesso = self.banco.transferir(jogador, propriedade.proprietario, aluguel)
        else:
            sucesso = jogador.pagarAluguel(propriedade.proprietario, aluguel)
        
        self._publicar_evento(TipoEvento.ALUGUEL_PAGO, {
            'pagador': jogador,
            'recebedor': propriedade.proprietario,
            'propriedade': propriedade,
            'valor': aluguel
        })
        
        if not sucesso:
            jogador.declararFalencia()
            self._publicar_evento(TipoEvento.JOGADOR_FALIU, {
                'jogador': jogador,
                'motivo': 'sem_dinheiro_aluguel'
            })
    
    def tratarCadeia(self, jogador) -> None:
        """
        Envia o jogador para a cadeia e atualiza seu estado
        
        espera:
            jogador: Jogador - jogador a ser preso
        retorna:
            None
        """
        jogador.entrarCadeia()
        
        self._publicar_evento(TipoEvento.JOGADOR_PRESO, {
            'jogador': jogador,
            'motivo': 'va_para_cadeia'
        })
    
    def processarOpcoesCadeia(self, jogador, opcao: str) -> bool:
        """
        Processa a escolha do jogador para sair da cadeia
        
        espera:
            jogador: Jogador - jogador preso
            opcao: str - "carta", "fianca" ou "dupla"
        retorna:
            bool - True se conseguiu sair da cadeia, False caso contrário
        """
        if not jogador.estaEmCadeia():
            return False
        
        if opcao == "carta":
            if jogador.podeUsarCartaSairCadeia():
                if jogador.usarCartaSairCadeia():
                    jogador.sairCadeia()
                    self._publicar_evento(TipoEvento.SAIU_CADEIA, {
                        'jogador': jogador,
                        'metodo': 'carta'
                    })
                    return True
        
        elif opcao == "fianca":
            if jogador.podePagarFianca():
                from modules.regras import Regras
                regras = Regras()
                fianca = regras.obter_valor_prisao()
                
                if jogador.pagarAoBanco(fianca):
                    jogador.sairCadeia()
                    self._publicar_evento(TipoEvento.SAIU_CADEIA, {
                        'jogador': jogador,
                        'metodo': 'fianca',
                        'valor': fianca
                    })
                    return True
        
        elif opcao == "dupla":
            resultado_dados = self.dados.lancar()
            foi_dupla = self.dados.isDupla()
            soma = self.dados.soma_dados()

            self._publicar_evento(TipoEvento.DADOS_LANCADOS, {
                'jogador': jogador,
                'dados': resultado_dados,
                'soma': soma,
                'na_cadeia': True
            })
            
            if jogador.tentarSairCadeiaDupla(foi_dupla):
                self._publicar_evento(TipoEvento.SAIU_CADEIA, {
                    'jogador': jogador,
                    'metodo': 'dupla' if foi_dupla else 'tres_turnos'
                })
                return True
            else:
                jogador.incrementarTurnoCadeia()

        return False

    def solicitarDecisaoCompra(self, jogador, propriedade, callback_decisao) -> None:
        """
        Solicita decisão de compra de propriedade ao jogador

        espera:
            jogador: Jogador - jogador que pode comprar
            propriedade: Titulo - propriedade disponível
            callback_decisao: callable - função que retorna True/False para comprar
        retorna:
            None
        """
        decisao = callback_decisao(jogador, propriedade)
        if decisao:
            self.tratarCompraPropriedade(jogador, propriedade)

    def solicitarDecisaoConstrucao(self, jogador, callback_decisao) -> None:
        """
        Solicita decisão de construção ao jogador

        espera:
            jogador: Jogador - jogador que pode construir
            callback_decisao: callable - função que processa construção
        retorna:
            None
        """
        from modules.tituloPropriedade import TituloPropriedade

        propriedades_construiveis = []
        for prop in jogador.getPropriedades():
            if isinstance(prop, TituloPropriedade):
                if jogador.possuiMonopolio(prop.cor):
                    if hasattr(prop, 'num_casas') and prop.num_casas < 4:
                        if jogador.getSaldo() >= prop.getCustoCasa():
                            propriedades_construiveis.append(prop)

        if propriedades_construiveis:
            prop_escolhida = callback_decisao(jogador, propriedades_construiveis)
            if prop_escolhida and self.banco.comprarCasa(prop_escolhida, jogador):
                self._publicar_evento(TipoEvento.CONSTRUCAO_FEITA, {
                    'jogador': jogador,
                    'propriedade': prop_escolhida,
                    'tipo': 'casa'
                })    
    # INTEGRACAO COM LEILAO
    
    def iniciarLeilao(self, propriedade):
        """
        Cria e inicia um leilao para propriedade
        
        espera:
            propriedade: Titulo - propriedade a ser leiloada
        retorna:
            Leilao - instancia do leilao criado
        """
        jogadores_ativos = [j for j in self.jogadores if not j.verificarFalencia()]
        
        self.leilao_ativo = Leilao()
        self.leilao_ativo.iniciarLeilao(propriedade, jogadores_ativos)
        
        self._publicar_evento(TipoEvento.LEILAO_INICIADO, {
            'propriedade': propriedade,
            'participantes': jogadores_ativos
        })
        
        return self.leilao_ativo
    
    def getLeilaoAtivo(self):
        """
        Retorna o leilao ativo atual
        
        espera:
            nenhum parametro
        retorna:
            Leilao - leilao ativo ou None
        """
        return self.leilao_ativo
    
    def notificarLeilaoFinalizado(self, vencedor, valor):
        """
        Publica evento quando leilao e finalizado
        
        espera:
            vencedor: Jogador - vencedor do leilao ou None
            valor: int - valor final ou 0
        retorna:
            None
        """
        if vencedor and valor > 0:
            self._publicar_evento(TipoEvento.LEILAO_FINALIZADO, {
                'vencedor': vencedor,
                'valor': valor,
                'propriedade': self.leilao_ativo.getPropriedade() if self.leilao_ativo else None
            })
        else:
            self._publicar_evento(TipoEvento.LEILAO_SEM_VENCEDOR, {
                'propriedade': self.leilao_ativo.getPropriedade() if self.leilao_ativo else None
            })
        
        self.leilao_ativo = None
    
    # GESTAO DE CONSTRUCOES
    
    def processarConstrucoes(self, jogador) -> None:
        """
        Permite ao jogador construir casas e hoteis
        Delega para Banco a venda de casas/hoteis
        
        espera:
            jogador: Jogador - jogador que deseja construir
        retorna:
            None
        """
        from modules.tituloPropriedade import TituloPropriedade
        from modules.jogadorIA import JogadorIA
        
        propriedades_monopolio = [p for p in jogador.getPropriedades() 
                                  if isinstance(p, TituloPropriedade) and jogador.possuiMonopolio(p.cor)]
        
        if not propriedades_monopolio:
            return
        
        if isinstance(jogador, JogadorIA):
            construiveis = [p for p in propriedades_monopolio 
                           if p.num_casas < 4 and not p.tem_hotel and jogador.getSaldo() >= p.getCustoCasa()]
            
            if construiveis:
                prop = jogador.escolher_propriedade_construir(construiveis)
                if prop and jogador.decidir_construir_casa(prop):
                    if self.banco.comprarCasa(prop, jogador):
                        self._publicar_evento(TipoEvento.CONSTRUCAO_FEITA, {
                            'jogador': jogador,
                            'propriedade': prop,
                            'tipo': 'casa'
                        })
    
    def processarGestaoFinanceira(self, jogador) -> None:
        """
        Interface para jogador gerenciar hipotecas e vendas
        Apenas orquestra - delegando para Banco e Titulo
        
        espera:
            jogador: Jogador - jogador que deseja gerenciar
        retorna:
            None
        """
        pass
