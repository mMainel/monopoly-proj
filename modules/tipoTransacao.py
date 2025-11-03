from enum import Enum

class TipoTransacao(Enum):
    """
    Enumera os tipos de transações financeiras
    Usado pelo Banco para registrar histórico de movimentações
    """
    COMPRA_PROPRIEDADE = "Compra de Propriedade"
    VENDA_PROPRIEDADE = "Venda de Propriedade"
    ALUGUEL = "Pagamento de Aluguel"
    CONSTRUCAO = "Construção"
    HIPOTECA = "Hipoteca"
    SALARIO = "Salário"
    IMPOSTO = "Pagamento de Imposto"
    FIANCA = "Fiança da Cadeia"
    LEILAO = "Leilão"
    TRANSFERENCIA = "Transferência entre Jogadores"
    MULTA = "Multa"
    PREMIO = "Prêmio"
