from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    def __init__(self, valor: float, descricao: str, data: str = None):
        self.valor = valor
        self.descricao = descricao
        self.data = data or datetime.now().strftime("%d/%m/%Y")

    @abstractmethod
    def calcular_impacto(self) -> float:
        pass

class Despesa(Transacao):
    def __init__(self, valor: float, descricao: str, categoria: str, data: str = None):
        super().__init__(valor, descricao, data)
        self.categoria = categoria

    def calcular_impacto(self) -> float:
        return -self.valor

class Receita(Transacao):
    def __init__(self, valor: float, descricao: str, fonte: str, data: str = None):
        super().__init__(valor, descricao, data)
        self.fonte = fonte

    def calcular_impacto(self) -> float:  # Corrigido o nome do método
        return self.valor