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
from modules.regras import Regras
from modules.tituloPropriedade import TituloPropriedade

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
        
    def iniciar_jogo(self, jogadores_config: List[tuple] = None) -> None:
        """
        Inicializa o jogo com jogadores reais e IA
        Recebe uma lista de tuplas (nome, peca)

        espera:
            jogadores_config: List[Tuple[str, Peca]] - (nome, peca) dos jogadores
        retorna:
            None
        """
        if jogadores_config is None:
            # Fallback se o jogo for iniciado sem config
            pecas_disponiveis = list(Peca)
            jogadores_config = [("Jogador 1", pecas_disponiveis[0])]

        if len(jogadores_config) < 1:
            raise ValueError("O jogo precisa de pelo menos 1 jogador")

        # Se apenas 1 jogador, adiciona IA
        if len(jogadores_config) == 1:
            peca_usada = jogadores_config[0][1]
            # Pega a primeira peça que não foi usada
            peca_ia = Peca.BIOLOGIA if peca_usada != Peca.BIOLOGIA else Peca.ARTES
            jogadores_config.append(("IA", peca_ia))

        if len(jogadores_config) > 8:
            raise ValueError("O jogo suporta no máximo 8 jogadores")

        
        self.jogadores = []

        for nome, peca in jogadores_config:
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

        jogador = self.jogadorAtual

        self._publicar_evento(TipoEvento.TURNO_INICIADO, {
            'turno': self.turno,
            'jogador': jogador
        })

        resultado_dados = self.dados.lancar()
        soma = self.dados.soma_dados()

        self._publicar_evento(TipoEvento.DADOS_LANCADOS, {
            'jogador': jogador,
            'dados': resultado_dados,
            'soma': soma
        })

        foi_dupla = self.dados.isDupla()

        if foi_dupla:
            self._contador_duplas += 1
            self._publicar_evento(TipoEvento.DUPLA_LANCADA, {
                'jogador': jogador,
                'contador_duplas': self._contador_duplas
            })

            if self._contador_duplas >= self._regras.obter_max_duplas():
                self._enviar_para_prisao(jogador)
                self.proximo_turno()
                return

        self._mover_jogador(jogador, soma)

        if not foi_dupla:
            self._contador_duplas = 0
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
        Envia jogador para a prisão por tirar 3 duplas consecutivas

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

        espera:
            jogador: Jogador - jogador que deseja comprar
            propriedade: Propriedade - propriedade a ser comprada
        retorna:
            bool - True se comprou com sucesso, False caso contrário
        """
        if not self._regras.validar_compra(jogador, propriedade):
            return False

        sucesso = self.banco.venderPropriedade(propriedade, jogador)

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

        if propriedade.estaHipotecada():
            return

        aluguel = self._regras.calcular_aluguel(propriedade, self.dados)
        sucesso = self.banco.transferir(jogador, propriedade.proprietario, aluguel)

        self._publicar_evento(TipoEvento.ALUGUEL_PAGO, {
            'pagador': jogador,
            'recebedor': propriedade.proprietario,
            'propriedade': propriedade,
            'valor': aluguel
        })

        if not sucesso:
            credor = propriedade.proprietario
            jogador.declararFalencia(credor)
            self._publicar_evento(TipoEvento.JOGADOR_FALIU, {
                'jogador': jogador,
                'credor': credor,
                'motivo': 'sem_dinheiro_aluguel'
            })
    
    def tratarCadeia(self, jogador) -> None:
        """
        Envia o jogador para a cadeia

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
                fianca = self._regras.obter_valor_prisao()

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
        Cria e inicia um leilão para propriedade

        espera:
            propriedade: Titulo - propriedade a ser leiloada
        retorna:
            Leilao - instância do leilão criado
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
        Retorna o leilão ativo atual

        espera:
            nenhum parâmetro
        retorna:
            Leilao - leilão ativo ou None
        """
        return self.leilao_ativo

    def notificarLeilaoFinalizado(self, vencedor, valor):
        """
        Publica evento quando leilão é finalizado

        espera:
            vencedor: Jogador - vencedor do leilão ou None
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

    def construirCasa(self, propriedade, jogador) -> bool:
        """
        Constrói uma casa na propriedade via Banco

        espera:
            propriedade: TituloPropriedade - onde construir
            jogador: Jogador - proprietário
        retorna:
            bool - True se construiu, False caso contrário
        """
        sucesso = self.banco.comprarCasa(propriedade, jogador)

        if sucesso:
            self._publicar_evento(TipoEvento.CONSTRUCAO_FEITA, {
                'jogador': jogador,
                'propriedade': propriedade,
                'tipo': 'casa'
            })

        return sucesso

    def construirHotel(self, propriedade, jogador) -> bool:
        """
        Constrói um hotel na propriedade via Banco

        espera:
            propriedade: TituloPropriedade - onde construir
            jogador: Jogador - proprietário
        retorna:
            bool - True se construiu, False caso contrário
        """
        sucesso = self.banco.comprarHotel(propriedade, jogador)

        if sucesso:
            self._publicar_evento(TipoEvento.CONSTRUCAO_FEITA, {
                'jogador': jogador,
                'propriedade': propriedade,
                'tipo': 'hotel'
            })

        return sucesso

    def venderCasa(self, propriedade, jogador) -> bool:
        """
        Vende uma casa da propriedade via Banco

        espera:
            propriedade: TituloPropriedade - propriedade com casa
            jogador: Jogador - vendedor
        retorna:
            bool - True se vendeu, False caso contrário
        """
        sucesso = self.banco.venderCasa(propriedade, jogador)

        if sucesso:
            self._publicar_evento(TipoEvento.CONSTRUCAO_VENDIDA, {
                'jogador': jogador,
                'propriedade': propriedade,
                'tipo': 'casa'
            })

        return sucesso

    def venderHotel(self, propriedade, jogador) -> bool:
        """
        Vende um hotel da propriedade via Banco

        espera:
            propriedade: TituloPropriedade - propriedade com hotel
            jogador: Jogador - vendedor
        retorna:
            bool - True se vendeu, False caso contrário
        """
        sucesso = self.banco.venderHotel(propriedade, jogador)

        if sucesso:
            self._publicar_evento(TipoEvento.CONSTRUCAO_VENDIDA, {
                'jogador': jogador,
                'propriedade': propriedade,
                'tipo': 'hotel'
            })

        return sucesso

    # GESTAO FINANCEIRA

    def hipotecarPropriedade(self, propriedade, jogador) -> int:
        """
        Hipoteca uma propriedade via Banco

        espera:
            propriedade: Titulo - propriedade a hipotecar
            jogador: Jogador - proprietário
        retorna:
            int - valor recebido pela hipoteca
        """
        valor = self.banco.hipotecarPropriedade(propriedade, jogador)

        if valor > 0:
            self._publicar_evento(TipoEvento.PROPRIEDADE_HIPOTECADA, {
                'jogador': jogador,
                'propriedade': propriedade,
                'valor': valor
            })

        return valor

    def deshipotecarPropriedade(self, propriedade, jogador) -> bool:
        """
        Remove a hipoteca de uma propriedade

        espera:
            propriedade: Titulo - propriedade a deshipotecar
            jogador: Jogador - proprietário
        retorna:
            bool - True se deshipotecou, False caso contrário
        """
        if not propriedade.estaHipotecada() or propriedade.getProprietario() != jogador:
            return False

        custo = int(propriedade.getPreco() * 0.55)

        if jogador.getSaldo() < custo:
            return False

        sucesso = propriedade.deshipotecar()

        if sucesso:
            self._publicar_evento(TipoEvento.PROPRIEDADE_DESHIPOTECADA, {
                'jogador': jogador,
                'propriedade': propriedade,
                'valor': custo
            })

        return sucesso
