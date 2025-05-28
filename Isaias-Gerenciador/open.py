import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.usuario import Usuario
from models.transacao import Receita, Despesa
from utils.graficos import plotar_gastos_por_categoria
import os
from pathlib import Path

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Login")
        self.geometry("300x150")
        self.resizable(False, False)
        
        ttk.Label(self, text="Bem-vindo ao Gerenciador Financeiro").pack(pady=10)
        ttk.Label(self, text="Digite seu nome:").pack()
        self.nome_entry = ttk.Entry(self)
        self.nome_entry.pack(pady=5)
        ttk.Button(self, text="Entrar", command=self._validar).pack(pady=10)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _validar(self):
        if nome := self.nome_entry.get().strip():
            Path("data/usuarios").mkdir(parents=True, exist_ok=True)
            self.parent.nome_usuario = nome
            self.destroy()
        else:
            messagebox.showerror("Erro", "O nome não pode estar vazio!")
    
    def _on_close(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair do programa?"):
            self.parent.quit()

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.usuario = None
        self.root.withdraw()
        self.root.title("Gerenciador Financeiro")
        self.root.geometry("800x600")
        self._mostrar_login()
    
    def _mostrar_login(self):
        login = LoginWindow(self.root)
        self.root.wait_window(login)
        
        if hasattr(self.root, 'nome_usuario'):
            self.usuario = Usuario(self.root.nome_usuario)
            self.root.title(f"Gerenciador Financeiro - {self.usuario.nome}")
            self._setup_ui()
            self.root.deiconify()
        else:
            self.root.destroy()
    
    def _setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill='both')
        
        self.frame_transacoes = ttk.Frame(self.notebook)
        self._build_transactions_tab()
        self.notebook.add(self.frame_transacoes, text="Registrar Transações")
        
        self.frame_relatorios = ttk.Frame(self.notebook)
        self._build_reports_tab()
        self.notebook.add(self.frame_relatorios, text="Relatórios")

    def _build_transactions_tab(self):
        frame = ttk.LabelFrame(self.frame_transacoes, text="Nova Transação", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Tipo:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.tipo_var = tk.StringVar(value="Despesa")
        ttk.Combobox(frame, textvariable=self.tipo_var, 
                    values=["Receita", "Despesa"], state="readonly").grid(row=0, column=1, sticky='ew')
        
        ttk.Label(frame, text="Valor:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.valor_entry = ttk.Entry(frame)
        self.valor_entry.grid(row=1, column=1, sticky='ew')
        
        ttk.Label(frame, text="Descrição:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.descricao_entry = ttk.Entry(frame)
        self.descricao_entry.grid(row=2, column=1, sticky='ew')
        
        ttk.Label(frame, text="Categoria/Fonte:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.categoria_entry = ttk.Entry(frame)
        self.categoria_entry.grid(row=3, column=1, sticky='ew')
        
        ttk.Button(frame, text="Adicionar", command=self._adicionar_transacao).grid(row=4, column=1, pady=10)

    def _build_reports_tab(self):
        frame = ttk.Frame(self.frame_relatorios)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Resumo Financeiro", font=('Arial', 12, 'bold')).pack(pady=5)
        self.relatorio_text = tk.Text(frame, height=10, wrap=tk.WORD)
        self.relatorio_text.pack(fill='both', expand=True)
        ttk.Button(frame, text="Atualizar Relatório", command=self._atualizar_relatorio).pack(pady=5)
        ttk.Button(frame, text="Gerar Gráfico", command=self._gerar_grafico).pack(pady=5)
        self._atualizar_relatorio()

    def _adicionar_transacao(self):
        try:
            valor = float(self.valor_entry.get())
            descricao = self.descricao_entry.get().strip()
            categoria_fonte = self.categoria_entry.get().strip()
            
            if not descricao or not categoria_fonte:
                raise ValueError("Descrição e categoria/fonte são obrigatórias")
            
            if valor <= 0:
                raise ValueError("O valor deve ser positivo")
            
            transacao = Receita(valor, descricao, categoria_fonte) if self.tipo_var.get() == "Receita" else Despesa(valor, descricao, categoria_fonte)
            self.usuario.adicionar_transacao(transacao)
            
            messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
            self.valor_entry.delete(0, tk.END)
            self.descricao_entry.delete(0, tk.END)
            self.categoria_entry.delete(0, tk.END)
            self._atualizar_relatorio()
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Dados inválidos:\n{str(e)}")

    def _atualizar_relatorio(self):
        try:
            relatorio = self.usuario.gerar_relatorio()
            texto = (
                f"=== RESUMO FINANCEIRO ===\n\n"
                f"Saldo Total: R$ {relatorio['saldo']:.2f}\n"
                f"Total Receitas: R$ {relatorio['total_receitas']:.2f}\n"
                f"Total Despesas: R$ {relatorio['total_despesas']:.2f}\n\n"
                f"=== ÚLTIMAS TRANSAÇÕES ===\n"
            )
            
            for t in relatorio['transacoes'][:5]:  # Mostra as 5 mais recentes
                tipo = "RECEITA" if isinstance(t, Receita) else "DESPESA"
                texto += f"\n[{t.data}] {tipo}: {t.descricao[:20].ljust(20)} R$ {t.valor:>8.2f}"
            
            self.relatorio_text.config(state=tk.NORMAL)
            self.relatorio_text.delete(1.0, tk.END)
            self.relatorio_text.insert(tk.END, texto)
            self.relatorio_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar relatório:\n{str(e)}")

    def _gerar_grafico(self):
        try:
            if not any(isinstance(t, Despesa) for t in self.usuario.transacoes):
                messagebox.showinfo("Informação", "Nenhuma despesa registrada para gerar o gráfico.")
                return
                
            plotar_gastos_por_categoria(self.usuario)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível gerar o gráfico:\n{str(e)}")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()