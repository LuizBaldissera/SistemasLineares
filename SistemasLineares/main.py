import tkinter as tk
from tkinter import ttk, messagebox
import time

# =========================
# MÉTODOS NUMÉRICOS
# =========================

def gauss(A, b):
    n = len(A)

    for i in range(n):
        if A[i][i] == 0:
            raise Exception("Matriz singular")

        for j in range(i + 1, n):
            fator = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= fator * A[i][k]
            b[j] -= fator * b[i]

    x = [0] * n
    for i in range(n - 1, -1, -1):
        soma = sum(A[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (b[i] - soma) / A[i][i]

    return x


def jacobi(A, b, tol, max_iter):
    n = len(A)
    x = [0] * n

    for it in range(max_iter):
        x_new = x.copy()

        for i in range(n):
            soma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - soma) / A[i][i]

        erro = max(abs(x_new[i] - x[i]) for i in range(n))
        x = x_new

        if erro < tol:
            return x, it + 1

    raise Exception("Não convergiu")


def gauss_seidel(A, b, tol, max_iter):
    n = len(A)
    x = [0] * n

    for it in range(max_iter):
        x_old = x.copy()

        for i in range(n):
            soma1 = sum(A[i][j] * x[j] for j in range(i))
            soma2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
            x[i] = (b[i] - soma1 - soma2) / A[i][i]

        erro = max(abs(x[i] - x_old[i]) for i in range(n))

        if erro < tol:
            return x, it + 1

    raise Exception("Não convergiu")


# =========================
# APP
# =========================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de Sistemas Lineares")
        self.root.geometry("700x600")
        self.root.configure(bg="#f4f6f8")

        self.entries = []

        # ===== Frame topo =====
        topo = tk.Frame(root, bg="#f4f6f8")
        topo.pack(pady=10)

        tk.Label(topo, text="Tamanho (n):", bg="#f4f6f8").grid(row=0, column=0, padx=5)
        self.n_entry = ttk.Entry(topo, width=5)
        self.n_entry.grid(row=0, column=1)

        ttk.Button(topo, text="Criar Matriz", command=self.criar_matriz).grid(row=0, column=2, padx=10)

        # ===== Parâmetros =====
        params = tk.LabelFrame(root, text="Parâmetros", padx=10, pady=10)
        params.pack(pady=10, fill="x", padx=20)

        tk.Label(params, text="Tolerância:").grid(row=0, column=0, padx=5)
        self.tol_entry = ttk.Entry(params, width=10)
        self.tol_entry.insert(0, "0.001")
        self.tol_entry.grid(row=0, column=1)

        tk.Label(params, text="Máx Iterações:").grid(row=0, column=2, padx=5)
        self.iter_entry = ttk.Entry(params, width=10)
        self.iter_entry.insert(0, "100")
        self.iter_entry.grid(row=0, column=3)

        tk.Label(params, text="Método:").grid(row=0, column=4, padx=5)
        self.metodo = ttk.Combobox(params, values=["Gauss", "Jacobi", "Gauss-Seidel"], state="readonly")
        self.metodo.current(0)
        self.metodo.grid(row=0, column=5)

        # ===== Matriz =====
        self.frame_matriz = tk.LabelFrame(root, text="Matriz A | b", padx=10, pady=10)
        self.frame_matriz.pack(pady=10)

        # ===== Botão =====
        ttk.Button(root, text="Resolver", command=self.resolver).pack(pady=10)

        # ===== Resultado =====
        resultado_frame = tk.LabelFrame(root, text="Resultado", padx=10, pady=10)
        resultado_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.resultado = tk.Text(resultado_frame, height=10, font=("Consolas", 10))
        self.resultado.pack(fill="both", expand=True)

    def criar_matriz(self):
        try:
            n = int(self.n_entry.get())
        except:
            messagebox.showerror("Erro", "Digite um tamanho válido")
            return

        for widget in self.frame_matriz.winfo_children():
            widget.destroy()

        self.entries = []

        for i in range(n):
            linha = []
            for j in range(n + 1):
                e = ttk.Entry(self.frame_matriz, width=6, justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)
                linha.append(e)
            self.entries.append(linha)

    def resolver(self):
        try:
            n = len(self.entries)

            A = []
            b = []

            for i in range(n):
                linha = []
                for j in range(n):
                    linha.append(float(self.entries[i][j].get()))
                A.append(linha)
                b.append(float(self.entries[i][n].get()))

            metodo = self.metodo.get()
            tol = float(self.tol_entry.get())
            max_iter = int(self.iter_entry.get())

            inicio = time.time()

            if metodo == "Gauss":
                x = gauss([row[:] for row in A], b[:])
                iteracoes = "-"
            elif metodo == "Jacobi":
                x, iteracoes = jacobi(A, b, tol, max_iter)
            else:
                x, iteracoes = gauss_seidel(A, b, tol, max_iter)

            fim = time.time()
            tempo = (fim - inicio) * 1000

            self.resultado.delete(1.0, tk.END)

            self.resultado.insert(tk.END, "=== SOLUÇÃO ===\n\n")
            for i, val in enumerate(x):
                self.resultado.insert(tk.END, f"x{i+1} = {val:.6f}\n")

            self.resultado.insert(tk.END, "\n=== INFO ===\n")
            self.resultado.insert(tk.END, f"Iterações: {iteracoes}\n")
            self.resultado.insert(tk.END, f"Tempo: {tempo:.4f} ms\n")

        except Exception as e:
            messagebox.showerror("Erro", str(e))


# =========================
# EXECUÇÃO
# =========================

root = tk.Tk()
app = App(root)
root.mainloop()