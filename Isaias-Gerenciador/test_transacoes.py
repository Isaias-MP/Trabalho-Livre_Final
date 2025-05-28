import os
import unittest
from models.transacao import Despesa, Receita

class TestTransacoes(unittest.TestCase):
    def test_despesa(self):
        d = Despesa(100, "Teste", "Categoria")
        self.assertEqual(d.calcular_impacto(), -100)

    def test_receita(self):
        r = Receita(500, "Salário", "Trabalho")
        self.assertEqual(r.calcular_impacto(), 500)

if __name__ == "__main__":
    unittest.main()
    
from models.usuario import Usuario

class TestUsuario(unittest.TestCase):
    def test_adicionar_transacao(self):
        usuario = Usuario("Teste")
        usuario.adicionar_transacao(Receita(100, "Teste", "Fonte"))
        self.assertEqual(len(usuario.transacoes), 1)
        
    def test_salvar_json(self):
        usuario = Usuario("Teste")
        usuario.adicionar_transacao(Despesa(50, "Teste", "Categoria"))
        usuario.salvar_em_json("test_transacoes.json")
        self.assertTrue(os.path.exists("test_transacoes.json"))
        os.remove("test_transacoes.json")  # Limpeza