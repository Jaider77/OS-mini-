import tkinter as tk
from tkinter import ttk, messagebox
import psutil # Biblioteca específica para este módulo

def abrir_gestion_procesos(ventana_padre):
    """Crea la ventana del gestor de procesos."""
    procesos_win = tk.Toplevel(ventana_padre)
    procesos_win.title("Gestión de Procesos")
    procesos_win.geometry("500x450")

    frame = ttk.Frame(procesos_win, padding="10")
    frame.pack(expand=True, fill=tk.BOTH)

    # Frame para la lista
    list_frame = ttk.Frame(frame)
    list_frame.pack(expand=True, fill=tk.BOTH)

    listbox = tk.Listbox(list_frame, height=15)
    scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
    listbox.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.pack(expand=True, fill=tk.BOTH)

    def listar_procesos():
        """Requerimiento B.1: Lista los procesos activos."""
        listbox.delete(0, tk.END)
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                listbox.insert(tk.END, f"PID: {proc.info['pid']} - Nombre: {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    # Frame de controles (matar proceso)
    control_frame = ttk.Frame(frame)
    control_frame.pack(fill=tk.X, pady=10)

    lbl_pid = ttk.Label(control_frame, text="PID a finalizar:")
    lbl_pid.pack(side=tk.LEFT, padx=5)
    
    entry_pid = ttk.Entry(control_frame, width=10)
    entry_pid.pack(side=tk.LEFT, padx=5)

    def finalizar_proceso():
        """Requerimiento B.2: Finaliza un proceso por su PID."""
        try:
            pid = int(entry_pid.get())
            proceso = psutil.Process(pid)
            proceso.terminate()
            messagebox.showinfo("Éxito", f"Proceso {pid} finalizado.", parent=procesos_win)
            listar_procesos() # Refrescar lista
        except ValueError:
            messagebox.showerror("Error", "Ingrese un PID numérico.", parent=procesos_win)
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", f"No se encontró el PID {pid}.", parent=procesos_win)
        except psutil.AccessDenied:
            messagebox.showerror("Error", f"Permisos denegados para finalizar {pid}.", parent=procesos_win)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}", parent=procesos_win)

    btn_finalizar = ttk.Button(control_frame, text="Finalizar Proceso", command=finalizar_proceso)
    btn_finalizar.pack(side=tk.LEFT, padx=5)

    btn_refrescar = ttk.Button(control_frame, text="Refrescar Lista", command=listar_procesos)
    btn_refrescar.pack(side=tk.RIGHT, padx=5)

    # Carga inicial
    listar_procesos()