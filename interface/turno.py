from modules.eventoJogo import TipoEvento
from modules.jogadorIA import JogadorIA
import pygame
from interface.negociacao_ui import DialogoConfirmacaoUI
from modules.espaco import EspacoPropriedade

def executar_turno(jogo, jogador, interface):
    """
    Versão simplificada para CLI ou interface básica.
    Segue exatamente o fluxo recomendado em integracao.md
    """
    if jogador.estaEmCadeia():
        if jogador.getTurnosCadeia() > 0:
            # IA escolhe automaticamente, humano via interface
            if hasattr(jogador, 'isIA') and jogador.isIA():
                opcao = jogador.escolher_opcao_cadeia()
            else:
                opcao = interface.perguntar_opcao_cadeia(jogador) if hasattr(interface, 'perguntar_opcao_cadeia') else "dupla"
            
            saiu = jogo.processarOpcoesCadeia(jogador, opcao)
            if not saiu:
                # Não saiu da cadeia, turno termina
                return

    try:
        jogo.executar_turno()
    except Exception as e:
        print(f"Erro ao executar turno: {e}")
        return

    if jogo.propriedade_disponivel_compra:
        propriedade = jogo.propriedade_disponivel_compra
        
        # IA decide automaticamente, humano via interface
        if hasattr(jogador, 'isIA') and jogador.isIA():
            decisao = jogador.decidir_comprar_propriedade(propriedade)
        else:
            decisao = interface.perguntar_compra(propriedade) if hasattr(interface, 'perguntar_compra') else True
        
        if decisao:
            jogo.tratarCompraPropriedade(jogador, propriedade)
        else:
            # Iniciar leilão
            leilao = jogo.iniciarLeilao(propriedade)
            if hasattr(interface, 'gerenciar_leilao'):
                interface.gerenciar_leilao(leilao)
            else:
                # Finalizar leilão automaticamente se não houver interface
                leilao.finalizarLeilao()
        
        jogo.propriedade_disponivel_compra = None

    propriedades_construiveis = _obter_propriedades_construiveis(jogador)
    if propriedades_construiveis:
        if hasattr(jogador, 'isIA') and jogador.isIA():
            propriedade = jogador.escolher_propriedade_construir(propriedades_construiveis)
        else:
            propriedade = interface.escolher_propriedade_construir(propriedades_construiveis) if hasattr(interface, 'escolher_propriedade_construir') else None
        
        if propriedade:
            jogo.construirCasa(propriedade, jogador)

    if jogador.verificarFalencia():
        if hasattr(jogo, 'tratarFalencia'):
            jogo.tratarFalencia(jogador)


def executar_turno_com_ui(jogo, jogador, dialogo_compra, elementos_ui, dialogo_cadeia=None):
    """
    Versão com interface gráfica Pygame.
    CORRIGIDA: Usa jogo.executar_turno() em vez de reimplementar a lógica.
    """
    tabuleiro = elementos_ui["tabuleiro"]
    jogadores_ui = elementos_ui["jogadores_ui"]
    painel = elementos_ui["painel"]
    evento_ui = elementos_ui["evento_ui"]
    botao_dado = elementos_ui["botao_dado"]
    dado_ui = elementos_ui["dado_ui"]
    dialogo_escolher = elementos_ui.get("dialogo_escolher")
    dialogo_negociacao = elementos_ui.get("dialogo_negociacao")
    dialogo_leilao = elementos_ui.get("dialogo_leilao")
    dialogo_menu = elementos_ui.get("dialogo_menu")
    dialogo_gerenciar = elementos_ui.get("dialogo_gerenciar")
    popup_eventos = elementos_ui.get("popup_eventos")
    
    if jogador.estaEmCadeia():
        if isinstance(jogador, JogadorIA):
            opcao = jogador.escolher_opcao_cadeia()
        else:
            # Jogador humano - mostrar diálogo
            if dialogo_cadeia:
                opcao = _mostrar_dialogo_cadeia(dialogo_cadeia, jogador)
            else:
                # Fallback
                opcao = _escolher_opcao_cadeia_fallback(jogador)
        
        saiu = jogo.processarOpcoesCadeia(jogador, opcao)
        
        if not saiu:
            jogo.proximo_turno()
            return
    
    try:
        jogo.executar_turno()
        foi_dupla = jogo.dados.isDupla()
        _animar_dados(dado_ui, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, popup_eventos)
    except Exception as e:
        print(f"Erro ao executar turno do jogo: {e}")
        import traceback
        traceback.print_exc()
        return
    
    if jogo.propriedade_disponivel_compra:
        propriedade = jogo.propriedade_disponivel_compra

        if isinstance(jogador, JogadorIA):
            decisao = jogador.decidir_comprar_propriedade(propriedade)
        else:
            decisao = _mostrar_dialogo_compra(dialogo_compra, propriedade, jogador,
                                              tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui)

        if decisao:
            jogo.tratarCompraPropriedade(jogador, propriedade)
        else:
            # Iniciar fluxo de leilão começando do próximo jogador
            try:
                if dialogo_leilao:
                    _executar_leilao_ui(jogo, jogador, propriedade, dialogo_leilao,
                                         tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui, popup_eventos)
                else:
                    # Fallback automático (sem UI): finalizar imediatamente sem lances
                    leilao = jogo.iniciarLeilao(propriedade)
                    vencedor, valor = leilao.finalizarLeilao()
                    jogo.notificarLeilaoFinalizado(vencedor, valor)
            except Exception as e:
                print(f"Erro ao processar leilão: {e}")

        jogo.propriedade_disponivel_compra = None

    try:
        espaco = jogo.tabuleiro.getEspaco(jogador.getPosicao()) if hasattr(jogo, 'tabuleiro') else None
        if isinstance(espaco, EspacoPropriedade):
            titulo = espaco.getTitulo()
            if hasattr(titulo, 'estaHipotecada') and titulo.estaHipotecada() \
               and hasattr(titulo, 'getProprietario') and titulo.getProprietario() == jogador:
                custo = int(getattr(titulo, 'getPreco', lambda: 0)() * 0.55)
                # Só oferece se tiver chance de pagar ou para informar
                confirmar = DialogoConfirmacaoUI(tabuleiro.tela)
                confirmar.mostrar("Deshipotecar propriedade?", f"Pagar R$ {custo} para deshipotecar {titulo.getNome()}?")
                _loop_modal(confirmar, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui)
                if confirmar.obter_resposta():
                    try:
                        jogo.deshipotecarPropriedade(titulo, jogador)
                    except Exception as e:
                        print(f"Falha ao deshipotecar: {e}")
    except Exception as e:
        print(f"Erro ao oferecer deshipoteca: {e}")
    
    try:
        propriedades_construiveis = _obter_propriedades_construiveis(jogador)
        
        if propriedades_construiveis:
            if isinstance(jogador, JogadorIA):
                propriedade_escolhida = jogador.escolher_propriedade_construir(propriedades_construiveis)
                if propriedade_escolhida:
                    jogo.construirCasa(propriedade_escolhida, jogador)
            else:
                pass
    except Exception as e:
        print(f"Erro ao processar construção: {e}")
    
    if jogador.verificarFalencia():
        if hasattr(jogo, 'tratarFalencia'):
            jogo.tratarFalencia(jogador)
    
    try:
        if dialogo_menu:
            # Garantia: evitar que outros diálogos fiquem ativos ao mesmo tempo
            for d in (dialogo_escolher, dialogo_negociacao, dialogo_leilao, dialogo_gerenciar):
                try:
                    if d is not None:
                        d.ativo = False
                except Exception:
                    pass
            # Exibe menu com opções
            dialogo_menu.mostrar()
            _loop_modal(dialogo_menu, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui, popup_eventos)
            escolha = dialogo_menu.obter_opcao()
            if escolha == 'negociar' and dialogo_escolher and dialogo_negociacao:
                _fluxo_negociacao(jogo, jogador, dialogo_escolher, dialogo_negociacao, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui)
            elif escolha == 'gerenciar' and dialogo_gerenciar:
                # Garantir que o menu anterior não permaneça ativo
                try:
                    dialogo_menu.ativo = False
                except Exception:
                    pass
                dialogo_gerenciar.mostrar(jogo, jogador)
                _loop_modal(dialogo_gerenciar, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui, popup_eventos)
            # 'passar' não faz nada extra (turno já avançado pelo jogo)
    except Exception as e:
        print(f"Erro no menu de fim de turno: {e}")



def _mostrar_dialogo_cadeia(dialogo_cadeia, jogador):
    """Mostra diálogo de opções da cadeia e retorna a escolha"""
    dialogo_cadeia.mostrar(jogador)
    
    relogio = pygame.time.Clock()
    while dialogo_cadeia.ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "dupla"
            dialogo_cadeia.handle_event(evento)
        
        dialogo_cadeia.desenhar()
        pygame.display.flip()
        relogio.tick(60)
    
    return dialogo_cadeia.obter_resposta()


def _escolher_opcao_cadeia_fallback(jogador):
    """Fallback para escolher opção da cadeia sem diálogo"""
    if jogador.podeUsarCartaSairCadeia():
        return "carta"
    elif jogador.podePagarFianca():
        return "fianca"
    else:
        return "dupla"


def _mostrar_dialogo_compra(dialogo_compra, propriedade, jogador,
                            tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui):
    """Mostra diálogo de compra (modal) e retorna a decisão"""
    dialogo_compra.mostrar(propriedade, jogador)
    _loop_modal(dialogo_compra, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui)
    return dialogo_compra.obter_resposta()


def _animar_dados(dado_ui, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, popup_eventos=None):
    """
    Animação dos dados melhorada.
    Mantém a tela responsiva durante a animação.
    """
    start_time = pygame.time.get_ticks()
    DURACAO_ANIMACAO = 2500
    
    while pygame.time.get_ticks() - start_time < DURACAO_ANIMACAO:
        tabuleiro.desenhar_tabuleiro()
        jogadores_ui.desenhar_jogadores()
        painel.desenhar()
        evento_ui.desenhar()
        botao_dado.desenhar()
        dado_ui.desenhar()
        if popup_eventos:
            popup_eventos.desenhar()
        
        pygame.display.flip()
        tabuleiro.relogio.tick(60)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
    
    dado_ui.esconder()


def _desenhar_frame(tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui, popup_eventos=None, dialogo=None):
    tabuleiro.desenhar_tabuleiro()
    jogadores_ui.desenhar_jogadores()
    painel.desenhar()
    evento_ui.desenhar()
    botao_dado.desenhar()
    dado_ui.desenhar()
    if dialogo:
        dialogo.desenhar()
    if popup_eventos:
        popup_eventos.desenhar()

def _executar_leilao_ui(jogo, jogador_inicial, propriedade, dialogo_leilao,
                        tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui, popup_eventos=None):
    """Executa o fluxo de leilão via diálogo Pygame começando do próximo jogador."""
    # Criar leilão no jogo
    leilao = jogo.iniciarLeilao(propriedade)
    jogadores = jogo.jogadores
    indice_inicial = (jogadores.index(jogador_inicial) + 1) % len(jogadores)

    dialogo_leilao.iniciar(leilao, jogadores, indice_inicial)

    relogio = pygame.time.Clock()
    inicio_finalizado = None

    while dialogo_leilao.ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            dialogo_leilao.handle_event(evento)
        _desenhar_frame(tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui, popup_eventos, dialogo_leilao)
        pygame.display.flip()
        relogio.tick(60)

        # Se finalizado, aguarda breve intervalo para visualização e encerra
        if dialogo_leilao.finalizado:
            if inicio_finalizado is None:
                inicio_finalizado = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - inicio_finalizado > 1800:
                dialogo_leilao.ativo = False

    # Publicar resultado
    resultado = dialogo_leilao.obter_resultado()
    if resultado:
        vencedor, valor = resultado
        jogo.notificarLeilaoFinalizado(vencedor, valor)
    else:
        # Nenhum lance realizado
        jogo.notificarLeilaoFinalizado(None, 0)
    pygame.display.flip()
    tabuleiro.relogio.tick(60)


def _loop_modal(dialogo, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui, popup_eventos=None):
    relogio = pygame.time.Clock()
    while getattr(dialogo, 'ativo', False):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            dialogo.handle_event(evento)
        _desenhar_frame(tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui, popup_eventos, dialogo)
        pygame.display.flip()
        relogio.tick(60)


def _esperar_confirmacao(dialogo_confirmar, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui, titulo, mensagem):
    dialogo_confirmar.mostrar(titulo, mensagem)
    _loop_modal(dialogo_confirmar, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui)
    return dialogo_confirmar.obter_resposta()


def _fluxo_negociacao(jogo, jogador_atual, dialogo_escolher, dialogo_negociacao, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui):
    confirmar = DialogoConfirmacaoUI(tabuleiro.tela)
    confirmar.mostrar("Negociação", "Deseja negociar com alguém?")
    _loop_modal(confirmar, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui)
    if not confirmar.obter_resposta():
        return

    dialogo_escolher.mostrar(jogo.jogadores, jogador_atual)
    _loop_modal(dialogo_escolher, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui)
    alvo = dialogo_escolher.obter_jogador()
    if not alvo:
        return

    dialogo_negociacao.mostrar(jogador_atual, alvo)
    _loop_modal(dialogo_negociacao, tabuleiro, jogadores_ui, painel, evento_ui, botao_dado, dado_ui)
    resultado = dialogo_negociacao.obter_resultado()

    din_a = resultado['dinheiro_a']
    din_b = resultado['dinheiro_b']
    if din_a > jogador_atual.getSaldo() or din_b > alvo.getSaldo():
        try:
            evento_ui.adicionar_evento("Negociação falhou: saldo insuficiente")
        except:
            pass
        return

    if din_a > 0:
        jogo.banco.transferir(jogador_atual, alvo, din_a)
    if din_b > 0:
        jogo.banco.transferir(alvo, jogador_atual, din_b)

    for p in resultado['props_a']:
        if hasattr(p, 'transferirPropriedade'):
            p.transferirPropriedade(alvo)
    for p in resultado['props_b']:
        if hasattr(p, 'transferirPropriedade'):
            p.transferirPropriedade(jogador_atual)

    try:
        evento_ui.adicionar_evento("Negociação concluída entre jogadores")
    except:
        pass


def _obter_propriedades_construiveis(jogador):
    """
    Retorna lista de propriedades onde o jogador pode construir.
    Mantida do código original - está correta.
    """
    from modules.tituloPropriedade import TituloPropriedade
    
    propriedades_construiveis = []
    
    for prop in jogador.getPropriedades():
        if not isinstance(prop, TituloPropriedade):
            continue
        
        try:
            if not jogador.possuiMonopolio(prop.getCor()):
                continue
        except:
            continue
        
        if hasattr(prop, 'tem_hotel') and prop.tem_hotel:
            continue
        
        try:
            num_casas = prop.getNumCasas() if hasattr(prop, 'getNumCasas') else 0
            if num_casas >= 4:
                continue
        except:
            continue
        
        try:
            custo_casa = prop.getCustoCasa() if hasattr(prop, 'getCustoCasa') else 0
            if jogador.getSaldo() < custo_casa:
                continue
        except:
            continue
        
        propriedades_construiveis.append(prop)
    
    return propriedades_construiveis