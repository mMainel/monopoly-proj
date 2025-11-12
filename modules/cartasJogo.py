from modules.carta import CartaSorte, CartaCofre, CartaSairCadeia, TipoCarta
from modules.eventoJogo import TipoEvento

def criar_cartas_sorte(jogo) -> list:
    """
    Cria as cartas do baralho Sorte com contexto universitário
    ATUALIZADO: Agora publica eventos quando cartas são executadas

    espera:
        jogo: Jogo - instância do jogo para acesso a componentes
    retorna:
        list - lista de cartas sorte
    """
    cartas = []

    # ===== CARTA ESPECIAL: SAIR DA CADEIA =====
    carta_sair_cadeia = CartaSairCadeia(TipoCarta.SORTE)
    cartas.append(carta_sair_cadeia)

    # ===== CARTA 1: IR PARA INÍCIO =====
    def ir_para_inicio(jogador):
        # Move o jogador até a posição 0.
        # Se passou pelo INÍCIO, reutiliza a rotina do jogo para processar a passagem
        # (paga salário e publica o evento) para manter consistência com o fluxo
        passou = jogador.irPara(0)
        if passou:
            try:
                # Preferimos usar o método do jogo que já publica eventos
                if hasattr(jogo, '_processar_passagem_inicio'):
                    jogo._processar_passagem_inicio(jogador)
                else:
                    # Fallback: pagar diretamente pelo banco e publicar evento manualmente
                    if jogo.banco:
                        jogo.banco.pagarSalario(jogador)
                    if hasattr(jogo, '_publicar_evento'):
                        jogo._publicar_evento(TipoEvento.PASSOU_INICIO, {
                            'jogador': jogador,
                            'valor': jogo._regras.obter_salario_inicio() if hasattr(jogo, '_regras') else 0
                        })
            except Exception:
                # Não quebrar o jogo por erros em publicação de evento
                try:
                    if jogo.banco:
                        jogo.banco.pagarSalario(jogador)
                except Exception:
                    pass

    carta1 = CartaSorte(
        "Seu artigo foi aceito em congresso internacional! Avance até o INÍCIO e receba R$ 200",
        ir_para_inicio
    )
    cartas.append(carta1)

    # ===== CARTAS QUE DÃO DINHEIRO =====
    def receber_150(jogador):
        jogador.receberDinheiro(150)
        # Publicar evento
        if hasattr(jogo, '_publicar_evento'):
            jogo._publicar_evento(TipoEvento.JOGADOR_RECEBEU_DINHEIRO, {
                'jogador': jogador,
                'valor': 150,
                'motivo': 'Carta Sorte'
            })

    carta2 = CartaSorte(
        "Você ganhou o prêmio de melhor TCC do semestre! Receba R$ 150",
        receber_150
    )
    cartas.append(carta2)

    def receber_100(jogador):
        jogador.receberDinheiro(100)
        if hasattr(jogo, '_publicar_evento'):
            jogo._publicar_evento(TipoEvento.JOGADOR_RECEBEU_DINHEIRO, {
                'jogador': jogador,
                'valor': 100,
                'motivo': 'Carta Sorte'
            })

    carta3 = CartaSorte(
        "Sua bolsa de iniciação científica foi aprovada! Receba R$ 100",
        receber_100
    )
    cartas.append(carta3)

    def receber_50(jogador):
        jogador.receberDinheiro(50)
        if hasattr(jogo, '_publicar_evento'):
            jogo._publicar_evento(TipoEvento.JOGADOR_RECEBEU_DINHEIRO, {
                'jogador': jogador,
                'valor': 50,
                'motivo': 'Carta Sorte'
            })

    carta7 = CartaSorte(
        "Você vendeu seus resumos para outros alunos! Receba R$ 50",
        receber_50
    )
    cartas.append(carta7)

    def receber_200(jogador):
        jogador.receberDinheiro(200)
        if hasattr(jogo, '_publicar_evento'):
            jogo._publicar_evento(TipoEvento.JOGADOR_RECEBEU_DINHEIRO, {
                'jogador': jogador,
                'valor': 200,
                'motivo': 'Carta Sorte'
            })

    carta8 = CartaSorte(
        "Bolsa PROUNI aprovada! Receba R$ 200",
        receber_200
    )
    cartas.append(carta8)

    def receber_75(jogador):
        jogador.receberDinheiro(75)
        if hasattr(jogo, '_publicar_evento'):
            jogo._publicar_evento(TipoEvento.JOGADOR_RECEBEU_DINHEIRO, {
                'jogador': jogador,
                'valor': 75,
                'motivo': 'Carta Sorte'
            })

    carta10 = CartaSorte(
        "Você ganhou uma competição de hackathon! Receba R$ 75",
        receber_75
    )
    cartas.append(carta10)

    # ===== CARTAS DE MOVIMENTO =====
    def ir_posicao_21(jogador):
        jogador.irPara(21)

    carta4 = CartaSorte(
        "Você foi convidado para uma palestra na Economia. Avance até lá",
        ir_posicao_21
    )
    cartas.append(carta4)

    def ir_estacao_proxima(jogador):
        posicao = jogador.getPosicao()
        estacoes = [5, 15, 25, 35]
        proxima = min([e for e in estacoes if e > posicao], default=estacoes[0])
        jogador.irPara(proxima)

    carta5 = CartaSorte(
        "Transporte universitário gratuito! Avance até a estação mais próxima",
        ir_estacao_proxima
    )
    cartas.append(carta5)

    def voltar_3_casas(jogador):
        nova_pos = (jogador.getPosicao() - 3) % 40
        jogador.irPara(nova_pos)

    carta6 = CartaSorte(
        "Você esqueceu o material em sala. Volte 3 casas",
        voltar_3_casas
    )
    cartas.append(carta6)

    # ===== CARTA ESPECIAL: RECEBER DE CADA JOGADOR =====
    def receber_de_cada_jogador(jogador):
        total_recebido = 0
        for j in jogo.jogadores:
            if j != jogador and not j.verificarFalencia():
                if jogo.banco:
                    jogo.banco.transferir(j, jogador, 50)
                else:
                    j.pagarAluguel(jogador, 50)
                total_recebido += 50
        
        # Publicar evento com total recebido
        if hasattr(jogo, '_publicar_evento') and total_recebido > 0:
            jogo._publicar_evento(TipoEvento.JOGADOR_RECEBEU_DINHEIRO, {
                'jogador': jogador,
                'valor': total_recebido,
                'motivo': 'Aniversário - Carta Sorte'
            })

    carta9 = CartaSorte(
        "É seu aniversário! Festa no Bandejão. Cada colega te dá R$ 50",
        receber_de_cada_jogador
    )
    cartas.append(carta9)

    return cartas

def criar_cartas_cofre(jogo) -> list:
    """
    Cria as cartas do baralho Cofre (Community Chest) com contexto universitário
    ATUALIZADO: Agora publica eventos quando cartas são executadas

    espera:
        jogo: Jogo - instância do jogo para acesso a componentes
    retorna:
        list - lista de cartas cofre
    """
    cartas = []

    # ===== CARTA ESPECIAL: SAIR DA CADEIA =====
    carta_sair_cadeia = CartaSairCadeia(TipoCarta.COFRE)
    cartas.append(carta_sair_cadeia)

    # ===== CARTA QUE ENVIA PARA CADEIA =====
    def ir_cadeia(jogador):
        jogador.entrarCadeia()

    carta1 = CartaCofre(
        "Você colou na prova e foi pego! Vá direto para a Reitoria (cadeia). Não passe pelo INÍCIO",
        ir_cadeia
    )
    cartas.append(carta1)

    # ===== CARTAS QUE COBRAM DINHEIRO =====
    def pagar_50(jogador):
        valor = 50
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, valor, "Taxa de segunda chamada")
        else:
            jogador.pagarAoBanco(valor)
        
        # Publicar evento
        if hasattr(jogo, '_publicar_evento'):
            jogo._publicar_evento(TipoEvento.JOGADOR_PAGOU_TAXA, {
                'jogador': jogador,
                'valor': valor,
                'motivo': 'Carta Cofre'
            })

    carta2 = CartaCofre(
        "Você perdeu a prova e precisa pagar taxa de segunda chamada. Pague R$ 50",
        pagar_50
    )
    cartas.append(carta2)

    def pagar_100(jogador):
        valor = 100
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, valor, "Multa por atraso de matrícula")
        else:
            jogador.pagarAoBanco(valor)
        
        if hasattr(jogo, '_publicar_evento'):
            jogo._publicar_evento(TipoEvento.JOGADOR_PAGOU_TAXA, {
                'jogador': jogador,
                'valor': valor,
                'motivo': 'Carta Cofre'
            })

    carta3 = CartaCofre(
        "Você atrasou a matrícula. Pague multa de R$ 100",
        pagar_100
    )
    cartas.append(carta3)

    def pagar_150(jogador):
        valor = 150
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, valor, "Reposição de livros da biblioteca")
        else:
            jogador.pagarAoBanco(valor)
        
        if hasattr(jogo, '_publicar_evento'):
            jogo._publicar_evento(TipoEvento.JOGADOR_PAGOU_TAXA, {
                'jogador': jogador,
                'valor': valor,
                'motivo': 'Carta Cofre'
            })

    carta4 = CartaCofre(
        "Você perdeu livros da biblioteca. Pague R$ 150 pela reposição",
        pagar_150
    )
    cartas.append(carta4)

    def pagar_75(jogador):
        valor = 75
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, valor, "Taxa de laboratório de Química")
        else:
            jogador.pagarAoBanco(valor)
        
        if hasattr(jogo, '_publicar_evento'):
            jogo._publicar_evento(TipoEvento.JOGADOR_PAGOU_TAXA, {
                'jogador': jogador,
                'valor': valor,
                'motivo': 'Carta Cofre'
            })

    carta7 = CartaCofre(
        "Você quebrou um béquer no laboratório. Pague R$ 75",
        pagar_75
    )
    cartas.append(carta7)

    def pagar_200(jogador):
        valor = 200
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, valor, "Mensalidade atrasada")
        else:
            jogador.pagarAoBanco(valor)
        
        if hasattr(jogo, '_publicar_evento'):
            jogo._publicar_evento(TipoEvento.JOGADOR_PAGOU_TAXA, {
                'jogador': jogador,
                'valor': valor,
                'motivo': 'Carta Cofre'
            })

    carta9 = CartaCofre(
        "Mensalidade da universidade particular atrasada. Pague R$ 200",
        pagar_200
    )
    cartas.append(carta9)

    def pagar_120(jogador):
        valor = 120
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, valor, "Taxa de formatura")
        else:
            jogador.pagarAoBanco(valor)
        
        if hasattr(jogo, '_publicar_evento'):
            jogo._publicar_evento(TipoEvento.JOGADOR_PAGOU_TAXA, {
                'jogador': jogador,
                'valor': valor,
                'motivo': 'Carta Cofre'
            })

    carta10 = CartaCofre(
        "Taxa antecipada de formatura. Pague R$ 120",
        pagar_120
    )
    cartas.append(carta10)

    # ===== CARTA DE REPAROS (CALCULA BASEADO EM CASAS/HOTÉIS) =====
    def pagar_reparos(jogador):
        total_casas = jogador.getTotalCasas()
        total_hoteis = jogador.getTotalHoteis()
        custo = (total_casas * 25) + (total_hoteis * 100)
        
        if custo > 0:
            if jogo.banco:
                jogo.banco.cobrarTaxa(jogador, custo, "Manutenção de repúblicas")
            else:
                jogador.pagarAoBanco(custo)
            
            # Publicar evento
            if hasattr(jogo, '_publicar_evento'):
                jogo._publicar_evento(TipoEvento.JOGADOR_PAGOU_TAXA, {
                    'jogador': jogador,
                    'valor': custo,
                    'motivo': 'Manutenção - Carta Cofre'
                })

    carta5 = CartaCofre(
        "Manutenção das repúblicas estudantis. Pague R$ 25 por república e R$ 100 por prédio",
        pagar_reparos
    )
    cartas.append(carta5)

    # ===== CARTA ESPECIAL: PAGAR CADA JOGADOR =====
    def pagar_cada_jogador(jogador):
        total_pago = 0
        for j in jogo.jogadores:
            if j != jogador and not j.verificarFalencia():
                if jogo.banco:
                    jogo.banco.transferir(jogador, j, 50)
                else:
                    jogador.pagarAluguel(j, 50)
                total_pago += 50
        
        # Publicar evento com total pago
        if hasattr(jogo, '_publicar_evento') and total_pago > 0:
            jogo._publicar_evento(TipoEvento.JOGADOR_PAGOU_TAXA, {
                'jogador': jogador,
                'valor': total_pago,
                'motivo': 'Diretor do CA - Carta Cofre'
            })

    carta6 = CartaCofre(
        "Você foi eleito diretor do centro acadêmico. Pague R$ 50 para cada colega pela festa",
        pagar_cada_jogador
    )
    cartas.append(carta6)

    # ===== CARTA: IR INÍCIO SEM SALÁRIO =====
    def ir_inicio_sem_salario(jogador):
        jogador.irPara(0)

    carta8 = CartaCofre(
        "Você foi reprovado e precisa refazer o período. Volte ao INÍCIO (sem receber R$ 200)",
        ir_inicio_sem_salario
    )
    cartas.append(carta8)

    return cartas