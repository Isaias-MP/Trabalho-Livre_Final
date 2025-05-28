from models.transacao import Despesa, Receita
from models.usuario import Usuario


user = Usuario("Teste")
user.adicionar_transacao(Receita(500, "Freelance", "TI"))
user.adicionar_transacao(Despesa(50, "Café", "Alimentação"))

print("Saldo:", sum(t.calcular_impacto() for t in user.transacoes))