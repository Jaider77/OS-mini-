import tkinter as tk
from tkinter import ttk, messagebox
import os
from .estilo import aplicar_gradiente_y_contenido

# =============================================================================
# FUNCIÓN PRINCIPAL DEL MÓDULO
# =============================================================================

def abrir_explorador(ventana_padre):
    """
    Crea y muestra la ventana del explorador de archivos.
    
    Esta función genera una ventana secundaria (Toplevel) que permite al usuario
    navegar por el sistema de archivos de manera visual e intuitiva.
    
    Args:
        ventana_padre (tk.Tk): La ventana principal de la aplicación
    
    Returns:
        None
    """
    
    # =============================================================================
    # CONFIGURACIÓN DE LA VENTANA
    # =============================================================================
    
    explorador_win = tk.Toplevel(ventana_padre)
    explorador_win.title("Explorador de Archivos")
    explorador_win.geometry("600x500")
    explorador_win.resizable(True, True)
    
    # Aplicar fondo gradiente (azul a negro)
    canvas_fondo, frame_grad, mid_color = aplicar_gradiente_y_contenido(explorador_win, "#44B3EB", "#000000")

    # Usar un frame tk con el color medio como fondo para que no tape el gradiente
    frame = tk.Frame(frame_grad, bg=mid_color)
    frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    # =============================================================================
    # SECCIÓN: BARRA SUPERIOR CON RUTA ACTUAL
    # =============================================================================
    
    # Variable que almacena la ruta del directorio actual
    ruta_actual_var = tk.StringVar(value=os.getcwd())
    
    # Label que muestra la ruta actual con estilo "hundido"
    lbl_ruta = ttk.Label(
        frame,
        textvariable=ruta_actual_var,
        relief="sunken",
        padding=5,
        font=('Courier', 9)
    )
    lbl_ruta.pack(fill=tk.X, pady=(0, 10))
    
    # =============================================================================
    # SECCIÓN: BOTONES DE CONTROL
    # =============================================================================
    
    # Frame para contener los botones de control
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill=tk.X, pady=5)
    
    # =============================================================================
    # SECCIÓN: LISTA DE ARCHIVOS Y CARPETAS
    # =============================================================================
    
    # Frame para la lista con scrollbar
    lista_frame = ttk.Frame(frame)
    lista_frame.pack(expand=True, fill=tk.BOTH, pady=5)
    
    # Listbox para mostrar archivos y carpetas
    listbox = tk.Listbox(
        lista_frame,
        height=15,
        font=('Courier', 10),
        selectmode=tk.SINGLE
    )
    
    # Scrollbar vertical para la lista
    scrollbar = ttk.Scrollbar(
        lista_frame,
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
    
    def actualizar_lista():
        """
        Actualiza el contenido del listbox con los archivos y carpetas
        del directorio actual.
        
        Esta función:
        1. Limpia la lista actual
        2. Lee el contenido del directorio
        3. Ordena los elementos alfabéticamente
        4. Distingue entre carpetas (con prefijo [CARPETA]) y archivos
        5. Maneja errores de permisos y otros problemas
        
        Returns:
            None
        """
        try:
            # Obtener la ruta actual
            ruta = ruta_actual_var.get()
            
            # Cambiar al directorio (asegura que estamos en la ruta correcta)
            os.chdir(ruta)
            
            # Limpiar el listbox
            listbox.delete(0, tk.END)
            
            # Obtener la lista de elementos en el directorio
            items = os.listdir(ruta)
            
            # Si el directorio está vacío, mostrar mensaje
            if not items:
                listbox.insert(tk.END, "[Carpeta vacía]")
                return
            
            # Ordenar elementos alfabéticamente (sin distinguir mayúsculas)
            items_ordenados = sorted(items, key=lambda s: s.lower())
            
            # Insertar elementos en el listbox
            for item in items_ordenados:
                ruta_completa = os.path.join(ruta, item)
                
                # Distinguir entre carpetas y archivos
                if os.path.isdir(ruta_completa):
                    listbox.insert(tk.END, f"📁 [CARPETA] {item}")
                else:
                    listbox.insert(tk.END, f"📄 {item}")
                    
        except PermissionError:
            # Error de permisos denegados
            listbox.delete(0, tk.END)
            listbox.insert(tk.END, "❌ [Error: Permiso denegado]")
            messagebox.showwarning(
                "Permiso Denegado",
                "No tienes permisos para acceder a este directorio.",
                parent=explorador_win
            )
            
        except Exception as e:
            # Otros errores
            messagebox.showerror(
                "Error",
                f"No se pudo leer el directorio:\n{e}",
                parent=explorador_win
            )
            # Intentar volver al directorio anterior
            subir_nivel()
    
    def subir_nivel():
        """
        Sube un nivel en la jerarquía de directorios.
        
        Esta función navega al directorio padre del directorio actual
        y actualiza la vista.
        
        Returns:
            None
        """
        # Obtener el directorio padre
        ruta_actual = ruta_actual_var.get()
        nueva_ruta = os.path.abspath(os.path.join(ruta_actual, '..'))
        
        # Actualizar la variable de ruta
        ruta_actual_var.set(nueva_ruta)
        
        # Actualizar la lista
        actualizar_lista()
    
    def navegar(event):
        """
        Maneja el evento de doble clic en un elemento de la lista.
        
        Si el elemento es una carpeta, navega hacia ella.
        Si es un archivo, no hace nada (se podría extender para abrirlo).
        
        Args:
            event: Evento de Tkinter (doble clic)
        
        Returns:
            None
        """
        try:
            # Obtener el elemento seleccionado
            seleccion = listbox.get(listbox.curselection())
            
            # Ignorar si es el mensaje de carpeta vacía o error
            if seleccion.startswith("[Carpeta vacía]") or seleccion.startswith("❌"):
                return
            
            # Limpiar el prefijo de carpeta si existe
            if "[CARPETA]" in seleccion:
                # Remover el emoji y el prefijo [CARPETA]
                seleccion = seleccion.split("[CARPETA]")[1].strip()
            elif seleccion.startswith("📁"):
                seleccion = seleccion[2:].strip()
            elif seleccion.startswith("📄"):
                # Es un archivo, no hacer nada
                messagebox.showinfo(
                    "Archivo",
                    "Has seleccionado un archivo. En esta versión solo se puede navegar por carpetas.",
                    parent=explorador_win
                )
                return
            
            # Construir la nueva ruta
            nueva_ruta = os.path.join(ruta_actual_var.get(), seleccion)
            
            # Verificar si es un directorio
            if os.path.isdir(nueva_ruta):
                ruta_actual_var.set(nueva_ruta)
                actualizar_lista()
                
        except tk.TclError:
            # No hay selección
            pass
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al navegar:\n{e}",
                parent=explorador_win
            )
    
    def cerrar_ventana():
        """
        Cierra la ventana del explorador de archivos.
        
        Esta función se ejecuta cuando el usuario hace clic en el botón
        de retroceso.
        
        Returns:
            None
        """
        explorador_win.destroy()
    
    # =============================================================================
    # CONFIGURACIÓN DE EVENTOS
    # =============================================================================
    
    # Vincular doble clic a la función de navegación
    listbox.bind("<Double-1>", navegar)
    
    # =============================================================================
    # CREACIÓN DE BOTONES DE CONTROL
    # =============================================================================
    
    # Botón: Refrescar
    btn_refrescar = ttk.Button(
        btn_frame,
        text="🔄 Refrescar",
        command=actualizar_lista
    )
    btn_refrescar.pack(side=tk.LEFT, padx=5)
    
    # Botón: Subir Nivel
    btn_subir = ttk.Button(
        btn_frame,
        text="⬆️ Subir Nivel (..)",
        command=subir_nivel
    )
    btn_subir.pack(side=tk.LEFT, padx=5)
    
    # Botón: Retroceder (NUEVO)
    btn_retroceder = ttk.Button(
        btn_frame,
        text="⬅️ Retroceder",
        command=cerrar_ventana
    )
    btn_retroceder.pack(side=tk.RIGHT, padx=5)
    
    # =============================================================================
    # INICIALIZACIÓN
    # =============================================================================
    
    # Cargar la lista inicial de archivos
    actualizar_lista()
    
    # Información de ayuda en la barra de estado
    barra_estado = ttk.Label(
        frame,
        text=" Doble clic en una carpeta para navegar | Usa 'Subir Nivel' para retroceder",
        relief=tk.SUNKEN,
        padding=5,
        font=('Arial', 8)
    )
    barra_estado.pack(fill=tk.X, pady=(5, 0))
