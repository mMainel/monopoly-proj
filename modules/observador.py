from abc import ABC, abstractmethod
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.eventoJogo import EventoJogo

class Observador(ABC):
    """
    classe abstrata, onde defino por -> ABC, onde eu posso depois criar uma classe a partir desta passando 'Observador' como parametro da classe
    o 'abstractmethod' serve pra 'tagearmos' um método obrigatório nas subclasses, ou seja, toda classe que eu criar a partir de observador, deve ter o método notificar implementado
    """
    @abstractmethod
    def notificar(self, evento: 'EventoJogo') -> None:
        pass