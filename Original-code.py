import tkinter as tk
from tkinter import messagebox

def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 != 0:
        return num1 / num2
    else:
        return "Error: Division by zero"

def calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operator = operator_var.get()

        if operator == '+':
            result = add(num1, num2)
        elif operator == '-':
            result = subtract(num1, num2)
        elif operator == '*':
            result = multiply(num1, num2)
        elif operator == '/':
            result = divide(num1, num2)
            if isinstance(result, str):  # Handle division by zero
                messagebox.showerror("Error", result)
                return
        else:
            messagebox.showerror("Error", "Operador inválido")
            return

        label_result.config(text=f"Resultado: {result}")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora")

# Crear widgets
tk.Label(root, text="Número 1:").grid(row=0, column=0, padx=10, pady=10)
entry_num1 = tk.Entry(root)
entry_num1.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Número 2:").grid(row=1, column=0, padx=10, pady=10)
entry_num2 = tk.Entry(root)
entry_num2.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Operador:").grid(row=2, column=0, padx=10, pady=10)
operator_var = tk.StringVar(value='+')
tk.OptionMenu(root, operator_var, '+', '-', '*', '/').grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Calcular", command=calculate).grid(row=3, column=0, columnspan=2, pady=10)

label_result = tk.Label(root, text="resultado : ")
label_result.grid(row=4, column=0, columnspan=2, pady=10)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()