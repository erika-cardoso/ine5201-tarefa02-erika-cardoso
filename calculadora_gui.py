
import ast
import re
import tkinter as tk

# Criando a janela principal
janela = tk.Tk()

janela.title("Minha Calculadora")
janela.geometry("300x520")
janela.configure(bg="#F8C8DC")

# Criando o display
display = tk.Entry(
    janela,
    font=("Arial", 24),
    justify="right",
    bg="#FFF0F6",
    fg="#7A355B",
    readonlybackground="#FFF0F6",
    relief="flat"
)

display.pack(pady=20, padx=10, fill="x")


# Função para adicionar valores ao display
def adicionar_ao_display(valor):
    display.insert(tk.END, valor)


# Função para limpar o display
def limpar_display():
    display.delete(0, tk.END)


# Função para apagar o último caractere
def apagar_ultimo():
    conteudo = display.get()

    if conteudo:
        display.delete(len(conteudo) - 1, tk.END)


historico_operacoes = []


def adicionar_ao_historico(operacao):
    historico_operacoes.append(operacao)
    historico_lista.insert(tk.END, operacao)
    historico_lista.see(tk.END)


def limpar_historico():
    historico_operacoes.clear()
    historico_lista.delete(0, tk.END)


# Função para calcular
def calcular(expressao):
    try:
        if not expressao or not re.fullmatch(r"[0-9+\-*/(). ]+", expressao):
            raise ValueError

        if any(
            expressao[i] in "+-*/" and expressao[i + 1] in "+-*/"
            for i in range(len(expressao) - 1)
        ):
            raise ValueError

        arvore = ast.parse(expressao, mode="eval")

        def avaliar(no):
            if isinstance(no, ast.Expression):
                return avaliar(no.body)
            if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
                return float(no.value)
            if isinstance(no, ast.UnaryOp) and isinstance(no.op, (ast.UAdd, ast.USub)):
                valor = avaliar(no.operand)
                return valor if isinstance(no.op, ast.UAdd) else -valor
            if isinstance(no, ast.BinOp):
                esquerda = avaliar(no.left)
                direita = avaliar(no.right)
                if isinstance(no.op, ast.Add):
                    return esquerda + direita
                if isinstance(no.op, ast.Sub):
                    return esquerda - direita
                if isinstance(no.op, ast.Mult):
                    return esquerda * direita
                if isinstance(no.op, ast.Div):
                    return esquerda / direita
            raise ValueError

        resultado = avaliar(arvore)

        # Mostrar o resultado
        display.delete(0, tk.END)

        if resultado.is_integer():
            resultado = int(resultado)

        display.insert(tk.END, str(resultado))
        adicionar_ao_historico(f"{expressao} = {resultado}")

    except ZeroDivisionError:
        display.delete(0, tk.END)
        display.insert(tk.END, "Erro: divisão por zero")

    except (ValueError, SyntaxError):
        display.delete(0, tk.END)
        display.insert(tk.END, "Operação inválida")

# Função que identifica qual botão foi clicado
def clicar_botao(valor):

    if valor == "C":
        limpar_display()

    elif valor == "←":
        apagar_ultimo()

    elif valor == "=":
        expressao = display.get()
        calcular(expressao)

    else:
        adicionar_ao_display(valor)


# Criando o quadro dos botões
quadro = tk.Frame(janela, bg="#F8C8DC")
quadro.pack()

# Lista dos botões
botoes = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "←", "+"],
    ["=", "", "", ""]
]

# Percorrendo as linhas e colunas
for linha, lista_linha in enumerate(botoes):

    for coluna, texto in enumerate(lista_linha):

        if texto != "":

            botao = tk.Button(
                quadro,
                text=texto,
                font=("Arial", 16),
                width=5,
                height=2,
                command=lambda t=texto: clicar_botao(t),
                bg="#F48FB1",
                fg="#4A1F35",
                activebackground="#EC6FA6",
                activeforeground="#FFFFFF",
                relief="raised",
                bd=2
            )

            if texto == "=":
                botao.configure(bg="#D81B60", fg="#FFFFFF")
                botao.grid(
                    row=linha,
                    column=0,
                    columnspan=4,
                    padx=3,
                    pady=3,
                    sticky="nsew"
                )

            else:
                botao.grid(
                    row=linha,
                    column=coluna,
                    padx=3,
                    pady=3
                )


tk.Label(
    janela,
    text="Histórico",
    font=("Arial", 12),
    bg="#F8C8DC",
    fg="#7A355B"
).pack(pady=(8, 2))

historico_lista = tk.Listbox(
    janela,
    height=5,
    font=("Arial", 12),
    bg="#FFF0F6",
    fg="#7A355B",
    selectbackground="#F48FB1",
    selectforeground="#4A1F35",
    relief="flat"
)
historico_lista.pack(padx=10, fill="x")

tk.Button(
    janela,
    text="Limpar histórico",
    command=limpar_historico,
    bg="#E75480",
    fg="#FFFFFF",
    activebackground="#D81B60",
    activeforeground="#FFFFFF",
    relief="raised"
).pack(pady=5)


# Iniciando a interface
janela.mainloop()
