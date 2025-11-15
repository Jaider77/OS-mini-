import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter # pyright: ignore[reportMissingImports]
import os

# =============================================================================
# IMPORTACIÓN DE MÓDULOS PERSONALIZADOS
# =============================================================================
# Gracias a __init__.py, podemos importar desde la carpeta 'modulos'
from modulos.mod_explorador import abrir_explorador
from modulos.mod_procesos import abrir_gestion_procesos
from modulos.mod_shell import abrir_shell
from modulos.mod_info import abrir_info_sistema

# =============================================================================
# CONFIGURACIÓN DE LA VENTANA PRINCIPAL
# =============================================================================

def crear_ventana_principal(color1="#44B3EB", color2="#000000", ancho=550, alto=550):
    """
    Crea y configura la ventana principal de la aplicación.
    
    Esta función inicializa la ventana raíz con todos sus componentes,
    incluyendo los botones con imágenes para acceder a cada módulo.
    
    Returns:
        tk.Tk: La ventana principal de la aplicación
    """
    
    # 1. Crear la ventana raíz
    root = tk.Tk()
    root.title("Mini Sistema Operativo")  # Título de la ventana
    root.geometry(f"{ancho}x{alto}")  # Tamaño ajustado para botones con imagen
    root.resizable(False, False)  # Evitar redimensionamiento

    # Crear un canvas que servirá como fondo donde dibujaremos el gradiente
    canvas = tk.Canvas(root, width=ancho, height=alto, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Dibujar gradiente vertical de color1 a color2 (línea por línea)
    try:
        r1, g1, b1 = root.winfo_rgb(color1)
        r2, g2, b2 = root.winfo_rgb(color2)
        for i in range(alto):
            r = int(r1 + (r2 - r1) * i / max(1, alto)) >> 8
            g = int(g1 + (g2 - g1) * i / max(1, alto)) >> 8
            b = int(b1 + (b2 - b1) * i / max(1, alto)) >> 8
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, ancho, i, fill=color)
    except Exception:
        # En caso de fallo al dibujar el gradiente, usar color de fondo sólido
        canvas.configure(bg=color1)

    # No usamos un frame opaco: dibujaremos todo sobre el canvas para
    # que el gradiente de fondo sea visible en toda la ventana.
    # Dibujar título y subtítulo directamente en el canvas (parte superior)
    banner_alto = 140
    canvas.create_text(ancho/2, 40, text="Mini Sistema Operativo",
                       font=('Arial', 18, 'bold'), fill='#ffffff')
    canvas.create_text(ancho/2, 80, text="Selecciona un módulo para comenzar",
                       font=('Arial', 10), fill='#dfeefb')
    
    # =============================================================================
    # CARGA DE IMÁGENES PARA LOS BOTONES
    # =============================================================================
    
    # Obtener la ruta del directorio de imágenes
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    directorio_imagenes = os.path.join(directorio_actual, "imagenes")
    
    # Diccionario para almacenar las imágenes cargadas
    imagenes = {}
    
    # Lista de módulos con sus configuraciones
    modulos = [
        {
            "nombre": "explorador",
            "titulo": "Explorador de Archivos",
            "descripcion": "Navega por el sistema de archivos",
            "comando": lambda: abrir_explorador(root)
        },
        {
            "nombre": "procesos",
            "titulo": "Gestión de Procesos",
            "descripcion": "Administra los procesos del sistema",
            "comando": lambda: abrir_gestion_procesos(root)
        },
        {
            "nombre": "shell",
            "titulo": "Shell Educativa",
            "descripcion": "Ejecuta comandos básicos del sistema",
            "comando": lambda: abrir_shell(root)
        },
        {
            "nombre": "info",
            "titulo": "Información del Sistema",
            "descripcion": "Visualiza datos del sistema",
            "comando": lambda: abrir_info_sistema(root)
        }
    ]
    
    # Cargar y redimensionar las imágenes
    tamaño_imagen = (64, 64)  # Tamaño de las imágenes en los botones

    # --- Función auxiliar: crear fondo de tarjeta con sombra (PIL) ---
    def crear_fondo_tarjeta(w, h, radius=12, shadow=6):
        # Imagen RGBA transparente
        img = Image.new('RGBA', (w + shadow, h + shadow), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Parámetros de colores
        fill = (255, 255, 255, 230)  # blanco semitransparente
        shadow_color = (0, 0, 0, 90)

        # Dibujar sombra (recta desplazada)
        shadow_box = (shadow, shadow, w + shadow, h + shadow)
        draw.rounded_rectangle(shadow_box, radius=radius, fill=shadow_color)

        # Difuminar sombra
        img = img.filter(ImageFilter.GaussianBlur(radius=shadow//2))

        # Dibujar tarjeta encima
        draw = ImageDraw.Draw(img)
        card_box = (0, 0, w, h)
        draw.rounded_rectangle(card_box, radius=radius, fill=fill)

        return img

    # Preparar tamaños de tarjeta según ancho de ventana
    card_padding_x = 40 # Mayor padding = tarjetas más estrechas y centradas
    card_width = max(150, ancho - 2 * card_padding_x)
    card_height = 70

    # Crear fondos de tarjeta para cada módulo
    for idx, modulo in enumerate(modulos):
        try:
            ruta_imagen = os.path.join(directorio_imagenes, f"{modulo['nombre']}.png")
            imagen_original = Image.open(ruta_imagen)
            imagen_redimensionada = imagen_original.resize(tamaño_imagen, Image.LANCZOS)
            imagenes[modulo['nombre']] = ImageTk.PhotoImage(imagen_redimensionada)
        except Exception as e:
            print(f"Error al cargar imagen {modulo['nombre']}: {e}")
            # Si falla la carga, se usará None y el botón se creará sin imagen
            imagenes[modulo['nombre']] = None
        # Generar fondo de tarjeta y guardarlo también
        try:
            bg_img = crear_fondo_tarjeta(card_width, card_height, radius=12, shadow=8)
            imagenes[f"card_{idx}"] = ImageTk.PhotoImage(bg_img)
        except Exception as e:
            print(f"Error al crear fondo de tarjeta para {modulo['nombre']}: {e}")
    
    # =============================================================================
    # CREACIÓN DE BOTONES CON IMÁGENES
    # =============================================================================
    
    def crear_boton_modulo(modulo_info, idx, y_pos):
        """
        Crea un botón personalizado con imagen y texto para un módulo.
        
        Args:
            modulo_info (dict): Diccionario con la información del módulo
        
        Returns:
            tk.Frame: Frame contenedor del botón personalizado
        """
        
        # Canvas que representará la tarjeta (fondo + contenido dibujado encima)
        # Posición horizontal (izquierda) para la tarjeta
        x_left = card_padding_x

        tag = f"card_{idx}"

        # Dibujar imagen de fondo de la tarjeta en el canvas principal
        card_bg = imagenes.get(f"card_{idx}")
        if card_bg:
            canvas.create_image(x_left, y_pos, anchor='nw', image=card_bg, tags=(tag,))

        # Dibujar icono si existe
        icon = imagenes.get(modulo_info['nombre'])
        icon_x = x_left + 20
        icon_y = y_pos + card_height / 2
        if icon:
            canvas.create_image(icon_x, icon_y, anchor='w', image=icon, tags=(tag,))

        # Textos: título y descripción
        text_x = x_left + 100
        canvas.create_text(text_x, y_pos + card_height/2 - 8, anchor='w', text=modulo_info['titulo'],
                           font=('Arial', 12, 'bold'), fill='#2c3e50', tags=(tag,))
        canvas.create_text(text_x, y_pos + card_height/2 + 12, anchor='w', text=modulo_info['descripcion'],
                           font=('Arial', 9), fill='#7f8c8d', tags=(tag,))

        # Eventos: clic y hover (se aplican a todos los elementos de la tarjeta via tag)
        def on_click(event, cmd=modulo_info['comando']):
            try:
                cmd()
            except Exception as e:
                print(f"Error al ejecutar comando del módulo: {e}")

        canvas.tag_bind(tag, '<Button-1>', on_click)
        canvas.tag_bind(tag, '<Enter>', lambda e: canvas.config(cursor='hand2'))
        canvas.tag_bind(tag, '<Leave>', lambda e: canvas.config(cursor=''))

        return None
    
    # Crear los botones (tarjetas) para cada módulo directamente sobre el canvas
    y_start = banner_alto + 20
    spacing = 20
    for idx, modulo in enumerate(modulos):
        y = y_start + idx * (card_height + spacing)
        crear_boton_modulo(modulo, idx, y)
    
    # =============================================================================
    # PIE DE PÁGINA
    # =============================================================================
    
    # Pie de página dibujado en el canvas
    canvas.create_text(ancho/2, alto - 12, text="© 2025 - Mini Sistema Operativo v2.0",
                       font=('Arial', 8), fill="#d1e7e9")
    
    # Mantener una referencia a las imágenes en el objeto root para
    # evitar que el recolector de basura elimine los PhotoImage y las
    # etiquetas se queden sin imagen.
    root._imagenes = imagenes

    return root

# =============================================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# =============================================================================

if __name__ == "__main__":
    """
    Punto de entrada principal de la aplicación.
    
    Este bloque se ejecuta solo cuando el archivo se ejecuta directamente,
    no cuando se importa como módulo.
    """
    
    # Crear y mostrar la ventana principal
    ventana_principal = crear_ventana_principal()
    
    # Iniciar el bucle principal de eventos de Tkinter
    ventana_principal.mainloop()
