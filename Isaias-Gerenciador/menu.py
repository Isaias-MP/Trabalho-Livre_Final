from models.usuario import Usuario
from models.transacao import Despesa, Receita
from utils.graficos import plotar_gastos_por_categoria
import os

def adicionar_receita(usuario):
    print("\n" + "="*30)
    print("NOVA RECEITA".center(30))
    print("="*30)
    try:
        valor = float(input("Valor: R$ "))
        descricao = input("Descrição: ").strip()
        fonte = input("Fonte (ex: Salário, Freela): ").strip()
        
        if valor <= 0:
            print("⚠️ O valor deve ser positivo!")
            return
            
        usuario.adicionar_transacao(Receita(valor, descricao, fonte))
        print("\n✅ Receita adicionada com sucesso!")
    except ValueError:
        print("\n⚠️ Valor inválido! Use números (ex: 100.50)")

def adicionar_despesa(usuario):
    print("\n" + "="*30)
    print("NOVA DESPESA".center(30))
    print("="*30)
    try:
        valor = float(input("Valor: R$ "))
        descricao = input("Descrição: ").strip()
        categoria = input("Categoria (ex: Alimentação, Transporte): ").strip()
        
        if valor <= 0:
            print("⚠️ O valor deve ser positivo!")
            return
            
        usuario.adicionar_transacao(Despesa(valor, descricao, categoria))
        print("\n✅ Despesa adicionada com sucesso!")
    except ValueError:
        print("\n⚠️ Valor inválido! Use números (ex: 50.00)")

def ver_relatorio(usuario):
    relatorio = usuario.gerar_relatorio()
    print("\n" + "="*50)
    print(f" RELATÓRIO FINANCEIRO - {usuario.nome.upper()} ".center(50))
    print("="*50)
    print(f"\nSaldo Total: R$ {relatorio['saldo']:,.2f}")
    print(f"Total Receitas: R$ {relatorio['total_receitas']:,.2f}")
    print(f"Total Despesas: R$ {relatorio['total_despesas']:,.2f}")
    
    # Mostra situação financeira
    if relatorio['saldo'] > 0:
        print("\nSituação: Positiva 👍")
    elif relatorio['saldo'] < 0:
        print("\nSituação: Negativa 👎")
    else:
        print("\nSituação: Equilibrada ⚖️")
    
    print("\nÚltimas Transações:")
    if not relatorio["transacoes"]:
        print("Nenhuma transação registrada.")
    else:
        for t in relatorio["transacoes"][:5]:  # Mostra as 5 mais recentes
            tipo = "RECEITA" if isinstance(t, Receita) else "DESPESA"
            cor = "\033[92m" if tipo == "RECEITA" else "\033[91m"
            print(f"- [{t.data}] {cor}{tipo}\033[0m: {t.descricao} (R$ {abs(t.valor):,.2f})")

def ver_grafico(usuario):
    if not any(isinstance(t, Despesa) for t in usuario.transacoes):
        print("\n⚠️ Nenhuma despesa registrada para gerar o gráfico.")
        return
    plotar_gastos_por_categoria(usuario)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*50)
    print(" SISTEMA FINANCEIRO PESSOAL ".center(50))
    print("="*50)
    
    nome = input("\nDigite seu nome: ").strip()
    while not nome:
        print("⚠️ O nome não pode estar vazio!")
        nome = input("Digite seu nome: ").strip()
    
    usuario = Usuario(nome)
    print(f"\n✅ Olá, {usuario.nome}! Sistema pronto.")
    
    while True:
        print("\n" + "="*50)
        print(" MENU PRINCIPAL ".center(50))
        print("="*50)
        print("1. Adicionar Receita")
        print("2. Adicionar Despesa")
        print("3. Ver Relatório")
        print("4. Ver Gráfico de Gastos")
        print("5. Sair")
        print("="*50)

        opcao = input("\nEscolha uma opção (1-5): ").strip()

        if opcao == "1":
            adicionar_receita(usuario)
        elif opcao == "2":
            adicionar_despesa(usuario)
        elif opcao == "3":
            ver_relatorio(usuario)
        elif opcao == "4":
            ver_grafico(usuario)
        elif opcao == "5":
            print("\n📁 Salvando seus dados...")
            print("\nAté logo! 👋")
            break
        else:
            print("\n⚠️ Opção inválida! Digite um número de 1 a 5.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()