import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.leilao import leilao

def test_leilao_iniciar_e_determinar_vencedor():
    print("-----")
    print("Testando: iniciar leilão e determinar vencedor")
    print("-----")
    
    class JogadorMock:
        def __init__(self, nome, dinheiro, lances):
            self.nome = nome
            self.dinheiro = dinheiro
            self.lances = lances
            self.lance_index = 0

        def realizarlance(self):
            if self.lance_index < len(self.lances):
                lance = self.lances[self.lance_index]
                self.lance_index += 1
                return lance
            return 0  # Não quer mais dar lances

    jogador1 = JogadorMock("Jogador1", 500, [100, 200, 300])
    jogador2 = JogadorMock("Jogador2", 600, [150, 250, 350])
    jogador3 = JogadorMock("Jogador3", 400, [200, 100, 100])

    leilao_instance = leilao(propriedade=None, participantes=[jogador1, jogador2, jogador3])
    vencedor = leilao_instance.iniciar_leilao()

    assert vencedor is not None, "Deveria haver um vencedor"
    assert vencedor.nome == "Jogador2", f"Esperado Jogador2 como vencedor, mas obteve {vencedor.nome}"
    assert leilao_instance.lance_atual == 350, f"Esperado lance atual de 350, mas obteve {leilao_instance.lance_atual}"


if __name__ == "__main__":
    test_leilao_iniciar_e_determinar_vencedor()