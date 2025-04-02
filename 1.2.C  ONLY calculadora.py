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

# Función para manejar los clics en los botones
def click_button(value):
    current = entry_display.get()
    entry_display.delete(0, tk.END)
    entry_display.insert(0, current + value)

def clear_display():
    entry_display.delete(0, tk.END)

# Función para mostrar mensajes de notificación
def show_notification(message, color="#d32f2f", clear_on_error=False):
    notification_label.config(text=message, fg=color)
    if clear_on_error:
        entry_display.delete(0, tk.END)
    notification_label.after(3000, lambda: notification_label.config(text=""))

# Actualizar el historial cuando se realiza un cálculo
def calculate_result():
    try:
        expression = entry_display.get()
        if not expression.strip():
            show_notification("La expresión está vacía", "#ffa000", clear_on_error=True)
            return
        result = eval(expression)  # Evalúa la expresión matemática
        if str(result) == expression:
            show_notification("El cálculo es redundante", "#ffa000")
            return
        calculation_history.append(expression + " = " + str(result))  # Guardar en el historial
        entry_display.delete(0, tk.END)
        entry_display.insert(0, str(result))
    except Exception:
        entry_display.delete(0, tk.END)  # Clear the input field visually on error
        show_notification("Expresión inválida", clear_on_error=True)

# Función para mostrar la pantalla de bienvenida
def show_welcome_screen():
    welcome_screen = tk.Toplevel(root)
    welcome_screen.title("Bienvenida")
    welcome_screen.geometry("400x600")
    welcome_screen.configure(bg="#1a73e8")
    welcome_screen.resizable(False, False)

    tk.Label(
        welcome_screen,
        text="Bienvenidos a\nCalculator Easy",
        font=("Segoe UI", 24, "bold"),
        bg="#1a73e8",
        fg="white",
        justify="center"
    ).pack(expand=True)

    # Programar el cierre de la pantalla de bienvenida después de 3 segundos
    def close_welcome():
        welcome_screen.destroy()

    root.after(3000, close_welcome)

# Mostrar la pantalla de bienvenida antes de iniciar la calculadora
root.withdraw()  # Ocultar la ventana principal
show_welcome_screen()
root.after(3000, root.deiconify)  # Mostrar la ventana principal después de 3 segundos

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

for (text, row, col) in buttons:
    if text == '=':
        tk.Button(calculator_frame, text=text, **button_style, bg="#1a73e8", command=calculate_result).grid(row=row, column=col, columnspan=4, sticky="nsew", pady=10)
    elif text == 'C':
        tk.Button(calculator_frame, text=text, **button_style, bg="#d32f2f", command=clear_display).grid(row=row, column=col, sticky="nsew")
    else:
        tk.Button(calculator_frame, text=text, **button_style, bg="#333333", command=lambda t=text: click_button(t)).grid(row=row, column=col, sticky="nsew")

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

# Reemplazar el botón de historial para abrir la ventana emergente
tk.Button(calculator_frame, text="Historial", font=("Segoe UI", 14), bg="#ffa000", fg="white", command=show_history).grid(row=7, column=3, sticky="nsew", pady=10)

for i in range(8):
    calculator_frame.grid_rowconfigure(i, weight=1)
for j in range(4):
    calculator_frame.grid_columnconfigure(j, weight=1)

# Ajustar el tamaño de las columnas y filas
for i in range(8):
    root.grid_rowconfigure(i, weight=1)
for j in range(4):  # Ajustar el rango para la calculadora
    root.grid_columnconfigure(j, weight=1)

# Asociar la tecla Enter con la función de cálculo
root.bind('<Return>', lambda event: calculate_result())

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
