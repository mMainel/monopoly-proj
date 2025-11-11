from typing import List
import sys
import os
import json
from datetime import datetime

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
from modules.carta import CartaSairCadeia

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

    # SALVAMENTO E CARREGAMENTO DO JOGO

    def salvar_estado_jogo(self, caminho_arquivo: str = None) -> bool:
        """
        Serializa e salva todo o estado atual do jogo em um arquivo JSON

        espera:
            caminho_arquivo: str - caminho completo do arquivo (padrão: save_game.json na raiz do projeto)
        retorna:
            bool - True se salvou com sucesso, False caso contrário
        """
        if caminho_arquivo is None:
            diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            caminho_arquivo = os.path.join(diretorio_raiz, 'save_game.json')

        try:
            indice_jogador_atual = self.jogadores.index(self.jogadorAtual) if self.jogadorAtual else 0

            jogadores_serializados = []
            for jogador in self.jogadores:
                jogador_dict = jogador.to_dict()

                propriedades_indices = []
                for prop in jogador.getPropriedades():
                    posicao = self.tabuleiro.obter_posicao_propriedade(prop)
                    if posicao != -1:
                        propriedades_indices.append(posicao)

                jogador_dict['propriedades_indices'] = propriedades_indices
                jogadores_serializados.append(jogador_dict)

            estado = {
                'meta': {
                    'data_salvamento': datetime.now().isoformat(),
                    'versao': '1.0'
                },
                'jogo': {
                    'turno': self.turno,
                    'contador_duplas': self._contador_duplas,
                    'jogo_ativo': self._jogo_ativo,
                    'indice_jogador_atual': indice_jogador_atual,
                    'tem_propriedade_disponivel': self.propriedade_disponivel_compra is not None,
                    'propriedade_disponivel_posicao': self.tabuleiro.obter_posicao_propriedade(self.propriedade_disponivel_compra) if self.propriedade_disponivel_compra else None
                },
                'jogadores': jogadores_serializados,
                'tabuleiro': self.tabuleiro.to_dict(self.jogadores),
                'banco': self.banco.to_dict(),
                'dados': self.dados.to_dict(),
                'leilao': self.leilao_ativo.to_dict(self.jogadores) if self.leilao_ativo and self.leilao_ativo.estaAtivo() else None
            }

            with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                json.dump(estado, arquivo, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"Erro ao salvar jogo: {e}")
            return False

    def carregar_estado_jogo(self, caminho_arquivo: str = None) -> bool:
        """
        Carrega e restaura o estado do jogo de um arquivo JSON

        espera:
            caminho_arquivo: str - caminho do arquivo de save (padrão: save_game.json na raiz)
        retorna:
            bool - True se carregou com sucesso, False caso contrário
        """
        estado = Jogo.verificar_jogo_salvo(caminho_arquivo)

        if estado is None:
            return False

        try:
            self._restaurar_jogadores(estado['jogadores'])

            self._restaurar_propriedades(estado['tabuleiro']['propriedades'])

            self._restaurar_banco(estado['banco'])

            self._restaurar_dados(estado['dados'])

            self._restaurar_baralhos(estado['tabuleiro'])

            self._restaurar_estado_jogo(estado['jogo'])

            if estado.get('leilao'):
                self._restaurar_leilao(estado['leilao'])

            return True

        except Exception as e:
            print(f"Erro ao carregar estado do jogo: {e}")
            return False

    def _restaurar_jogadores(self, jogadores_data: list) -> None:
        """Restaura os jogadores a partir dos dados salvos"""
        self.jogadores = []

        for jogador_dict in jogadores_data:
            peca = Peca(jogador_dict['peca'])

            if jogador_dict.get('eh_ia', False):
                jogador = JogadorIA(jogador_dict['nome'], peca)
            else:
                jogador = Jogador(jogador_dict['nome'], peca)

            jogador.saldo = jogador_dict['saldo']
            jogador.posicao = jogador_dict['posicao']
            jogador.emCadeia = jogador_dict['emCadeia']
            jogador.turnosCadeia = jogador_dict['turnosCadeia']
            jogador.cartasSairCadeia = jogador_dict['cartasSairCadeia']
            jogador.estaFalido = jogador_dict['estaFalido']

            self.jogadores.append(jogador)

    def _restaurar_propriedades(self, propriedades_data: list) -> None:
        """Restaura o estado das propriedades e atribui proprietários"""
        for prop_dict in propriedades_data:
            posicao = prop_dict['posicao']
            espaco = self.tabuleiro.getEspaco(posicao)

            if hasattr(espaco, 'titulo') and espaco.titulo is not None:
                titulo = espaco.titulo

                proprietario_index = prop_dict.get('proprietario_index', -1)
                if proprietario_index >= 0 and proprietario_index < len(self.jogadores):
                    proprietario = self.jogadores[proprietario_index]
                    titulo.proprietario = proprietario
                    proprietario.adicionarPropriedade(titulo)

                titulo.hipotecada = prop_dict.get('hipotecada', False)

                if isinstance(titulo, TituloPropriedade):
                    titulo.num_casas = prop_dict.get('num_casas', 0)
                    titulo.tem_hotel = prop_dict.get('tem_hotel', False)

    def _restaurar_banco(self, banco_data: dict) -> None:
        """Restaura o estado do banco"""
        self.banco.casas_disponiveis = banco_data['casas_disponiveis']
        self.banco.hoteis_disponiveis = banco_data['hoteis_disponiveis']

    def _restaurar_dados(self, dados_data: dict) -> None:
        """Restaura o estado dos dados"""
        lancamento = dados_data.get('ultimo_lancamento')
        if lancamento:
            self.dados.ultimo_lancamento = tuple(lancamento)
        else:
            self.dados.ultimo_lancamento = None

    def _restaurar_baralhos(self, tabuleiro_data: dict) -> None:
        """
        Restaura o estado dos baralhos mantendo a ordem das cartas
        (optamos por não aumentar a complexidade nesse ponto pois é irrelevante)
        """
        pass

    def _restaurar_estado_jogo(self, jogo_data: dict) -> None:
        """Restaura o estado geral do jogo"""
        self.turno = jogo_data['turno']
        self._contador_duplas = jogo_data['contador_duplas']
        self._jogo_ativo = jogo_data['jogo_ativo']

        indice_jogador_atual = jogo_data['indice_jogador_atual']
        if indice_jogador_atual >= 0 and indice_jogador_atual < len(self.jogadores):
            self.jogadorAtual = self.jogadores[indice_jogador_atual]

        if jogo_data.get('tem_propriedade_disponivel', False):
            posicao = jogo_data.get('propriedade_disponivel_posicao')
            if posicao is not None and posicao >= 0:
                espaco = self.tabuleiro.getEspaco(posicao)
                if hasattr(espaco, 'titulo'):
                    self.propriedade_disponivel_compra = espaco.titulo

    def _restaurar_leilao(self, leilao_data: dict) -> None:
        """Restaura o estado do leilão ativo"""
        if not leilao_data or not leilao_data.get('ativo', False):
            self.leilao_ativo = None
            return

        self.leilao_ativo = Leilao()
        self.leilao_ativo.ativo = True
        self.leilao_ativo.lance_minimo = leilao_data.get('lance_minimo', 1)

        participantes = []
        for indice in leilao_data.get('participantes_indices', []):
            if indice >= 0 and indice < len(self.jogadores):
                participantes.append(self.jogadores[indice])

        self.leilao_ativo.participantes = participantes

        lances = {}
        for indice_str, valor in leilao_data.get('lances', {}).items():
            indice = int(indice_str)
            if indice >= 0 and indice < len(self.jogadores):
                lances[self.jogadores[indice]] = valor

        self.leilao_ativo.lances = lances

    @staticmethod
    def verificar_jogo_salvo(caminho_arquivo: str = None) -> dict:
        """
        Verifica se existe um jogo salvo e retorna o estado

        espera:
            caminho_arquivo: str - caminho do arquivo de save (padrão: save_game.json na raiz)
        retorna:
            dict - estado do jogo salvo ou None se não houver save
        """
        if caminho_arquivo is None:
            diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            caminho_arquivo = os.path.join(diretorio_raiz, 'save_game.json')

        if not os.path.exists(caminho_arquivo):
            return None

        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                estado = json.load(arquivo)
                return estado
        except Exception as e:
            print(f"Erro ao carregar jogo salvo: {e}")
            return None
