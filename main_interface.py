import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'interface')))

from modules.jogo import Jogo
from modules.observadorConsole import ObservadorConsole
from modules.jogadorIA import JogadorIA

from interface.main_ui import main_ui


def main() -> None:
    """Ponto de entrada principal do jogo"""
    print("\n" + "=" * 60)
    print("BEM-VINDO AO MONOPOLY UFFIANO")
    print("=" * 60)

    num_jogadores = solicitar_numero_jogadores()
    nomes = solicitar_nomes_jogadores(num_jogadores)
    
    jogo = inicializar_jogo(nomes)

    # aqui chamamos a UI passando a instância do jogo
    main_ui(jogo)

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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAte logo!")
    except Exception as e:
        print(f"\nErro fatal: {e}")
