from modules.eventoJogo import TipoEvento
from modules.jogadorIA import JogadorIA
import pygame

def executar_turno(jogo, jogador, interface):
    if jogador.estaEmCadeia():
        if jogador.getTurnosCadeia() > 0:
            if hasattr(jogador, 'isIA') and jogador.isIA():
                opcao = jogador.escolher_opcao_cadeia()
            else:
                opcao = interface.perguntar_opcao_cadeia(jogador) if hasattr(interface, 'perguntar_opcao_cadeia') else "dupla"
            
            saiu = jogo.processarOpcoesCadeia(jogador, opcao)
            if not saiu:
                return

    try:
        jogo.executar_turno()
    except Exception as e:
        print(f"Erro ao executar turno: {e}")
        return

    if jogo.propriedade_disponivel_compra:
        propriedade = jogo.propriedade_disponivel_compra
        
        if hasattr(jogador, 'isIA') and jogador.isIA():
            decisao = jogador.decidir_comprar_propriedade(propriedade)
        else:
            decisao = interface.perguntar_compra(propriedade) if hasattr(interface, 'perguntar_compra') else True
        
        if decisao:
            jogo.tratarCompraPropriedade(jogador, propriedade)
        else:
            leilao = jogo.iniciarLeilao(propriedade)
            if hasattr(interface, 'gerenciar_leilao'):
                interface.gerenciar_leilao(leilao)

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


def executar_turno_com_ui(jogo, jogador, dialogo_compra, elementos_ui):
    tabuleiro = elementos_ui["tabuleiro"]
    jogadores_ui = elementos_ui["jogadores_ui"]
    painel = elementos_ui["painel"]
    evento_ui = elementos_ui["evento_ui"]
    botao_dado = elementos_ui["botao_dado"]
    dado_ui = elementos_ui["dado_ui"]
    
    if jogador.estaEmCadeia():
        if isinstance(jogador, JogadorIA):
            opcao = jogador.escolher_opcao_cadeia()
        else:
            if jogador.podeUsarCartaSairCadeia():
                opcao = "carta"
            elif jogador.podePagarFianca():
                opcao = "fianca"
            else:
                opcao = "dupla"
        
        saiu = jogo.processarOpcoesCadeia(jogador, opcao)
        
        if not saiu:
            jogo.proximo_turno()
            return
    
    try:
        #jogo.executar_turno()
        resultado_dados = jogo.dados.lancar()
        soma = jogo.dados.soma_dados()
        foi_dupla = jogo.dados.isDupla()
        
        jogo._publicar_evento(TipoEvento.DADOS_LANCADOS, {
            'jogador': jogador,
            'dados': resultado_dados,
            'soma': soma
        })
        
        start_time = pygame.time.get_ticks()
        DURACAO_ANIMACAO = 2500
        
        while pygame.time.get_ticks() - start_time < DURACAO_ANIMACAO:
            tabuleiro.desenhar_tabuleiro()
            jogadores_ui.desenhar_jogadores()
            painel.desenhar()
            evento_ui.desenhar()
            botao_dado.desenhar()
            dado_ui.desenhar() 
            
            pygame.display.flip()
            tabuleiro.relogio.tick(60)
            
            for evento_anim in pygame.event.get():
                if evento_anim.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            
        dado_ui.esconder()   
        if foi_dupla:
            jogo._contador_duplas += 1
            jogo._publicar_evento(TipoEvento.DUPLA_LANCADA, {
                'jogador': jogador,
                'contador_duplas': jogo._contador_duplas
            })
            if jogo._contador_duplas >= jogo._regras.obter_max_duplas():
                jogo._enviar_para_prisao(jogador)
                jogo.proximo_turno()
                return 
        
        
        jogo._mover_jogador(jogador, soma)
        
       
        if not foi_dupla:
            jogo._contador_duplas = 0
            jogo.proximo_turno()
        
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
            dialogo_compra.mostrar(propriedade, jogador)
            decisao = None
            
            relogio = pygame.time.Clock()
            while dialogo_compra.ativo:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        return
                    dialogo_compra.handle_event(evento)
                
                dialogo_compra.desenhar()
                pygame.display.flip()
                relogio.tick(60)
            
            decisao = dialogo_compra.obter_resposta()
        
        if decisao:
            jogo.tratarCompraPropriedade(jogador, propriedade)
        else:
            try:
                leilao = jogo.iniciarLeilao(propriedade)
                leilao.finalizarLeilao()
            except Exception as e:
                print(f"Erro ao processar leilão: {e}")
        
        jogo.propriedade_disponivel_compra = None
    
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
        pass


def _obter_propriedades_construiveis(jogador):
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