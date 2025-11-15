import tkinter as tk
from tkinter import ttk, scrolledtext
import platform
import getpass
import psutil # pyright: ignore[reportMissingModuleSource]
import os
from datetime import datetime
from .estilo import aplicar_gradiente_y_contenido

# =============================================================================
# FUNCIÓN PRINCIPAL DEL MÓDULO
# =============================================================================

def abrir_info_sistema(ventana_padre):
    """
    Crea y muestra la ventana de información del sistema.
    
    Esta función genera una ventana secundaria (Toplevel) que muestra
    información detallada sobre el sistema operativo y los recursos del equipo.
    
    Args:
        ventana_padre (tk.Tk): La ventana principal de la aplicación
    
    Returns:
        None
    """
    
    # =============================================================================
    # CONFIGURACIÓN DE LA VENTANA
    # =============================================================================
    
    info_win = tk.Toplevel(ventana_padre)
    info_win.title("Información del Sistema")
    info_win.geometry("650x600")
    info_win.resizable(True, True)
    
    # Aplicar fondo gradiente (azul a negro)
    canvas_fondo, frame_grad, mid_color = aplicar_gradiente_y_contenido(info_win, "#44B3EB", "#000000")

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
        text="Información del Sistema",
        font=('Arial', 14, 'bold')
    )
    titulo.pack()
    
    descripcion = ttk.Label(
        titulo_frame,
        text="Detalles completos sobre tu sistema operativo y hardware",
        font=('Arial', 9),
        foreground='gray'
    )
    descripcion.pack()
    
    # =============================================================================
    # SECCIÓN: ÁREA DE INFORMACIÓN
    # =============================================================================
    
    # ScrolledText para mostrar la información
    txt_info = scrolledtext.ScrolledText(
        frame,
        wrap=tk.WORD,
        state=tk.DISABLED,
        font=('Courier', 9),
        bg='#f8f9fa',
        fg='#212529'
    )
    txt_info.pack(expand=True, fill=tk.BOTH, pady=10)
    
    # =============================================================================
    # FUNCIONES AUXILIARES
    # =============================================================================
    
    def bytes_a_gb(bytes_valor):
        """
        Convierte bytes a gigabytes.
        
        Args:
            bytes_valor (int): Valor en bytes
        
        Returns:
            float: Valor en gigabytes con 2 decimales
        """
        return round(bytes_valor / (1024**3), 2)
    
    def obtener_tiempo_actividad():
        """
        Obtiene el tiempo de actividad del sistema.
        
        Returns:
            str: Tiempo de actividad formateado
        """
        try:
            boot_time = psutil.boot_time()
            boot_datetime = datetime.fromtimestamp(boot_time)
            ahora = datetime.now()
            tiempo_activo = ahora - boot_datetime
            
            dias = tiempo_activo.days
            horas, resto = divmod(tiempo_activo.seconds, 3600)
            minutos, segundos = divmod(resto, 60)
            
            return f"{dias} días, {horas} horas, {minutos} minutos"
        except:
            return "No disponible"
    
    def recopilar_informacion():
        """
        Recopila toda la información del sistema.
        
        Returns:
            str: Cadena con toda la información formateada
        """
        info_str = ""
        
        # =============================================================================
        # SECCIÓN 1: INFORMACIÓN DEL USUARIO
        # =============================================================================
        
        info_str += "╔" + "═" * 60 + "╗\n"
        info_str += "║" + " " * 18 + "INFORMACIÓN DEL USUARIO" + " " * 19 + "║\n"
        info_str += "╚" + "═" * 60 + "╝\n\n"
        
        try:
            usuario = getpass.getuser()
            info_str += f" Usuario Actual: {usuario}\n"
        except Exception:
            info_str += " Usuario Actual: No disponible\n"
        
        try:
            info_str += f" Directorio Home: {os.path.expanduser('~')}\n"
        except Exception:
            info_str += " Directorio Home: No disponible\n"
        
        info_str += "\n"
        
        # =============================================================================
        # SECCIÓN 2: SISTEMA OPERATIVO
        # =============================================================================
        
        info_str += "╔" + "═" * 60 + "╗\n"
        info_str += "║" + " " * 18 + "SISTEMA OPERATIVO" + " " * 23 + "║\n"
        info_str += "╚" + "═" * 60 + "╝\n\n"
        
        info_str += f" Sistema: {platform.system()}\n"
        info_str += f" Nombre del Sistema: {platform.node()}\n"
        info_str += f" Release: {platform.release()}\n"
        info_str += f" Versión: {platform.version()}\n"
        info_str += f" Arquitectura: {platform.machine()}\n"
        info_str += f" Tiempo de Actividad: {obtener_tiempo_actividad()}\n"
        
        info_str += "\n"
        
        # =============================================================================
        # SECCIÓN 3: PROCESADOR
        # =============================================================================
        
        info_str += "╔" + "═" * 60 + "╗\n"
        info_str += "║" + " " * 22 + "PROCESADOR" + " " * 27 + "║\n"
        info_str += "╚" + "═" * 60 + "╝\n\n"
        
        info_str += f" Procesador: {platform.processor()}\n"
        
        try:
            info_str += f" Núcleos Físicos: {psutil.cpu_count(logical=False)}\n"
            info_str += f" Núcleos Lógicos: {psutil.cpu_count(logical=True)}\n"
            info_str += f" Uso de CPU: {psutil.cpu_percent(interval=1)}%\n"
            
            # Frecuencia del CPU
            freq = psutil.cpu_freq()
            if freq:
                info_str += f" Frecuencia Actual: {freq.current:.2f} MHz\n"
                info_str += f" Frecuencia Máxima: {freq.max:.2f} MHz\n"
        except Exception as e:
            info_str += f" No se pudo obtener información del CPU: {e}\n"
        
        info_str += "\n"
        
        # =============================================================================
        # SECCIÓN 4: MEMORIA RAM
        # =============================================================================
        
        info_str += "╔" + "═" * 60 + "╗\n"
        info_str += "║" + " " * 22 + "MEMORIA RAM" + " " * 26 + "║\n"
        info_str += "╚" + "═" * 60 + "╝\n\n"
        
        try:
            memoria = psutil.virtual_memory()
            
            info_str += f" Total: {bytes_a_gb(memoria.total)} GB\n"
            info_str += f" Disponible: {bytes_a_gb(memoria.available)} GB\n"
            info_str += f" Usado: {bytes_a_gb(memoria.used)} GB\n"
            info_str += f" Porcentaje Usado: {memoria.percent}%\n"
            
            # Barra de progreso visual
            barra_longitud = 40
            usado_barra = int((memoria.percent / 100) * barra_longitud)
            libre_barra = barra_longitud - usado_barra
            barra = "█" * usado_barra + "░" * libre_barra
            info_str += f" [{barra}] {memoria.percent}%\n"
            
        except Exception as e:
            info_str += f" No se pudo obtener información de memoria: {e}\n"
        
        info_str += "\n"
        
        # =============================================================================
        # SECCIÓN 5: ESPACIO EN DISCO
        # =============================================================================
        
        info_str += "╔" + "═" * 60 + "╗\n"
        info_str += "║" + " " * 20 + "ESPACIO EN DISCO" + " " * 23 + "║\n"
        info_str += "╚" + "═" * 60 + "╝\n\n"
        
        try:
            # Obtener todas las particiones
            particiones = psutil.disk_partitions()
            
            for particion in particiones:
                try:
                    uso = psutil.disk_usage(particion.mountpoint)
                    
                    info_str += f" Partición: {particion.device}\n"
                    info_str += f"   Punto de Montaje: {particion.mountpoint}\n"
                    info_str += f"   Sistema de Archivos: {particion.fstype}\n"
                    info_str += f"   Total: {bytes_a_gb(uso.total)} GB\n"
                    info_str += f"   Usado: {bytes_a_gb(uso.used)} GB\n"
                    info_str += f"   Disponible: {bytes_a_gb(uso.free)} GB\n"
                    info_str += f"   Porcentaje Usado: {uso.percent}%\n"
                    
                    # Barra de progreso visual
                    barra_longitud = 40
                    usado_barra = int((uso.percent / 100) * barra_longitud)
                    libre_barra = barra_longitud - usado_barra
                    barra = "█" * usado_barra + "░" * libre_barra
                    info_str += f"   [{barra}] {uso.percent}%\n\n"
                    
                except PermissionError:
                    info_str += f" Partición: {particion.device}\n"
                    info_str += f"   Permiso denegado\n\n"
                except Exception:
                    continue
                    
        except Exception as e:
            info_str += f" No se pudo obtener información del disco: {e}\n"
        
        # =============================================================================
        # SECCIÓN 6: RED
        # =============================================================================
        
        info_str += "╔" + "═" * 60 + "╗\n"
        info_str += "║" + " " * 25 + "RED" + " " * 32 + "║\n"
        info_str += "╚" + "═" * 60 + "╝\n\n"
        
        try:
            # Obtener información de red
            info_red = psutil.net_if_addrs()
            
            for interfaz, direcciones in info_red.items():
                info_str += f" Interfaz: {interfaz}\n"
                for direccion in direcciones:
                    if direccion.family == 2:  # IPv4
                        info_str += f"   IPv4: {direccion.address}\n"
                    elif direccion.family == 23:  # IPv6
                        info_str += f"   IPv6: {direccion.address}\n"
                info_str += "\n"
                
        except Exception as e:
            info_str += f" No se pudo obtener información de red: {e}\n"
        
        # =============================================================================
        # PIE DE PÁGINA
        # =============================================================================
        
        info_str += "\n" + "═" * 62 + "\n"
        info_str += f"Información generada el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        info_str += "═" * 62 + "\n"
        
        return info_str
    
    def actualizar_informacion():
        """
        Actualiza la información mostrada en el área de texto.
        
        Returns:
            None
        """
        # Mostrar mensaje de carga
        txt_info.config(state=tk.NORMAL)
        txt_info.delete(1.0, tk.END)
        txt_info.insert(tk.END, " Recopilando información del sistema...\n")
        txt_info.config(state=tk.DISABLED)
        txt_info.update()
        
        # Recopilar información
        info_completa = recopilar_informacion()
        
        # Mostrar información
        txt_info.config(state=tk.NORMAL)
        txt_info.delete(1.0, tk.END)
        txt_info.insert(tk.END, info_completa)
        txt_info.config(state=tk.DISABLED)
    
    def cerrar_ventana():
        """
        Cierra la ventana de información del sistema.
        
        Esta función se ejecuta cuando el usuario hace clic en el botón
        de retroceso.
        
        Returns:
            None
        """
        info_win.destroy()
    
    # =============================================================================
    # SECCIÓN: BOTONES DE CONTROL
    # =============================================================================
    
    botones_frame = ttk.Frame(frame)
    botones_frame.pack(fill=tk.X, pady=10)
    
    # Botón: Actualizar Información
    btn_actualizar = ttk.Button(
        botones_frame,
        text=" Actualizar Información",
        command=actualizar_informacion
    )
    btn_actualizar.pack(side=tk.LEFT, padx=5)
    
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
    
    # Cargar la información inicial
    actualizar_informacion()
