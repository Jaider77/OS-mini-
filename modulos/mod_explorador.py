import tkinter as tk
from tkinter import ttk, messagebox
import os

def abrir_explorador(ventana_padre):
    """Crea la ventana del explorador de archivos."""
    explorador_win = tk.Toplevel(ventana_padre)
    explorador_win.title("Explorador de Archivos")
    explorador_win.geometry("500x400")

    # Frame principal
    frame = ttk.Frame(explorador_win, padding="10")
    frame.pack(expand=True, fill=tk.BOTH)

    # Label para la ruta actual
    ruta_actual_var = tk.StringVar(value=os.getcwd())
    lbl_ruta = ttk.Label(frame, textvariable=ruta_actual_var, relief="sunken", padding=5)
    lbl_ruta.pack(fill=tk.X)

    # Frame para botones
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill=tk.X, pady=5)

    # Listbox para mostrar archivos y carpetas
    listbox = tk.Listbox(frame, height=15)
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
    listbox.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.pack(expand=True, fill=tk.BOTH)

    # --- Funciones internas del módulo ---

    def actualizar_lista():
        """Limpia y rellena el listbox con el contenido del directorio actual."""
        try:
            ruta = ruta_actual_var.get()
            os.chdir(ruta) # Aseguramos estar en el directorio
            listbox.delete(0, tk.END) # Limpiar lista
            
            items = os.listdir(ruta)
            
            if not items:
                # Requerimiento A.4: Mensaje si está vacía
                listbox.insert(tk.END, "[Carpeta vacía]")
                return

            for item in sorted(items, key=lambda s: s.lower()):
                if os.path.isdir(os.path.join(ruta, item)):
                    listbox.insert(tk.END, f"[CARPETA] {item}")
                else:
                    listbox.insert(tk.END, item)
        except PermissionError:
            listbox.delete(0, tk.END)
            listbox.insert(tk.END, "[Error: Permiso denegado]")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el directorio: {e}", parent=explorador_win)
            subir_nivel()

    def subir_nivel():
        """Sube un nivel en la jerarquía de directorios."""
        nueva_ruta = os.path.abspath(os.path.join(ruta_actual_var.get(), '..'))
        ruta_actual_var.set(nueva_ruta)
        actualizar_lista()

    def navegar(event):
        """Entra en una carpeta al hacer doble clic."""
        try:
            seleccion = listbox.get(listbox.curselection())
            
            if seleccion.startswith("[CARPETA] "):
                seleccion = seleccion[10:]
            
            nueva_ruta = os.path.join(ruta_actual_var.get(), seleccion)
            
            if os.path.isdir(nueva_ruta):
                ruta_actual_var.set(nueva_ruta)
                actualizar_lista()
        except tk.TclError:
            pass 
        except Exception as e:
            messagebox.showerror("Error", f"Error al navegar: {e}", parent=explorador_win)

    # --- Configuración de widgets y carga inicial ---
    
    listbox.bind("<Double-1>", navegar)

    # Requerimiento A.2: Refrescar
    btn_refrescar = ttk.Button(btn_frame, text="Refrescar", command=actualizar_lista)
    btn_refrescar.pack(side=tk.LEFT, padx=5)

    # Requerimiento A.3: Subir Nivel
    btn_subir = ttk.Button(btn_frame, text="Subir Nivel (..)", command=subir_nivel)
    btn_subir.pack(side=tk.LEFT, padx=5)

    # Carga inicial
    actualizar_lista()