# modulos/mod_procesos.py
import tkinter as tk
from tkinter import ttk, messagebox
import psutil  # Biblioteca específica para gestión de procesos
from .estilo import aplicar_gradiente_y_contenido

# =============================================================================
# FUNCIÓN PRINCIPAL DEL MÓDULO
# =============================================================================

def abrir_gestion_procesos(ventana_padre):
    """
    Crea y muestra la ventana del gestor de procesos.
    
    Esta función genera una ventana secundaria (Toplevel) que permite al usuario
    visualizar los procesos activos del sistema y finalizarlos si es necesario.
    
    Args:
        ventana_padre (tk.Tk): La ventana principal de la aplicación
    
    Returns:
        None
    """
    
    # =============================================================================
    # CONFIGURACIÓN DE LA VENTANA
    # =============================================================================
    
    procesos_win = tk.Toplevel(ventana_padre)
    procesos_win.title("Gestión de Procesos")
    procesos_win.geometry("700x550")
    procesos_win.resizable(True, True)
    
    # Aplicar fondo gradiente (azul a negro)
    canvas_fondo, frame_grad, mid_color = aplicar_gradiente_y_contenido(procesos_win, "#44B3EB", "#000000")

    # Usar un frame tk con el color medio como fondo para que no tape el gradiente
    frame = tk.Frame(frame_grad, bg=mid_color)
    frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    # =============================================================================
    # SECCIÓN: TÍTULO Y DESCRIPCIÓN
    # =============================================================================
    
    titulo_frame = ttk.Frame(frame)
    titulo_frame.pack(fill=tk.X, pady=(0, 10))
    
    titulo = ttk.Label(
        titulo_frame,
        text="Gestor de Procesos del Sistema",
        font=('Arial', 14, 'bold')
    )
    titulo.pack()
    
    descripcion = ttk.Label(
        titulo_frame,
        text="Visualiza y administra los procesos activos en tu sistema",
        font=('Arial', 9),
        foreground='gray'
    )
    descripcion.pack()
    
    # =============================================================================
    # SECCIÓN: LISTA DE PROCESOS
    # =============================================================================
    
    # Frame para la lista con scrollbar
    list_frame = ttk.Frame(frame)
    list_frame.pack(expand=True, fill=tk.BOTH, pady=10)
    
    # Listbox para mostrar los procesos
    listbox = tk.Listbox(
        list_frame,
        height=15,
        font=('Courier', 9),
        selectmode=tk.SINGLE
    )
    
    # Scrollbar vertical para la lista
    scrollbar = ttk.Scrollbar(
        list_frame,
        orient=tk.VERTICAL,
        command=listbox.yview
    )
    listbox.configure(yscrollcommand=scrollbar.set)
    
    # Empaquetar la lista y el scrollbar
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
    
    # =============================================================================
    # FUNCIONES INTERNAS DEL MÓDULO
    # =============================================================================
    
    def listar_procesos():
        """
        Lista todos los procesos activos del sistema en el listbox.
        
        Esta función:
        1. Limpia la lista actual
        2. Itera sobre todos los procesos del sistema
        3. Obtiene el PID y nombre de cada proceso
        4. Los muestra en formato: "PID: XXXX - Nombre: nombre_proceso"
        5. Maneja errores de procesos que desaparecen o sin acceso
        
        Returns:
            None
        """
        # Limpiar el listbox
        listbox.delete(0, tk.END)
        
        # Contador de procesos
        contador = 0
        
        try:
            # Iterar sobre todos los procesos del sistema
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    # Obtener información del proceso
                    pid = proc.info['pid']
                    nombre = proc.info['name']
                    usuario = proc.info.get('username', 'N/A')
                    
                    # Formatear y agregar a la lista
                    texto = f"PID: {pid:6d} | Nombre: {nombre:30s} | Usuario: {usuario}"
                    listbox.insert(tk.END, texto)
                    
                    contador += 1
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Ignorar procesos que ya no existen o no son accesibles
                    pass
            
            # Actualizar la etiqueta de contador
            lbl_contador.config(text=f"Total de procesos: {contador}")
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al listar procesos:\n{e}",
                parent=procesos_win
            )
    
    def finalizar_proceso():
        """
        Finaliza un proceso específico por su PID.
        
        Esta función:
        1. Lee el PID ingresado por el usuario
        2. Valida que sea un número
        3. Busca el proceso con ese PID
        4. Intenta finalizarlo
        5. Muestra mensajes de éxito o error
        6. Refresca la lista de procesos
        
        Returns:
            None
        """
        try:
            # Obtener el PID del campo de entrada
            pid_texto = entry_pid.get().strip()
            
            # Validar que no esté vacío
            if not pid_texto:
                messagebox.showwarning(
                    "Campo Vacío",
                    "Por favor, ingresa un PID válido.",
                    parent=procesos_win
                )
                return
            
            # Convertir a entero
            pid = int(pid_texto)
            
            # Obtener el proceso
            proceso = psutil.Process(pid)
            nombre_proceso = proceso.name()
            
            # Confirmar la acción
            respuesta = messagebox.askyesno(
                "Confirmar Finalización",
                f"¿Estás seguro de que deseas finalizar el proceso?\n\n"
                f"PID: {pid}\n"
                f"Nombre: {nombre_proceso}\n\n"
                f" Esta acción no se puede deshacer.",
                parent=procesos_win
            )
            
            if respuesta:
                # Finalizar el proceso
                proceso.terminate()
                
                # Mensaje de éxito
                messagebox.showinfo(
                    "Proceso Finalizado",
                    f"El proceso {pid} ({nombre_proceso}) ha sido finalizado exitosamente.",
                    parent=procesos_win
                )
                
                # Limpiar el campo de entrada
                entry_pid.delete(0, tk.END)
                
                # Refrescar la lista
                listar_procesos()
                
        except ValueError:
            # Error: no es un número
            messagebox.showerror(
                "Error de Formato",
                "El PID debe ser un número entero válido.",
                parent=procesos_win
            )
            
        except psutil.NoSuchProcess:
            # Error: el proceso no existe
            messagebox.showerror(
                "Proceso No Encontrado",
                f"No se encontró ningún proceso con el PID {pid}.",
                parent=procesos_win
            )
            
        except psutil.AccessDenied:
            # Error: permisos insuficientes
            messagebox.showerror(
                "Permiso Denegado",
                f"No tienes permisos suficientes para finalizar el proceso {pid}.\n\n"
                f" Intenta ejecutar la aplicación como administrador.",
                parent=procesos_win
            )
            
        except Exception as e:
            # Otros errores
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error al finalizar el proceso:\n{e}",
                parent=procesos_win
            )
    
    def obtener_pid_seleccionado():
        """
        Obtiene el PID del proceso seleccionado en la lista y lo coloca
        en el campo de entrada.
        
        Returns:
            None
        """
        try:
            # Obtener el índice seleccionado
            seleccion = listbox.curselection()
            
            if not seleccion:
                return
            
            # Obtener el texto del elemento seleccionado
            texto = listbox.get(seleccion[0])
            
            # Extraer el PID (formato: "PID: XXXX | ...")
            pid = texto.split("|")[0].split(":")[1].strip()
            
            # Colocar el PID en el campo de entrada
            entry_pid.delete(0, tk.END)
            entry_pid.insert(0, pid)
            
        except Exception as e:
            pass
    
    def cerrar_ventana():
        """
        Cierra la ventana del gestor de procesos.
        
        Esta función se ejecuta cuando el usuario hace clic en el botón
        de retroceso.
        
        Returns:
            None
        """
        procesos_win.destroy()
    
    # =============================================================================
    # CONFIGURACIÓN DE EVENTOS
    # =============================================================================
    
    # Vincular clic en la lista para obtener el PID
    listbox.bind("<ButtonRelease-1>", lambda e: obtener_pid_seleccionado())
    
    # =============================================================================
    # SECCIÓN: CONTROLES PARA FINALIZAR PROCESOS
    # =============================================================================
    
    control_frame = ttk.LabelFrame(frame, text="Finalizar Proceso", padding="10")
    control_frame.pack(fill=tk.X, pady=10)
    
    # Instrucciones
    instrucciones = ttk.Label(
        control_frame,
        text="💡 Selecciona un proceso de la lista o ingresa su PID manualmente",
        font=('Arial', 9),
        foreground='blue'
    )
    instrucciones.pack(pady=(0, 10))
    
    # Frame para entrada de PID
    entrada_frame = ttk.Frame(control_frame)
    entrada_frame.pack(fill=tk.X)
    
    # Label para el PID
    lbl_pid = ttk.Label(entrada_frame, text="PID a finalizar:", font=('Arial', 10))
    lbl_pid.pack(side=tk.LEFT, padx=5)
    
    # Entry para ingresar el PID
    entry_pid = ttk.Entry(entrada_frame, width=15, font=('Arial', 10))
    entry_pid.pack(side=tk.LEFT, padx=5)
    
    # Botón para finalizar el proceso
    btn_finalizar = ttk.Button(
        entrada_frame,
        text=" Finalizar Proceso",
        command=finalizar_proceso
    )
    btn_finalizar.pack(side=tk.LEFT, padx=5)
    
    # =============================================================================
    # SECCIÓN: BOTONES DE CONTROL INFERIOR
    # =============================================================================
    
    botones_frame = ttk.Frame(frame)
    botones_frame.pack(fill=tk.X, pady=10)
    
    # Botón: Refrescar Lista
    btn_refrescar = ttk.Button(
        botones_frame,
        text=" Refrescar Lista",
        command=listar_procesos
    )
    btn_refrescar.pack(side=tk.LEFT, padx=5)
    
    # Label contador de procesos
    lbl_contador = ttk.Label(
        botones_frame,
        text="Total de procesos: 0",
        font=('Arial', 9, 'bold')
    )
    lbl_contador.pack(side=tk.LEFT, padx=20)
    
    # Botón: Retroceder (NUEVO)
    btn_retroceder = ttk.Button(
        botones_frame,
        text=" Retroceder",
        command=cerrar_ventana
    )
    btn_retroceder.pack(side=tk.RIGHT, padx=5)
    
    # =============================================================================
    # INICIALIZACIÓN
    # =============================================================================
    
    # Cargar la lista inicial de procesos
    listar_procesos()
    
    # Advertencia de seguridad
    advertencia = ttk.Label(
        frame,
        text=" ADVERTENCIA: Finalizar procesos del sistema puede causar inestabilidad. Usa con precaución.",
        font=('Arial', 8),
        foreground='red',
        background='#fff3cd',
        relief=tk.SOLID,
        padding=5
    )
    advertencia.pack(fill=tk.X)
