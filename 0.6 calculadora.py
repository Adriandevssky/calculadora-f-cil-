import tkinter as tk
from tkinter import messagebox

def click_button(value):
    current = entry_display.get()
    entry_display.delete(0, tk.END)
    entry_display.insert(0, current + value)

def clear_display():
    entry_display.delete(0, tk.END)

def calculate_result():
    try:
        expression = entry_display.get()
        result = eval(expression)  # Evalúa la expresión matemática
        entry_display.delete(0, tk.END)
        entry_display.insert(0, str(result))
    except Exception as e:
        messagebox.showerror("Error", "Expresión inválida")

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora")
root.geometry("400x600")
root.resizable(False, False)
root.configure(bg="#202020")

# Crear el campo de entrada para mostrar los números y resultados
entry_display = tk.Entry(root, font=("Segoe UI", 24), bd=0, insertwidth=2, width=14, borderwidth=0, justify="right", bg="#2d2d2d", fg="white")
entry_display.grid(row=0, column=0, columnspan=4, ipady=20, pady=10)

# Crear botones
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
    ('=', 5, 0)
]

# Estilo de los botones
button_style = {
    "font": ("Segoe UI", 18),
    "bd": 0,
    "fg": "white",
    "activebackground": "#505050",
    "activeforeground": "white",
    "padx": 20,
    "pady": 20
}

# Crear y posicionar los botones
for (text, row, col) in buttons:
    if text == '=':
        tk.Button(root, text=text, **button_style, bg="#1a73e8", command=calculate_result).grid(row=row, column=col, columnspan=4, sticky="nsew", pady=10)
    elif text == 'C':
        tk.Button(root, text=text, **button_style, bg="#d32f2f", command=clear_display).grid(row=row, column=col, sticky="nsew")
    else:
        tk.Button(root, text=text, **button_style, bg="#333333", command=lambda t=text: click_button(t)).grid(row=row, column=col, sticky="nsew")

# Ajustar el tamaño de las columnas y filas
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for j in range(4):
    root.grid_columnconfigure(j, weight=1)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
