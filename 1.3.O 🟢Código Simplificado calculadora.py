import tkinter as tk
import tkinter.ttk as ttk  # Importar ttk para usar Notebook (pestañas)
from tkinter import messagebox

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora")
root.geometry("400x600")
root.resizable(False, False)
root.configure(bg="#202020")

# Lista para almacenar el historial de cálculos
calculation_history = []

# Funciones matemáticas
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
        return "Error: División por cero"

# Función para manejar los clics en los botones
def click_button(value):
    current = entry_display.get()  # Obtiene el contenido actual del campo de entrada
    entry_display.delete(0, tk.END)  # Limpia el campo de entrada
    entry_display.insert(0, current + value)  # Agrega el valor del botón presionado al campo de entrada

# Función para calcular el resultado
def calculate_result():
    try:
        expression = entry_display.get()  # Obtiene la expresión ingresada en el campo de entrada
        if not expression.strip():  # Verifica si el campo está vacío
            show_notification("La expresión está vacía", "#ffa000", clear_on_error=True)
            return

        # Separar los operandos y el operador
        tokens = expression.split()
        if len(tokens) != 3:
            show_notification("Formato inválido. Usa: número operador número", "#ffa000", clear_on_error=True)
            return

        num1, operator, num2 = tokens
        num1, num2 = float(num1), float(num2)

        # Realizar la operación
        if operator == '+':
            result = add(num1, num2)
        elif operator == '-':
            result = subtract(num1, num2)
        elif operator == '*':
            result = multiply(num1, num2)
        elif operator == '/':
            result = divide(num1, num2)
            if isinstance(result, str):  # Manejar división por cero
                messagebox.showerror("Error", result)
                return
        else:
            show_notification("Operador inválido", "#ffa000", clear_on_error=True)
            return

        # Guardar en el historial y mostrar el resultado
        calculation_history.append(expression + " = " + str(result))
        entry_display.delete(0, tk.END)
        entry_display.insert(0, str(result))
    except ValueError:
        show_notification("Por favor, ingresa valores numéricos válidos.", "#d32f2f", clear_on_error=True)

# Función para limpiar el campo de entrada
def clear_display():
    entry_display.delete(0, tk.END)

# Función para mostrar mensajes de notificación
def show_notification(message, color="#d32f2f", clear_on_error=False):
    notification_label.config(text=message, fg=color)
    if clear_on_error:
        entry_display.delete(0, tk.END)
    notification_label.after(3000, lambda: notification_label.config(text=""))

# Función para mostrar el historial en una ventana emergente
def show_history():
    if not calculation_history:
        show_notification("El historial está vacío", "#ffa000")
        return

    # Crear una nueva ventana para el historial
    history_window = tk.Toplevel(root)
    history_window.title("Historial")
    history_window.geometry("300x400")
    history_window.configure(bg="#2d2d2d")
    history_window.resizable(False, False)

    tk.Label(history_window, text="Historial de cálculos", font=("Segoe UI", 14), bg="#2d2d2d", fg="white").pack(pady=10)
    history_listbox = tk.Listbox(history_window, font=("Segoe UI", 12), bg="#202020", fg="white", selectbackground="#1a73e8", selectforeground="white")
    history_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Insertar los cálculos en el historial
    for item in calculation_history:
        history_listbox.insert(tk.END, item)

    # Función para usar una operación seleccionada
    def use_selected():
        selected = history_listbox.curselection()
        if selected:
            entry_display.delete(0, tk.END)
            entry_display.insert(0, calculation_history[selected[0]].split(" = ")[0])
        history_window.destroy()

    # Botón para usar la operación seleccionada
    tk.Button(history_window, text="Usar selección", font=("Segoe UI", 12), bg="#1a73e8", fg="white", command=use_selected).pack(pady=10)

    # Botón para cerrar la ventana del historial
    tk.Button(history_window, text="Cerrar", font=("Segoe UI", 12), bg="#d32f2f", fg="white", command=history_window.destroy).pack(pady=5)

# Crear el sistema de pestañas
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, columnspan=4, sticky="nsew")

# Crear el marco para la calculadora estándar
calculator_frame = tk.Frame(notebook, bg="#202020")
notebook.add(calculator_frame, text="Calculadora")

# Mover los elementos de la calculadora estándar al marco correspondiente
notification_label = tk.Label(calculator_frame, font=("Segoe UI", 12), bg="#202020", fg="white", anchor="center")
notification_label.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(5, 0))

entry_display = tk.Entry(calculator_frame, font=("Segoe UI", 24), bd=0, insertwidth=2, width=14, borderwidth=0, justify="right", bg="#2d2d2d", fg="white")
entry_display.grid(row=1, column=0, columnspan=4, ipady=20, pady=10)

# Configuración de los botones de la calculadora
buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('C', 5, 2), ('+', 5, 3),
    ('=', 6, 0)
]

button_style = {
    "font": ("Segoe UI", 18),
    "bd": 0,
    "fg": "white",
    "activebackground": "#505050",
    "activeforeground": "white",
    "padx": 20,
    "pady": 20
}

# Crear los botones y asignarles las funciones correspondientes
for (text, row, col) in buttons:
    if text == '=':
        tk.Button(calculator_frame, text=text, **button_style, bg="#1a73e8", command=calculate_result).grid(row=row, column=col, columnspan=4, sticky="nsew", pady=10)
    elif text == 'C':
        tk.Button(calculator_frame, text=text, **button_style, bg="#d32f2f", command=clear_display).grid(row=row, column=col, sticky="nsew")
    else:
        tk.Button(calculator_frame, text=text, **button_style, bg="#333333", command=lambda t=text: click_button(t)).grid(row=row, column=col, sticky="nsew")

# Ajustar el tamaño de las columnas y filas
for i in range(8):
    calculator_frame.grid_rowconfigure(i, weight=1)
for j in range(4):
    calculator_frame.grid_columnconfigure(j, weight=1)

# Asociar la tecla Enter con la función de cálculo
root.bind('<Return>', lambda event: calculate_result())

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
