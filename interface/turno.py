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


def executar_turno_com_ui(jogo, jogador, dialogo_compra, evento_ui, dialogo_cadeia=None):
    if jogador.estaEmCadeia():
        if isinstance(jogador, JogadorIA):
            opcao = jogador.escolher_opcao_cadeia()
        else:
            # Jogador humano - mostrar diálogo de opções
            if dialogo_cadeia:
                dialogo_cadeia.mostrar(jogador)
                opcao = None
                
                relogio = pygame.time.Clock()
                while dialogo_cadeia.ativo:
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            return
                        dialogo_cadeia.handle_event(evento)
                    
                    dialogo_cadeia.desenhar()
                    pygame.display.flip()
                    relogio.tick(60)
                
                opcao = dialogo_cadeia.obter_resposta()
            else:
                # Fallback caso o diálogo não seja fornecido
                if jogador.podeUsarCartaSairCadeia():
                    opcao = "carta"
                elif jogador.podePagarFianca():
                    opcao = "fianca"
                else:
                    opcao = "dupla"
        
        saiu = jogo.processarOpcoesCadeia(jogador, opcao)
        
        if not saiu:
            return
    
    try:
        jogo.executar_turno()
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