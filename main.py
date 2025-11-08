import tkinter as tk
from tkinter import ttk

# --- Importación de nuestros módulos ---
# Gracias a __init__.py, podemos importar desde la carpeta 'modulos'
from modulos.mod_explorador import abrir_explorador
from modulos.mod_procesos import abrir_gestion_procesos
from modulos.mod_shell import abrir_shell
from modulos.mod_info import abrir_info_sistema

# --- Ventana Principal (Requisito E) ---

# 1. Crear la ventana raíz
root = tk.Tk()
root.title("Mini Sistema Operativo") # E.2: Título
root.geometry("300x250")

# 2. Usar un Frame para organizar
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(expand=True, fill=tk.BOTH)

# Estilo para los botones
style = ttk.Style()
style.configure("TButton", padding=10, font=('Arial', 10, 'bold'))

# 3. E.1 y E.3: Botones para abrir módulos
# Usamos 'lambda' para poder pasar el argumento 'root' a nuestras funciones
# Esto le dice a cada módulo quién es su ventana "padre"

btn_explorador = ttk.Button(
    main_frame, 
    text="Explorador de Archivos", 
    command=lambda: abrir_explorador(root), # Pasa 'root' como padre
    style="TButton"
)
btn_explorador.pack(fill=tk.X, pady=5)

btn_procesos = ttk.Button(
    main_frame, 
    text="Gestión de Procesos", 
    command=lambda: abrir_gestion_procesos(root), # Pasa 'root' como padre
    style="TButton"
)
btn_procesos.pack(fill=tk.X, pady=5)

btn_shell = ttk.Button(
    main_frame, 
    text="Shell Educativa", 
    command=lambda: abrir_shell(root), # Pasa 'root' como padre
    style="TButton"
)
btn_shell.pack(fill=tk.X, pady=5)

btn_info = ttk.Button(
    main_frame, 
    text="Información del Sistema", 
    command=lambda: abrir_info_sistema(root), # Pasa 'root' como padre
    style="TButton"
)
btn_info.pack(fill=tk.X, pady=5)

# 4. Iniciar el bucle principal
if __name__ == "__main__":
    root.mainloop()