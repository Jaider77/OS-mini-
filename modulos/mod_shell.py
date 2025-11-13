# modulos/mod_shell.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import os
from .estilo import aplicar_gradiente_y_contenido

# =============================================================================
# FUNCIÓN PRINCIPAL DEL MÓDULO
# =============================================================================

def abrir_shell(ventana_padre):
    """
    Crea y muestra la ventana de la shell educativa.
    
    Esta función genera una ventana secundaria (Toplevel) que simula una
    terminal donde el usuario puede ejecutar comandos básicos del sistema.
    
    Args:
        ventana_padre (tk.Tk): La ventana principal de la aplicación
    
    Returns:
        None
    """
    
    # =============================================================================
    # CONFIGURACIÓN DE LA VENTANA
    # =============================================================================
    
    shell_win = tk.Toplevel(ventana_padre)
    shell_win.title("Shell Educativa")
    shell_win.geometry("700x550")
    shell_win.resizable(True, True)
    
    # Aplicar fondo gradiente (azul a negro)
    canvas_fondo, frame_container, mid_color = aplicar_gradiente_y_contenido(shell_win, "#44B3EB", "#000000")

    # Usar un frame tk con el color medio como fondo para que no tape el gradiente
    frame = tk.Frame(frame_container, bg=mid_color)
    frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    # =============================================================================
    # SECCIÓN: TÍTULO Y DESCRIPCIÓN
    # =============================================================================
    
    titulo_frame = ttk.Frame(frame)
    titulo_frame.pack(fill=tk.X, pady=(0, 10))
    
    titulo = ttk.Label(
        titulo_frame,
        text="Shell Educativa - Terminal de Comandos",
        font=('Arial', 14, 'bold')
    )
    titulo.pack()
    
    descripcion = ttk.Label(
        titulo_frame,
        text="Ejecuta comandos básicos del sistema de forma segura",
        font=('Arial', 9),
        foreground='gray'
    )
    descripcion.pack()
    
    # =============================================================================
    # SECCIÓN: ÁREA DE SALIDA DE COMANDOS
    # =============================================================================
    
    # Label para el área de salida
    lbl_output = ttk.Label(frame, text="Salida de Comandos:", font=('Arial', 10, 'bold'))
    lbl_output.pack(anchor='w', pady=(5, 2))
    
    # ScrolledText para mostrar la salida de los comandos
    txt_output = scrolledtext.ScrolledText(
        frame,
        wrap=tk.WORD,
        height=15,
        state=tk.DISABLED,
        font=('Courier', 9),
        bg='#1e1e1e',  # Fondo oscuro estilo terminal
        fg='#00ff00',  # Texto verde estilo terminal
        insertbackground='white'
    )
    txt_output.pack(expand=True, fill=tk.BOTH, pady=5)
    
    # =============================================================================
    # SECCIÓN: ENTRADA DE COMANDOS
    # =============================================================================
    
    # Frame para la entrada de comandos
    input_frame = ttk.LabelFrame(frame, text="Entrada de Comando", padding="10")
    input_frame.pack(fill=tk.X, pady=10)
    
    # Frame interno para organizar los widgets
    entrada_interna = ttk.Frame(input_frame)
    entrada_interna.pack(fill=tk.X)
    
    # Label del prompt
    lbl_prompt = ttk.Label(
        entrada_interna,
        text="$",
        font=('Courier', 11, 'bold'),
        foreground='green'
    )
    lbl_prompt.pack(side=tk.LEFT, padx=(0, 5))
    
    # Entry para ingresar comandos
    entry_cmd = ttk.Entry(entrada_interna, font=('Courier', 10))
    entry_cmd.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=5)
    
    # Botón para ejecutar el comando
    btn_ejecutar = ttk.Button(
        entrada_interna,
        text="▶️ Ejecutar",
        command=lambda: ejecutar_comando()
    )
    btn_ejecutar.pack(side=tk.RIGHT, padx=5)
    
    # =============================================================================
    # SECCIÓN: INFORMACIÓN DE COMANDOS PERMITIDOS
    # =============================================================================
    
    info_frame = ttk.Frame(frame)
    info_frame.pack(fill=tk.X, pady=5)
    
    info_comandos = ttk.Label(
        info_frame,
        text="📋 Comandos permitidos: ls, dir, pwd, echo",
        font=('Arial', 9),
        foreground='blue',
        background='#e7f3ff',
        relief=tk.SOLID,
        padding=5
    )
    info_comandos.pack(fill=tk.X)
    
    # =============================================================================
    # VARIABLES GLOBALES DEL MÓDULO
    # =============================================================================
    
    # Historial de comandos
    historial_comandos = []
    indice_historial = -1
    
    # Lista de comandos permitidos
    COMANDOS_VALIDOS = ['ls', 'dir', 'pwd', 'echo', 'cd', 'clear']
    
    # =============================================================================
    # FUNCIONES INTERNAS DEL MÓDULO
    # =============================================================================
    
    def escribir_salida(texto, color='#00ff00'):
        """
        Escribe texto en el área de salida con formato.
        
        Args:
            texto (str): El texto a escribir
            color (str): Color del texto en formato hexadecimal
        
        Returns:
            None
        """
        txt_output.config(state=tk.NORMAL)
        txt_output.insert(tk.END, texto)
        txt_output.config(state=tk.DISABLED)
        txt_output.see(tk.END)  # Hacer scroll hasta el final
    
    def limpiar_salida():
        """
        Limpia el área de salida de comandos.
        
        Returns:
            None
        """
        txt_output.config(state=tk.NORMAL)
        txt_output.delete(1.0, tk.END)
        txt_output.config(state=tk.DISABLED)
    
    def ejecutar_comando():
        """
        Ejecuta el comando ingresado por el usuario.
        
        Esta función:
        1. Obtiene el comando del campo de entrada
        2. Valida que el comando esté en la lista de permitidos
        3. Ejecuta el comando usando subprocess
        4. Muestra la salida en el área de texto
        5. Maneja errores y comandos no permitidos
        
        Returns:
            None
        """
        nonlocal indice_historial
        
        # Obtener el comando ingresado
        comando_str = entry_cmd.get().strip()
        
        # Validar que no esté vacío
        if not comando_str:
            return
        
        # Agregar al historial
        historial_comandos.append(comando_str)
        indice_historial = len(historial_comandos)
        
        # Extraer el comando base (primera palabra)
        comando_base = comando_str.split()[0].lower()
        
        # Comando especial: clear (limpiar pantalla)
        if comando_base == 'clear':
            limpiar_salida()
            entry_cmd.delete(0, tk.END)
            escribir_salida("Pantalla limpiada.\n\n")
            return
        
        # Validar contra la lista de comandos permitidos
        if comando_base not in COMANDOS_VALIDOS:
            escribir_salida(f"\n$ {comando_str}\n")
            escribir_salida(
                f"❌ ERROR: Comando '{comando_base}' no permitido en esta shell educativa.\n"
                f"💡 Comandos disponibles: {', '.join(COMANDOS_VALIDOS)}\n\n"
            )
            entry_cmd.delete(0, tk.END)
            return
        
        # Mostrar el comando ejecutado
        escribir_salida(f"\n$ {comando_str}\n")
        escribir_salida("-" * 60 + "\n")
        
        try:
            # Ejecutar el comando
            # Nota: Usamos shell=True para comandos como 'dir' y 'echo' en Windows
            resultado = subprocess.run(
                comando_str,
                capture_output=True,
                text=True,
                shell=True,
                encoding='utf-8',
                errors='ignore',
                timeout=10  # Timeout de 10 segundos
            )
            
            # Obtener la salida estándar y de error
            salida = resultado.stdout
            error = resultado.stderr
            
            # Mostrar la salida
            if salida:
                escribir_salida(salida)
            
            # Mostrar errores si existen
            if error:
                escribir_salida(f"\n⚠️ ADVERTENCIA/ERROR:\n{error}\n")
            
            # Si no hay salida ni error
            if not salida and not error:
                escribir_salida("✅ Comando ejecutado correctamente (sin salida).\n")
            
            escribir_salida("-" * 60 + "\n")
            
        except subprocess.TimeoutExpired:
            escribir_salida("❌ ERROR: El comando excedió el tiempo límite de ejecución.\n")
            escribir_salida("-" * 60 + "\n")
            
        except Exception as e:
            escribir_salida(f"❌ ERROR al ejecutar el comando:\n{e}\n")
            escribir_salida("-" * 60 + "\n")
        
        # Limpiar el campo de entrada
        entry_cmd.delete(0, tk.END)
    
    def navegar_historial(event):
        """
        Navega por el historial de comandos usando las flechas arriba/abajo.
        
        Args:
            event: Evento de teclado
        
        Returns:
            None
        """
        nonlocal indice_historial
        
        if not historial_comandos:
            return
        
        # Flecha arriba: comando anterior
        if event.keysym == 'Up':
            if indice_historial > 0:
                indice_historial -= 1
                entry_cmd.delete(0, tk.END)
                entry_cmd.insert(0, historial_comandos[indice_historial])
        
        # Flecha abajo: comando siguiente
        elif event.keysym == 'Down':
            if indice_historial < len(historial_comandos) - 1:
                indice_historial += 1
                entry_cmd.delete(0, tk.END)
                entry_cmd.insert(0, historial_comandos[indice_historial])
            else:
                indice_historial = len(historial_comandos)
                entry_cmd.delete(0, tk.END)
    
    def cerrar_ventana():
        """
        Cierra la ventana de la shell educativa.
        
        Esta función se ejecuta cuando el usuario hace clic en el botón
        de retroceso.
        
        Returns:
            None
        """
        shell_win.destroy()
    
    # =============================================================================
    # CONFIGURACIÓN DE EVENTOS
    # =============================================================================
    
    # Vincular la tecla Enter para ejecutar comandos
    entry_cmd.bind("<Return>", lambda event: ejecutar_comando())
    
    # Vincular las flechas arriba/abajo para navegar por el historial
    entry_cmd.bind("<Up>", navegar_historial)
    entry_cmd.bind("<Down>", navegar_historial)
    
    # =============================================================================
    # SECCIÓN: BOTONES DE CONTROL
    # =============================================================================
    
    botones_frame = ttk.Frame(frame)
    botones_frame.pack(fill=tk.X, pady=5)
    
    # Botón: Limpiar Pantalla
    btn_limpiar = ttk.Button(
        botones_frame,
        text="🗑️ Limpiar Pantalla",
        command=limpiar_salida
    )
    btn_limpiar.pack(side=tk.LEFT, padx=5)
    
    # Botón: Ayuda
    def mostrar_ayuda():
        ayuda_texto = """
COMANDOS DISPONIBLES EN LA SHELL EDUCATIVA:

• ls / dir: Lista los archivos y carpetas del directorio actual
• pwd: Muestra la ruta del directorio actual
• echo [texto]: Imprime el texto especificado
• clear: Limpia la pantalla de la terminal

ATAJOS DE TECLADO:
• Enter: Ejecutar comando
• Flecha Arriba/Abajo: Navegar por el historial de comandos

NOTAS:
- Esta es una shell educativa con comandos limitados por seguridad
- Los comandos se ejecutan en el contexto del sistema operativo actual
        """
        messagebox.showinfo("Ayuda - Shell Educativa", ayuda_texto, parent=shell_win)
    
    btn_ayuda = ttk.Button(
        botones_frame,
        text="❓ Ayuda",
        command=mostrar_ayuda
    )
    btn_ayuda.pack(side=tk.LEFT, padx=5)
    
    # Botón: Retroceder (NUEVO)
    btn_retroceder = ttk.Button(
        botones_frame,
        text="⬅️ Retroceder",
        command=cerrar_ventana
    )
    btn_retroceder.pack(side=tk.RIGHT, padx=5)
    
    # =============================================================================
    # INICIALIZACIÓN
    # =============================================================================
    
    # Mensaje de bienvenida
    mensaje_bienvenida = f"""
╔════════════════════════════════════════════════════════════╗
║          BIENVENIDO A LA SHELL EDUCATIVA v2.0              ║
╚════════════════════════════════════════════════════════════╝

Sistema Operativo: {os.name}
Directorio Actual: {os.getcwd()}

Escribe 'clear' para limpiar la pantalla o presiona el botón de Ayuda
para ver los comandos disponibles.

"""
    escribir_salida(mensaje_bienvenida)
    
    # Enfocar el campo de entrada
    entry_cmd.focus()
