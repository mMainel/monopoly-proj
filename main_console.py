import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from modules.jogo import Jogo
from modules.observadorConsole import ObservadorConsole
from modules.jogadorIA import JogadorIA

def main() -> None:
    """Ponto de entrada principal do jogo"""
    print("\n" + "=" * 60)
    print("BEM-VINDO AO MONOPOLY UFFIANO")
    print("=" * 60)

    num_jogadores = solicitar_numero_jogadores()
    nomes = solicitar_nomes_jogadores(num_jogadores)
    
    jogo = inicializar_jogo(nomes)
    executar_jogo(jogo)
    finalizar_jogo(jogo)

def solicitar_numero_jogadores() -> int:
    """Solicita e valida numero de jogadores"""
    while True:
        try:
            num = int(input("\nQuantos jogadores? (1-8): "))
            if 1 <= num <= 8:
                return num
            print("Digite um numero entre 1 e 8!")
        except ValueError:
            print("Por favor, digite um numero valido!")

def solicitar_nomes_jogadores(num_jogadores: int) -> list:
    """Solicita nomes dos jogadores"""
    nomes = []
    for i in range(num_jogadores):
        nome = input(f"Nome do jogador {i + 1}: ").strip()
        if not nome:
            nome = f"Jogador {i + 1}"
        nomes.append(nome)
    return nomes

def inicializar_jogo(nomes: list) -> Jogo:
    """Cria e configura uma nova instancia do jogo"""
    jogo = Jogo()
    observador = ObservadorConsole()
    jogo.adicionar_observador(observador)
    jogo.iniciar_jogo(nomes)

    print(f"\nJogo iniciado com sucesso!")
    print(f"Cada jogador comeca com R$ {jogo._regras.obter_saldo_inicial()}")

    if any(isinstance(j, JogadorIA) for j in jogo.jogadores):
        print("IA adicionada automaticamente ao jogo")

    return jogo

def executar_jogo(jogo: Jogo) -> None:
    """Loop principal do jogo"""
    while jogo.esta_ativo():
        jogador_atual = jogo.jogadorAtual

        if jogador_atual.verificarFalencia():
            print(f"\n{jogador_atual.getNome()} esta falido e pula o turno.")
            jogo.proximo_turno()
            continue

        if jogador_atual.estaEmCadeia():
            if not processar_cadeia(jogo, jogador_atual):
                jogo.proximo_turno()
                continue

        try:
            aguardar_jogador(jogador_atual)
            jogo.executar_turno()
            
            processar_pos_turno(jogo, jogador_atual)

            if verificar_fim_jogo(jogo):
                break

        except KeyboardInterrupt:
            print("\n\nJogo interrompido pelo usuario.")
            break
        except Exception as e:
            print(f"\nErro durante execucao do turno: {e}")
            break

def processar_cadeia(jogo: Jogo, jogador) -> bool:
    """Processa turno de jogador na cadeia"""
    if isinstance(jogador, JogadorIA):
        opcao = jogador.escolher_opcao_cadeia()
        print(f"{jogador.getNome()} escolheu: {opcao}")
        return jogo.processarOpcoesCadeia(jogador, opcao)
    
    print(f"\n{jogador.getNome()} esta na cadeia (turno {jogador.getTurnosCadeia()})!")
    print("1 - Tentar tirar dupla")
    print("2 - Pagar fianca (R$ 50)")
    if jogador.podeUsarCartaSairCadeia():
        print("3 - Usar carta 'Sair da Cadeia'")

    escolha = input("Escolha: ").strip()
    
    opcoes = {"1": "dupla", "2": "fianca", "3": "carta"}
    return jogo.processarOpcoesCadeia(jogador, opcoes.get(escolha, "dupla"))

def aguardar_jogador(jogador) -> None:
    """Aguarda jogador humano ou pausa para IA"""
    if isinstance(jogador, JogadorIA):
        print(f"\n{jogador.getNome()} esta jogando")
        time.sleep(1)
    else:
        input(f"\nPressione ENTER para {jogador.getNome()} lancar os dados")

def processar_pos_turno(jogo: Jogo, jogador) -> None:
    """Processa acoes apos o turno"""
    if jogador.verificarFalencia():
        return
    
    processar_compra_ou_leilao(jogo, jogador)
    jogo.processarConstrucoes(jogador)
    
    if not isinstance(jogador, JogadorIA):
        if input("\nGerenciar financas? (s/n): ").strip().lower() == 's':
            jogo.processarGestaoFinanceira(jogador)

def processar_compra_ou_leilao(jogo: Jogo, jogador) -> None:
    """Processa decisao de compra ou inicia leilao"""
    propriedade = jogo.propriedade_disponivel_compra
    if not propriedade:
        return
    
    comprou = decidir_compra(jogo, jogador, propriedade)
    
    if not comprou:
        executar_leilao(jogo, propriedade)
    
    jogo.propriedade_disponivel_compra = None

def decidir_compra(jogo: Jogo, jogador, propriedade) -> bool:
    """Jogador decide se compra a propriedade"""
    if isinstance(jogador, JogadorIA):
        if jogador.decidir_comprar_propriedade(propriedade):
            if jogo.tratarCompraPropriedade(jogador, propriedade):
                print(f"{jogador.getNome()} comprou {propriedade.getNome()}")
                return True
        print(f"{jogador.getNome()} decidiu nao comprar")
        return False
    
    exibir_info_propriedade(jogador, propriedade)
    
    if jogador.getSaldo() < propriedade.getPreco():
        print("Voce nao tem dinheiro suficiente")
        return False
    
    if input("Deseja comprar? (s/n): ").strip().lower() == 's':
        if jogo.tratarCompraPropriedade(jogador, propriedade):
            print(f"Parabens! Voce comprou {propriedade.getNome()}!")
            return True
    
    return False

def exibir_info_propriedade(jogador, propriedade) -> None:
    """Exibe informacoes da propriedade disponivel"""
    print(f"\n{'='*60}")
    print(f"PROPRIEDADE DISPONIVEL!")
    print(f"Nome: {propriedade.getNome()}")
    print(f"Preco: R$ {propriedade.getPreco()}")
    print(f"Seu saldo: R$ {jogador.getSaldo()}")
    print(f"{'='*60}")

def executar_leilao(jogo: Jogo, propriedade) -> None:
    """Executa leilao da propriedade"""
    leilao = jogo.iniciarLeilao(propriedade)
    
    print(f"\n{'='*60}")
    print(f"LEILAO INICIADO - {propriedade.getNome()}")
    print(f"{'='*60}")
    
    participantes = leilao.getParticipantes().copy()
    
    while len(participantes) > 0:
        exibir_status_leilao(leilao)
        
        if not processar_rodada_lances(leilao, participantes):
            break
    
    finalizar_leilao_exibir_resultado(jogo, leilao)

def exibir_status_leilao(leilao) -> None:
    """Exibe status atual do leilao"""
    lance_maior = leilao.getLanceMaior()
    lider = leilao.getLiderAtual()
    
    print(f"\nLance atual: R$ {lance_maior}")
    if lider:
        print(f"Lider: {lider.getNome()}")

def processar_rodada_lances(leilao, participantes: list) -> bool:
    """Processa uma rodada de lances"""
    alguem_deu_lance = False
    
    for jogador in participantes[:]:
        if processar_lance_jogador(leilao, jogador, participantes):
            alguem_deu_lance = True
    
    return alguem_deu_lance

def processar_lance_jogador(leilao, jogador, participantes: list) -> bool:
    """Processa lance de um jogador"""
    if isinstance(jogador, JogadorIA):
        return processar_lance_ia(leilao, jogador, participantes)
    else:
        return processar_lance_humano(leilao, jogador, participantes)

def processar_lance_ia(leilao, jogador, participantes: list) -> bool:
    """IA decide se da lance"""
    lance_maior = leilao.getLanceMaior()
    lance = jogador.decidir_dar_lance(leilao.getPropriedade(), lance_maior)
    
    if lance > lance_maior and leilao.fazerLance(jogador, lance):
        print(f"{jogador.getNome()} deu lance de R$ {lance}")
        return True
    
    leilao.desistir(jogador)
    participantes.remove(jogador)
    print(f"{jogador.getNome()} passou")
    return False

def processar_lance_humano(leilao, jogador, participantes: list) -> bool:
    """Jogador humano decide se da lance"""
    lance_maior = leilao.getLanceMaior()
    
    print(f"\n{jogador.getNome()}, seu saldo: R$ {jogador.getSaldo()}")
    
    if input("Dar lance? (s/n): ").strip().lower() != 's':
        leilao.desistir(jogador)
        participantes.remove(jogador)
        print(f"{jogador.getNome()} desistiu do leilao")
        return False
    
    try:
        valor = int(input(f"Valor (minimo R$ {lance_maior + 1}): "))
        if leilao.fazerLance(jogador, valor):
            print(f"Lance de R$ {valor} aceito!")
            return True
        print("Lance invalido!")
    except ValueError:
        print("Valor invalido!")
    
    return False

def finalizar_leilao_exibir_resultado(jogo: Jogo, leilao) -> None:
    """Finaliza leilao e exibe resultado"""
    vencedor, valor = leilao.finalizarLeilao()
    jogo.notificarLeilaoFinalizado(vencedor, valor)
    
    if vencedor:
        print(f"\n{vencedor.getNome()} venceu o leilao por R$ {valor}!")
    else:
        print(f"\nNenhum lance foi feito")

def verificar_fim_jogo(jogo: Jogo) -> bool:
    """Verifica se o jogo acabou"""
    vencedor = jogo.verificar_vencedor()
    if vencedor:
        print(f"\n{'=' * 60}")
        print(f"PARABENS {vencedor.getNome()}! Voce venceu!")
        print(f"Patrimonio final: R$ {vencedor.calcularPatrimonio()}")
        print(f"{'=' * 60}")
        jogo.finalizar_jogo()
        return True
    return False

def finalizar_jogo(jogo: Jogo) -> None:
    """Exibe status final do jogo"""
    print("\n" + "=" * 60)
    print("JOGO FINALIZADO")
    print("=" * 60)
    print("\n--- Status Final ---")
    
    for jogador in jogo.jogadores:
        tipo = "[IA]" if isinstance(jogador, JogadorIA) else ""
        status = "(FALIDO)" if jogador.verificarFalencia() else ""
        props = f"{len(jogador.getPropriedades())} props"
        
        print(f"{tipo} {jogador.getNome()}: R$ {jogador.getSaldo()} | {props} {status}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAte logo!")
    except Exception as e:
        print(f"\nErro fatal: {e}")