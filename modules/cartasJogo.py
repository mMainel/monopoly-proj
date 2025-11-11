from modules.carta import CartaSorte, CartaCofre, CartaSairCadeia, TipoCarta

def criar_cartas_sorte(jogo) -> list:
    """
    Cria as cartas do baralho Sorte com contexto universitário

    espera:
        jogo: Jogo - instância do jogo para acesso a componentes
    retorna:
        list - lista de cartas sorte
    """
    cartas = []

    carta_sair_cadeia = CartaSairCadeia(TipoCarta.SORTE)
    cartas.append(carta_sair_cadeia)

    def ir_para_inicio(jogador):
        passou = jogador.irPara(0)
        if passou and jogo.banco:
            jogo.banco.pagarSalario(jogador)

    carta1 = CartaSorte(
        "Seu artigo foi aceito em congresso internacional! Avance até o INÍCIO e receba R$ 200",
        ir_para_inicio
    )
    cartas.append(carta1)

    def receber_150(jogador):
        jogador.receberDinheiro(150)

    carta2 = CartaSorte(
        "Você ganhou o prêmio de melhor TCC do semestre! Receba R$ 150",
        receber_150
    )
    cartas.append(carta2)

    def receber_100(jogador):
        jogador.receberDinheiro(100)

    carta3 = CartaSorte(
        "Sua bolsa de iniciação científica foi aprovada! Receba R$ 100",
        receber_100
    )
    cartas.append(carta3)

    def ir_posicao_24(jogador):
        jogador.irPara(24)

    carta4 = CartaSorte(
        "Você foi convidado para uma palestra na Economia. Avance até lá",
        ir_posicao_24
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

    def receber_50(jogador):
        jogador.receberDinheiro(50)

    carta7 = CartaSorte(
        "Você vendeu seus resumos para outros alunos! Receba R$ 50",
        receber_50
    )
    cartas.append(carta7)

    def receber_200(jogador):
        jogador.receberDinheiro(200)

    carta8 = CartaSorte(
        "Bolsa PROUNI aprovada! Receba R$ 200",
        receber_200
    )
    cartas.append(carta8)

    def receber_de_cada_jogador(jogador):
        for j in jogo.jogadores:
            if j != jogador and not j.verificarFalencia():
                if jogo.banco:
                    jogo.banco.transferir(j, jogador, 50)
                else:
                    j.pagarAluguel(jogador, 50)

    carta9 = CartaSorte(
        "É seu aniversário! Festa no Bandeijão. Cada colega te dá R$ 50",
        receber_de_cada_jogador
    )
    cartas.append(carta9)

    def receber_75(jogador):
        jogador.receberDinheiro(75)

    carta10 = CartaSorte(
        "Você ganhou uma competição de hackathon! Receba R$ 75",
        receber_75
    )
    cartas.append(carta10)

    return cartas

def criar_cartas_cofre(jogo) -> list:
    """
    Cria as cartas do baralho Cofre (Community Chest) com contexto universitário

    espera:
        jogo: Jogo - instância do jogo para acesso a componentes
    retorna:
        list - lista de cartas cofre
    """
    cartas = []

    carta_sair_cadeia = CartaSairCadeia(TipoCarta.COFRE)
    cartas.append(carta_sair_cadeia)

    def ir_cadeia(jogador):
        jogador.entrarCadeia()

    carta1 = CartaCofre(
        "Você colou na prova e foi pego! Vá direto para a Reitoria (cadeia). Não passe pelo INÍCIO",
        ir_cadeia
    )
    cartas.append(carta1)

    def pagar_50(jogador):
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, 50, "Taxa de segunda chamada")
        else:
            jogador.pagarAoBanco(50)

    carta2 = CartaCofre(
        "Você perdeu a prova e precisa pagar taxa de segunda chamada. Pague R$ 50",
        pagar_50
    )
    cartas.append(carta2)

    def pagar_100(jogador):
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, 100, "Multa por atraso de matrícula")
        else:
            jogador.pagarAoBanco(100)

    carta3 = CartaCofre(
        "Você atrasou a matrícula. Pague multa de R$ 100",
        pagar_100
    )
    cartas.append(carta3)

    def pagar_150(jogador):
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, 150, "Reposição de livros da biblioteca")
        else:
            jogador.pagarAoBanco(150)

    carta4 = CartaCofre(
        "Você perdeu livros da biblioteca. Pague R$ 150 pela reposição",
        pagar_150
    )
    cartas.append(carta4)

    def pagar_reparos(jogador):
        total_casas = jogador.getTotalCasas()
        total_hoteis = jogador.getTotalHoteis()
        custo = (total_casas * 25) + (total_hoteis * 100)
        if custo > 0:
            if jogo.banco:
                jogo.banco.cobrarTaxa(jogador, custo, "Manutenção de repúblicas")
            else:
                jogador.pagarAoBanco(custo)

    carta5 = CartaCofre(
        "Manutenção das repúblicas estudantis. Pague R$ 25 por república e R$ 100 por prédio",
        pagar_reparos
    )
    cartas.append(carta5)

    def pagar_cada_jogador(jogador):
        for j in jogo.jogadores:
            if j != jogador and not j.verificarFalencia():
                if jogo.banco:
                    jogo.banco.transferir(jogador, j, 50)
                else:
                    jogador.pagarAluguel(j, 50)

    carta6 = CartaCofre(
        "Você foi eleito diretor do centro acadêmico. Pague R$ 50 para cada colega pela festa",
        pagar_cada_jogador
    )
    cartas.append(carta6)

    def pagar_75(jogador):
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, 75, "Taxa de laboratório de Química")
        else:
            jogador.pagarAoBanco(75)

    carta7 = CartaCofre(
        "Você quebrou um béquer no laboratório. Pague R$ 75",
        pagar_75
    )
    cartas.append(carta7)

    def ir_inicio_sem_salario(jogador):
        jogador.irPara(0)

    carta8 = CartaCofre(
        "Você foi reprovado e precisa refazer o período. Volte ao INÍCIO (sem receber R$ 200)",
        ir_inicio_sem_salario
    )
    cartas.append(carta8)

    def pagar_200(jogador):
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, 200, "Mensalidade atrasada")
        else:
            jogador.pagarAoBanco(200)

    carta9 = CartaCofre(
        "Mensalidade da universidade particular atrasada. Pague R$ 200",
        pagar_200
    )
    cartas.append(carta9)

    def pagar_120(jogador):
        if jogo.banco:
            jogo.banco.cobrarTaxa(jogador, 120, "Taxa de formatura")
        else:
            jogador.pagarAoBanco(120)

    carta10 = CartaCofre(
        "Taxa antecipada de formatura. Pague R$ 120",
        pagar_120
    )
    cartas.append(carta10)

    return cartas