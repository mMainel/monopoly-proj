from abc import ABC, abstractmethod
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.eventoJogo import EventoJogo

class Observador(ABC):
    """
    Classe abstrata que define o contrato para observadores
    """

    @abstractmethod
    def notificar(self, evento: 'EventoJogo') -> None:
        """
        Recebe notificação de um evento do jogo e processa conforme necessário

        espera:
            evento: EventoJogo - evento ocorrido no jogo
        retorna:
            None
        """
        pass