import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.titulo import tituloPropriedade, titulo, tituloCompanhia


def test_titulo_inicializacao():
    print("-----")
    print("Testando: inicialização de título básico")
    print("-----")
    proprietario_mock = object()
    titulo_instance = titulo(proprietario_mock, False, 500)
    assert titulo_instance.proprietario == proprietario_mock
    assert titulo_instance.hipotecado is False
    assert titulo_instance.valorHipoteca == 500

def test_titulo_hipotecar():
    print("-----")
    print("Testando: hipotecar título")
    print("-----")
    proprietario_mock = object()
    titulo_instance = titulo(proprietario_mock, False, 500)
    titulo_instance.hipotecar()
    assert titulo_instance.hipotecado is True

def test_resgatar_hipoteca():
    print("-----")
    print("Testando: resgatar hipoteca de título")
    print("-----")
    titulo_i = titulo(None, True, 500)
    titulo_i.resgatar_hipoteca()
    assert titulo_i.hipotecado is False
    
def test_transferir_proprietario():
    print("-----")
    print("Testando: transferir proprietário do título")
    print("-----")
    proprietario1 = object()
    proprietario2 = object()
    titulo_instance = titulo(proprietario1, False, 500)
    titulo_instance.transferir_proprietario(proprietario2)
    assert titulo_instance.proprietario == proprietario2
    
def test_titulo_propriedade_inicializacao():
    print("-----")
    print("Testando: inicialização de título de propriedade")
    print("-----")
    propriedade_mock = object()
    titulo_prop_instance = tituloPropriedade(None, False, 1000, propriedade_mock, 2, 200)
    assert titulo_prop_instance.propriedade == propriedade_mock
    assert titulo_prop_instance.valor_casa == 2
    assert titulo_prop_instance.valor_hotel == 200
    assert titulo_prop_instance.aluguel_por_construcao == 10
    
def tes_obter_aluguel_atual_propriedade():
    print("-----")
    print("Testando: obter aluguel atual de título de propriedade")
    print("-----")
    class PropriedadeMock:
        def calcula_aluguel(self):
            return 300
    propriedade_mock = PropriedadeMock()
    titulo_prop_instance = tituloPropriedade(None, False, 1000, propriedade_mock, 2, 200)
    aluguel = titulo_prop_instance.obter_aluguel_atual()    
    assert aluguel == 300

def test_contruir_e_vender_cas():
    print("-----")
    print("Testando: construir casa em título de propriedade")
    print("-----")
    class PropriedadeMock:
        def __init__(self):
            self.casas = 0
    propriedade_mock = PropriedadeMock()
    titulo_prop_instance = tituloPropriedade(None, False, 1000, propriedade_mock, 2, 200)
    titulo_prop_instance.contruir_casa()
    assert propriedade_mock.casas == 1
    print("----- Após construir casa -----")
    print("teste vender casa")
    print("-----")
    titulo_prop_instance.vender_construcao("casa")
    assert propriedade_mock.casas == 0
    
def test_contruir_e_vender_hotel():
    print("-----")
    print("Testando: construir hotel em título de propriedade")
    print("-----")
    class PropriedadeMock:
        def __init__(self):
            self.hotel = 0
    propriedade_mock = PropriedadeMock()
    titulo_prop_instance = tituloPropriedade(None, False, 1000, propriedade_mock, 2, 200)
    titulo_prop_instance.construir_hotel()
    assert propriedade_mock.hotel == 1
    print("----- Após construir casa -----")
    print("teste vender casa")
    print("-----")
    titulo_prop_instance.vender_construcao("hotel")
    assert propriedade_mock.hotel == 0
    
def test_titulo_companhia_inicializacao():
    print("-----")
    print("Testando: inicialização de título de companhia")
    print("-----")
    compahia_mock = object()
    titulo_comp_instance = tituloCompanhia(None, False, 1500, compahia_mock)
    assert titulo_comp_instance.companhia == compahia_mock
    assert titulo_comp_instance.hipotecado is False
    assert titulo_comp_instance.valorHipoteca == 1500
    
def test_obter_aluguel_companhia():
    print("-----")
    print("Testando: obter aluguel de título de companhia")
    print("-----")
    class CompanhiaMock:
        def calcula_aluguel(self, valor_dado, quantidade):
            return valor_dado * quantidade * 2
    companhia_mock = CompanhiaMock()
    titulo_comp_instance = tituloCompanhia(None, False, 1500, companhia_mock)
    aluguel = titulo_comp_instance.obter_aluguel(100, 3)
    assert aluguel == 600
    

if __name__ == "__main__":
    test_titulo_inicializacao()
    test_resgatar_hipoteca()
    test_titulo_hipotecar()
    test_transferir_proprietario()
    test_contruir_e_vender_cas()
    test_contruir_e_vender_hotel()
    tes_obter_aluguel_atual_propriedade()
    test_titulo_propriedade_inicializacao()
    test_titulo_companhia_inicializacao()
    test_obter_aluguel_companhia()