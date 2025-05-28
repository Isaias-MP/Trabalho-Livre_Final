import json
import os
from pathlib import Path
from typing import List
from models.transacao import Despesa, Receita

class Usuario:
    def __init__(self, nome: str):
        self.nome = nome
        self._transacoes = []
        self._pasta_usuarios = Path("data/usuarios")
        self._arquivo_usuario = self._pasta_usuarios / f"{self._sanitize(nome)}.json"
        self._carregar_dados()

    def _sanitize(self, nome):
        """Remove caracteres inválidos para nome de arquivo"""
        return "".join(c for c in nome if c.isalnum() or c in (" ", "_")).strip().replace(" ", "_")

    def _carregar_dados(self):
        try:
            if self._arquivo_usuario.exists():
                with open(self._arquivo_usuario, 'r') as f:
                    dados = json.load(f)
                    for item in dados:
                        if 'categoria' in item:
                            self._transacoes.append(Despesa(**item))
                        else:
                            self._transacoes.append(Receita(**item))
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)
        self._salvar_dados()

    def _salvar_dados(self):
        try:
            self._pasta_usuarios.mkdir(parents=True, exist_ok=True)
            with open(self._arquivo_usuario, 'w') as f:
                json.dump([t.__dict__ for t in self._transacoes], f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

    @property
    def transacoes(self):
        return self._transacoes

    def gerar_relatorio(self):
        """Gera um relatório financeiro com saldo, totais e transações ordenadas por data"""
        receitas = sum(t.valor for t in self._transacoes if isinstance(t, Receita))
        despesas = sum(t.valor for t in self._transacoes if isinstance(t, Despesa))
        
        return {
            'saldo': receitas - despesas,
            'total_receitas': receitas,
            'total_despesas': despesas,
            'transacoes': sorted(self._transacoes, key=lambda x: x.data, reverse=True)
        }