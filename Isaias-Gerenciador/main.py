from models.usuario import Usuario
from models.transacao import Despesa, Receita
from utils.graficos import plotar_gastos_por_categoria

import os
os.makedirs("data", exist_ok=True)

def main():
    usuario = Usuario("Maria")
    
    
    usuario.adicionar_transacao(Receita(3000, "Salário", "Trabalho"))
    usuario.adicionar_transacao(Despesa(150, "Mercado", "Alimentação"))
    
    print(usuario.gerar_relatorio())
    usuario.salvar_em_json()
    plotar_gastos_por_categoria(usuario)

if __name__ == "__main__":
    main()
