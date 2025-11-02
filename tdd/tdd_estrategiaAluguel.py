import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.estrategiaAluguel import estrategiaAluguel

def test_estrategia_aluguel_calculo():
    print("-----")
    print("Testando: cálculo de aluguel com diferentes estratégias")
    print("-----")
    # Teste com casas
    aluguel_casas = estrategiaAluguel.calcula(100, {'casa': 3})
    assert aluguel_casas == 1400, f"Esperado 1400, obtido {aluguel_casas}"
    # Teste com hotel
    aluguel_hotel = estrategiaAluguel.calcula(100, {'hotel': 1})
    assert aluguel_hotel == 2000, f"Esperado 2000, obtido {aluguel_hotel}"
    # Teste com monopolio
    aluguel_monopolio = estrategiaAluguel.calcula(100, {'monopolio': True})
    assert aluguel_monopolio == 200, f"Esperado 200, obtido {aluguel_monopolio}"
    # Teste sem construções ou monopolio
    aluguel_base = estrategiaAluguel.calcula(100, {})
    assert aluguel_base == 100, f"Esperado 100, obtido {aluguel_base}"

if __name__ == "__main__":
    test_estrategia_aluguel_calculo()