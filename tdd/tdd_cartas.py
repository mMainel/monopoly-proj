import sys
import os

# Adiciona o diretório raiz ao sys.path para permitir importações de 'modules'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importações dos módulos que vamos testar
from modules.carta import TipoCarta, CartaSorte, CartaReves, CartaSairCadeia
from modules.baralhoCartas import BaralhoCartas
from modules.cartasJogo import criar_cartas_sorte, criar_cartas_reves

# Importações de dependências necessárias para os testes
from modules.jogador import Jogador
from modules.peca import Peca

def test_carta_criacao_e_execucao():
    """Testa a criação de cartas e a execução de callbacks"""
    print("-----")
    print("Testando: Criação de Cartas e Execução de Callback")
    print("-----")

    # Usamos uma flag em uma lista para simular a execução (mutável)
    flag_execucao = [False]
    
    # Criamos um jogador real para o teste, como feito em tdd_leilao.py
    jogador_teste = Jogador("Jogador Teste", Peca.CACHORRO)
    saldo_inicial = jogador_teste.getSaldo()

    # Ação de teste simples
    def acao_teste(jogador):
        flag_execucao[0] = True
        jogador.receberDinheiro(50) # Testa interação com o jogador

    # Teste CartaSorte
    carta_sorte = CartaSorte("Receba R$ 50", acao_teste)
    assert carta_sorte.getDescricao() == "Receba R$ 50"
    
    carta_sorte.executar(jogador_teste)
    
    assert flag_execucao[0] == True
    assert jogador_teste.getSaldo() == saldo_inicial + 50
    print("CartaSorte executou callback corretamente")

    # Teste CartaReves (mesma lógica de callback)
    flag_execucao[0] = False # Reset
    jogador_teste.saldo = saldo_inicial # Reset saldo
    
    carta_reves = CartaReves("Ação de Revés", acao_teste)
    
    carta_reves.executar(jogador_teste)
    
    assert flag_execucao[0] == True
    assert jogador_teste.getSaldo() == saldo_inicial + 50
    print("CartaReves executou callback corretamente")

def test_carta_sair_cadeia():
    """Testa a carta especial 'Sair da Cadeia'"""
    print("-----")
    print("Testando: Carta Sair da Cadeia")
    print("-----")
    
    jogador_teste = Jogador("Preso", Peca.CANHAO)
    assert jogador_teste.cartasSairCadeia == 0
    
    carta_sair = CartaSairCadeia(TipoCarta.SORTE)
    assert "saiu da cadeia" in carta_sair.getDescricao().lower()
    
    # Executa a ação da carta no jogador
    carta_sair.executar(jogador_teste)
    
    assert jogador_teste.cartasSairCadeia == 1
    print("CartaSairCadeia foi adicionada ao jogador")

def test_baralho_inicializacao_e_adicao():
    """Testa a inicialização e adição de cartas ao baralho"""
    print("-----")
    print("Testando: Baralho - Inicialização e Adição")
    print("-----")
    
    baralho = BaralhoCartas(TipoCarta.SORTE)
    
    assert baralho.getTipo() == TipoCarta.SORTE
    assert baralho.getTamanho() == 0
    assert baralho.estaVazio() == True
    print("Baralho inicializado vazio")

    carta1 = CartaSorte("Carta 1", None)
    baralho.adicionarCarta(carta1)
    
    assert baralho.getTamanho() == 1
    assert baralho.estaVazio() == False
    print("Carta adicionada corretamente")

def test_baralho_sacar_e_retornar():
    """Testa sacar e retornar cartas do baralho"""
    print("-----")
    print("Testando: Baralho - Sacar e Retornar Cartas")
    print("-----")
    
    baralho = BaralhoCartas(TipoCarta.REVES)
    
    carta1 = CartaReves("Carta A", None)
    carta2 = CartaReves("Carta B", None)
    
    baralho.adicionarCarta(carta1)
    baralho.adicionarCarta(carta2)
    assert baralho.getTamanho() == 2
    
    # Teste de sacar (ordem FIFO - Primeiro que entra, Primeiro que sai)
    carta_sacada1 = baralho.sacarCarta()
    assert carta_sacada1 == carta1
    assert baralho.getTamanho() == 1
    print("Sacar (FIFO) funcionando")
    
    carta_sacada2 = baralho.sacarCarta()
    assert carta_sacada2 == carta2
    assert baralho.getTamanho() == 0
    assert baralho.estaVazio() == True
    print("Baralho esvaziado")
    
    # Teste sacar de baralho vazio
    carta_vazia = baralho.sacarCarta()
    assert carta_vazia is None
    print("Sacar de baralho vazio retorna None")
    
    # Teste de retornar (coloca no fim)
    baralho.retornarCarta(carta_sacada1) # Devolve Carta A
    assert baralho.getTamanho() == 1
    
    baralho.retornarCarta(carta_sacada2) # Devolve Carta B
    assert baralho.getTamanho() == 2
    
    # Verifica se a ordem de retorno está correta (FIFO)
    assert baralho.sacarCarta() == carta1 # Carta A
    assert baralho.sacarCarta() == carta2 # Carta B
    print("Retornar e re-sacar na ordem correta")

def test_baralho_embaralhar():
    """Testa o embaralhamento do baralho"""
    print("-----")
    print("Testando: Baralho - Embaralhar")
    print("-----")
    
    baralho = BaralhoCartas(TipoCarta.SORTE)
    
    cartas_ordenadas = []
    # Adiciona 20 cartas para garantir que o embaralhamento seja perceptível
    for i in range(20):
        carta = CartaSorte(f"Carta {i}", None)
        baralho.adicionarCarta(carta)
        cartas_ordenadas.append(carta)
    
    tamanho_antes = baralho.getTamanho()
    assert tamanho_antes == 20
    
    # Sacar todas para verificar a ordem
    ordem_antes = []
    for _ in range(tamanho_antes):
        ordem_antes.append(baralho.sacarCarta())
    
    # Verifica se saíram na ordem que entraram
    assert ordem_antes == cartas_ordenadas
    
    # Retornar todas e embaralhar
    for carta in ordem_antes:
        baralho.retornarCarta(carta)
        
    baralho.embaralhar()
    
    tamanho_depois = baralho.getTamanho()
    assert tamanho_depois == tamanho_antes
    
    # Sacar todas de novo
    ordem_depois = []
    for _ in range(tamanho_depois):
        ordem_depois.append(baralho.sacarCarta())
    
    # A chance de ser igual é astronomicamente pequena
    assert ordem_depois != ordem_antes 
    
    # Verifica se todas as cartas ainda estão presentes, apenas em ordem diferente
    assert sorted(ordem_depois, key=lambda c: c.getDescricao()) == sorted(ordem_antes, key=lambda c: c.getDescricao())
    print("Baralho embaralhado com sucesso")

def test_criar_cartas_jogo():
    """Testa as funções factory de criar cartas (cartasJogo.py)"""
    print("-----")
    print("Testando: Factory - criar_cartas_sorte e criar_cartas_reves")
    print("-----")
    
    # Criar um mock simples para o Jogo e Banco
    # As cartas em cartasJogo.py precisam de um 'jogo' com um 'banco'
    mock_banco = type('Banco', (), {
        'cobrarTaxa': lambda self, j, v, d: j.pagarAoBanco(v),
        'pagarSalario': lambda self, j: j.receberDinheiro(200)
    })()
    
    mock_jogo = type('Jogo', (), {
        'banco': mock_banco,
        'jogadores': [] # Ações de pagar a todos não farão nada
    })()
    
    # Teste criar_cartas_sorte
    cartas_sorte = criar_cartas_sorte(mock_jogo)
    assert isinstance(cartas_sorte, list)
    assert len(cartas_sorte) > 0
    assert any(isinstance(c, CartaSorte) for c in cartas_sorte)
    assert any(isinstance(c, CartaSairCadeia) for c in cartas_sorte)
    print("criar_cartas_sorte retornou lista válida")
    
    # Teste criar_cartas_reves
    cartas_reves = criar_cartas_reves(mock_jogo)
    assert isinstance(cartas_reves, list)
    assert len(cartas_reves) > 0
    assert any(isinstance(c, CartaReves) for c in cartas_reves)
    assert any(isinstance(c, CartaSairCadeia) for c in cartas_reves)
    print("criar_cartas_reves retornou lista válida")


# --- Executando os testes ---
if __name__ == "__main__":
    test_carta_criacao_e_execucao()
    test_carta_sair_cadeia()
    test_baralho_inicializacao_e_adicao()
    test_baralho_sacar_e_retornar()
    test_baralho_embaralhar()
    test_criar_cartas_jogo()

    print("\nTodos os testes de cartas passaram!")