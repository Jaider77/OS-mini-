import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import os
from tkinter import messagebox

def abrir_shell(ventana_padre):
    """Crea la ventana de la shell."""
    shell_win = tk.Toplevel(ventana_padre)
    shell_win.title("Shell Educativa")
    shell_win.geometry("600x400")

    frame = ttk.Frame(shell_win, padding="10")
    frame.pack(expand=True, fill=tk.BOTH)

    # Requerimiento C.2: Salida del comando
    txt_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15, state=tk.DISABLED)
    txt_output.pack(expand=True, fill=tk.BOTH, pady=5)

    # Frame de entrada
    input_frame = ttk.Frame(frame)
    input_frame.pack(fill=tk.X)

    lbl_prompt = ttk.Label(input_frame, text="Comando >")
    lbl_prompt.pack(side=tk.LEFT, padx=5)

    entry_cmd = ttk.Entry(input_frame)
    entry_cmd.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=5)

    def ejecutar_comando():
        """Ejecuta el comando y muestra la salida."""
        comando_str = entry_cmd.get()
        if not comando_str:
            return

        # Comandos permitidos (C.1)
        comandos_validos = ['ls', 'dir', 'pwd', 'echo']
        comando_base = comando_str.split()[0].lower()

        # Validamos contra la lista educativa
        if comando_base not in comandos_validos:
            salida_formateada = f"\n[ERROR] Comando '{comando_base}' no permitido en esta shell educativa.\n"
            txt_output.config(state=tk.NORMAL)
            txt_output.insert(tk.END, salida_formateada)
            txt_output.config(state=tk.DISABLED)
            txt_output.see(tk.END)
            entry_cmd.delete(0, tk.END)
            return

        # En Windows, 'dir' y 'echo' son comandos de shell, necesitamos shell=True
        usa_shell = (os.name == 'nt' and (comando_base in ['dir', 'echo']))

        try:
            resultado = subprocess.run(
                comando_str, 
                capture_output=True, 
                text=True, 
                shell=True, # Simplificamos usando shell=True para todos los comandos permitidos
                encoding='utf-8', 
                errors='ignore'
            )
            
            salida = resultado.stdout
            error = resultado.stderr

            txt_output.config(state=tk.NORMAL)
            txt_output.insert(tk.END, f"\n--- Ejecutando: {comando_str} ---\n")
            if salida:
                txt_output.insert(tk.END, salida)
            if error:
                txt_output.insert(tk.END, f"[ERROR SHELL]\n{error}")
            txt_output.config(state=tk.DISABLED)
            txt_output.see(tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar: {e}", parent=shell_win)

        entry_cmd.delete(0, tk.END)

    btn_ejecutar = ttk.Button(input_frame, text="Ejecutar", command=ejecutar_comando)
    btn_ejecutar.pack(side=tk.RIGHT, padx=5)

    entry_cmd.bind("<Return>", lambda event: ejecutar_comando())