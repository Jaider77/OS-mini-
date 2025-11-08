import tkinter as tk
from tkinter import ttk, scrolledtext
import platform
import getpass
import psutil
import os

def abrir_info_sistema(ventana_padre):
    """Crea la ventana de información del sistema."""
    info_win = tk.Toplevel(ventana_padre)
    info_win.title("Información del Sistema")
    info_win.geometry("400x300")

    frame = ttk.Frame(info_win, padding="10")
    frame.pack(expand=True, fill=tk.BOTH)

    txt_info = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.DISABLED)
    txt_info.pack(expand=True, fill=tk.BOTH)

    # --- Recopilar información ---
    info_str = ""
    
    # D.1: Nombre de usuario
    try:
        info_str += f"Usuario Actual: {getpass.getuser()}\n"
    except Exception:
        info_str += "Usuario Actual: No disponible\n"
        
    info_str += "-"*30 + "\n"
    
    # D.2: Sistema Operativo y Versión
    info_str += f"Sistema Operativo: {platform.system()}\n"
    info_str += f"Release: {platform.release()}\n"
    info_str += f"Versión: {platform.version()}\n"
    info_str += f"Procesador: {platform.processor()}\n"
    
    info_str += "-"*30 + "\n"

    # D.3: Espacio en disco
    info_str += "Espacio en Disco:\n"
    try:
        particion_raiz = os.path.abspath(os.sep)
        uso = psutil.disk_usage(particion_raiz)
        
        def bytes_a_gb(b):
            return round(b / (1024**3), 2)

        info_str += f"  Partición: {particion_raiz}\n"
        info_str += f"  Total: {bytes_a_gb(uso.total)} GB\n"
        info_str += f"  Usado: {bytes_a_gb(uso.used)} GB\n"
        info_str += f"  Disponible: {bytes_a_gb(uso.free)} GB\n"
        info_str += f"  Porcentaje Usado: {uso.percent}%\n"

    except Exception as e:
        info_str += f"  No se pudo obtener información del disco: {e}\n"

    # --- Mostrar la información ---
    txt_info.config(state=tk.NORMAL)
    txt_info.insert(tk.END, info_str)
    txt_info.config(state=tk.DISABLED)