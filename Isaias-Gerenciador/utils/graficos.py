import matplotlib.pyplot as plt
from models.transacao import Despesa

def plotar_gastos_por_categoria(usuario):
    try:
        categorias = {}
        for t in usuario.transacoes:
            if isinstance(t, Despesa):
                categorias[t.categoria] = categorias.get(t.categoria, 0) + t.valor
        
        if not categorias:
            raise ValueError("Nenhuma despesa cadastrada para gerar gráfico")
        
        plt.bar(categorias.keys(), categorias.values())
        plt.title("Gastos por Categoria")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"⚠️ Erro ao gerar gráfico: {e}")