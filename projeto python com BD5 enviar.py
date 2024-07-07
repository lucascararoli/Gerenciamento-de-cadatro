import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3

class CadastroApp:
    def __init__(self, master):
        self.master = master
        master.title("Ferramenta de Gerenciamento de Cadastro")

        # Conectar ao banco de dados SQLite
        self.conn = sqlite3.connect('cadastro.db')
        self.create_tables()

        self.create_widgets()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY,
                cpf TEXT NOT NULL,
                data TEXT NOT NULL,
                material TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        # Labels e Entradas para Clientes
        self.cliente_labels = []
        self.cliente_entries = []
        for i in range(1):
            label = tk.Label(self.master, text=f"Cliente {i+1} (CPF):")
            label.grid(row=i, column=0, padx=10, pady=5)
            self.cliente_labels.append(label)
            
            entry = tk.Entry(self.master)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.cliente_entries.append(entry)

        # Labels e Entradas para Materiais
        self.materiais_labels = []
        self.materiais_entries = []
        materiais = ["Cesta Básica", "Água", "Colchão"]
        for i, material in enumerate(materiais):
            label = tk.Label(self.master, text=material + ":")
            label.grid(row=i, column=2, padx=10, pady=5)
            self.materiais_labels.append(label)
            
            entry = tk.Entry(self.master)
            entry.grid(row=i, column=3, padx=10, pady=5)
            self.materiais_entries.append(entry)

        # Campo e Botão para Inserir Nome da Pessoa
        self.nome_label = tk.Label(self.master, text="Nome:")
        self.nome_label.grid(row=4, column=0, padx=10, pady=5)

        self.nome_entry = tk.Entry(self.master)
        self.nome_entry.grid(row=4, column=1, padx=10, pady=5)

        self.insert_button = tk.Button(self.master, text="Inserir Nome", command=self.inserir_nome)
        self.insert_button.grid(row=4, column=2, padx=10, pady=5)

        # Campo para Data
        self.data_label = tk.Label(self.master, text="Data (dd/mm/yyyy):")
        self.data_label.grid(row=5, column=0, padx=10, pady=5)

        self.data_entry = tk.Entry(self.master)
        self.data_entry.grid(row=5, column=1, padx=10, pady=5)

        # Botão de Submissão
        self.submit_button = tk.Button(self.master, text="Cadastrar", command=self.submit)
        self.submit_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Botão para Limpar Dados
        self.clear_button = tk.Button(self.master, text="Limpar Dados", command=self.limpar_dados)
        self.clear_button.grid(row=6, column=2, columnspan=2, pady=10)

    def inserir_nome(self):
        nome = self.nome_entry.get()
        if nome:
            for entry in self.cliente_entries:
                if not entry.get():  # Insere o nome no primeiro campo de cliente vazio
                    entry.insert(0, nome)
                    break
            self.nome_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Por favor, insira um nome.")

    def validar_data(self, data_text):
        try:
            data = datetime.strptime(data_text, "%d/%m/%Y")
            return data
        except ValueError:
            return None

    def submit(self):
        clientes = [entry.get() for entry in self.cliente_entries]
        materiais = [entry.get() for entry in self.materiais_entries]
        data_text = self.data_entry.get()
        data = self.validar_data(data_text)

        # Validar entrada
        if all(clientes) and all(materiais) and data:
            data_str = data.strftime('%Y-%m-%d')
            cursor = self.conn.cursor()
            for cpf in clientes:
                # Verificar duplicidade de CPF no mesmo dia
                cursor.execute('SELECT * FROM registros WHERE cpf = ? AND data = ?', (cpf, data_str))
                if cursor.fetchone():
                    messagebox.showerror("Erro", f"O CPF {cpf} já retirou um produto neste dia.")
                    return

            # Adicionar registros
            for cpf, material in zip(clientes, materiais):
                cursor.execute('INSERT INTO registros (cpf, data, material) VALUES (?, ?, ?)', (cpf, data_str, material))
            self.conn.commit()

            cadastro_info = "Clientes cadastrados:\n" + "\n".join(clientes) + "\n\nMateriais cadastrados:\n" + "\n".join(materiais) + f"\n\nData: {data_text}"
            messagebox.showinfo("Cadastro Realizado", cadastro_info)
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")

    def limpar_dados(self):
        # Limpar campos de entrada de clientes
        for entry in self.cliente_entries:
            entry.delete(0, tk.END)

        # Limpar campos de entrada de materiais
        for entry in self.materiais_entries:
            entry.delete(0, tk.END)

        # Limpar campo de data
        self.data_entry.delete(0, tk.END)

        # Limpar campo de nome
        self.nome_entry.delete(0, tk.END)

        messagebox.showinfo("Dados Limpados", "Todos os campos foram limpos.")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroApp(root)
    root.mainloop()
    
