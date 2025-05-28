from abc import ABC
from typing import List

class TagMixin:
    def __init__(self):
        self._tags: List[str] = []
    
    def adicionar_tag(self, tag: str):
        if tag not in self._tags:
            self._tags.append(tag)
    
    def remover_tag(self, tag: str):
        if tag in self._tags:
            self._tags.remove(tag)
    
    @property
    def tags(self):
        return self._tags.copy()

class Transacao(ABC, TagMixin):
    def __init__(self, valor: float, descricao: str, data: str = None):
        TagMixin.__init__(self)
        self.valor = valor