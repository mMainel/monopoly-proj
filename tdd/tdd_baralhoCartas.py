import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.baralhoCartas import BaralhoCartas
from modules.carta import Carta, CartaSorte, CartaReves, TipoCarta

class MockCartaSorte(Carta):
    def __init__(self, descricao: str):
        super().__init__(descricao)
    def executar(self, jogador) -> None:
        pass

class MockCartaReves(Carta):
    def __init__(self, descricao: str):
        super().__init__(descricao)
    def executar(self, jogador) -> None:
        pass

def test_baralho_inicializacao():
    """Testa a inicialização de um baralho vazio"""
    print("-----")
    print("Testando: Baralho - Inicialização")
    print("-----")
    
    baralho_sorte = BaralhoCartas(TipoCarta.SORTE)
    
    assert baralho_sorte.getTipo() == TipoCarta.SORTE
    assert baralho_sorte.getTamanho() == 0
    assert baralho_sorte.estaVazio() == True
    print("Baralho de Sorte inicializado vazio")
    
    baralho_reves = BaralhoCartas(TipoCarta.REVES)
    assert baralho_reves.getTipo() == TipoCarta.REVES
    print("Baralho de Revés inicializado")

def test_baralho_adicionar_carta():
    """Testa a adição de cartas ao baralho"""
    print("-----")
    print("Testando: Baralho - Adicionar Carta")
    print("-----")

    baralho = BaralhoCartas(TipoCarta.SORTE)
    
    carta1 = MockCartaSorte("Carta 1")
    baralho.adicionarCarta(carta1)
    
    assert baralho.getTamanho() == 1
    assert baralho.estaVazio() == False
    print("Carta adicionada corretamente")

    # Teste para não adicionar None
    baralho.adicionarCarta(None)
    assert baralho.getTamanho() == 1
    print("Não adicionou carta 'None' (correto)")


def test_baralho_sacar_e_retornar():
    """Testa sacar e retornar cartas do baralho (Lógica FIFO)"""
    print("-----")
    print("Testando: Baralho - Sacar e Retornar Cartas (FIFO)")
    print("-----")
    
    baralho = BaralhoCartas(TipoCarta.REVES)
    
    carta_a = MockCartaReves("Carta A")
    carta_b = MockCartaReves("Carta B")
    
    baralho.adicionarCarta(carta_a)
    baralho.adicionarCarta(carta_b)
    assert baralho.getTamanho() == 2
    
    # Teste de sacar (ordem FIFO - Primeiro que entra, Primeiro que sai)
    carta_sacada1 = baralho.sacarCarta()
    assert carta_sacada1 == carta_a
    assert baralho.getTamanho() == 1
    print("Sacar (FIFO) funcionando")
    
    carta_sacada2 = baralho.sacarCarta()
    assert carta_sacada2 == carta_b
    assert baralho.getTamanho() == 0
    assert baralho.estaVazio() == True
    print("Baralho esvaziado")
    
    # Teste sacar de baralho vazio
    carta_vazia = baralho.sacarCarta()
    assert carta_vazia is None
    print("Sacar de baralho vazio retorna None")
    
    # Teste de retornar (coloca no fim)
    baralho.retornarCarta(carta_sacada1)
    assert baralho.getTamanho() == 1
    
    baralho.retornarCarta(carta_sacada2)
    assert baralho.getTamanho() == 2
    
    # Verifica se a ordem de retorno está correta (FIFO)
    assert baralho.sacarCarta() == carta_a # Carta A
    assert baralho.sacarCarta() == carta_b # Carta B
    print("Retornar e re-sacar na ordem correta")

    # Teste para não retornar None
    baralho.retornarCarta(None)
    assert baralho.getTamanho() == 0
    print("Não retornou carta 'None' (correto)")

def test_baralho_embaralhar():
    """Testa o embaralhamento do baralho"""
    print("-----")
    print("Testando: Baralho - Embaralhar")
    print("-----")
    
    baralho = BaralhoCartas(TipoCarta.SORTE)
    
    cartas_ordenadas = []
    for i in range(20):
        carta = MockCartaSorte(f"Carta {i}")
        baralho.adicionarCarta(carta)
        cartas_ordenadas.append(carta)
    
    # Guardamos a referência da função original
    original_shuffle = random.shuffle
    
    def mock_shuffle(lista):
        lista.reverse()
    
    random.shuffle = mock_shuffle
    
    baralho.embaralhar()
    
    # Restauramos a função original
    random.shuffle = original_shuffle
    
    assert baralho.getTamanho() == 20
    
    # Sacar todas de novo
    ordem_depois = []
    for _ in range(20):
        ordem_depois.append(baralho.sacarCarta())
    
    # Verifica se a ordem é a inversa da original (nosso mock)
    cartas_invertidas = list(reversed(cartas_ordenadas))
    
    assert ordem_depois == cartas_invertidas
    assert ordem_depois != cartas_ordenadas
    
    print("Baralho embaralhado (com mock) com sucesso")

# --- Executando os testes ---
if __name__ == "__main__":
    test_baralho_inicializacao()
    test_baralho_adicionar_carta()
    test_baralho_sacar_e_retornar()
    test_baralho_embaralhar()

    print("\nTodos os testes de BaralhoCartas passaram!")