import tkinter as tk


def aplicar_gradiente_fondo(ventana, color1="#44B3EB", color2="#000000"):
    """
    Aplica un fondo con gradiente vertical a una ventana (Toplevel o Tk).
    
    Args:
        ventana (tk.Tk o tk.Toplevel): La ventana a la que aplicar gradiente
        color1 (str): Color inicial (hex, por defecto azul)
        color2 (str): Color final (hex, por defecto negro)
    
    Returns:
        tk.Canvas: El canvas que contiene el gradiente (para dibujar encima si es necesario)
    """
    
    # Obtener dimensiones de la ventana
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    
    # Si las dimensiones no están disponibles, usar valores por defecto
    if ancho <= 1:
        ancho = 700
    if alto <= 1:
        alto = 550
    
    # Crear canvas para el gradiente
    canvas = tk.Canvas(ventana, width=ancho, height=alto, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
    
    # Dibujar gradiente vertical
    try:
        r1, g1, b1 = ventana.winfo_rgb(color1)
        r2, g2, b2 = ventana.winfo_rgb(color2)
        for i in range(alto):
            r = int(r1 + (r2 - r1) * i / max(1, alto)) >> 8
            g = int(g1 + (g2 - g1) * i / max(1, alto)) >> 8
            b = int(b1 + (b2 - b1) * i / max(1, alto)) >> 8
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, ancho, i, fill=color)
    except Exception as e:
        print(f"Error al dibujar gradiente: {e}")
        canvas.configure(bg=color1)
    
    return canvas


def aplicar_gradiente_y_contenido(ventana, color1="#44B3EB", color2="#000000"):
    """
    Aplica un fondo gradiente a una ventana y retorna un frame sobre él
    para colocar contenido de forma tradicional (pack/grid).
    
    Esta función es útil para módulos que usan frame + padding con empaquetado.
    
    Args:
        ventana (tk.Tk o tk.Toplevel): La ventana a la que aplicar gradiente
        color1 (str): Color inicial
        color2 (str): Color final
    
    Returns:
        tuple: (canvas_fondo, frame_contenido)
            - canvas_fondo: el canvas con el gradiente (por si necesitas dibujar encima)
            - frame_contenido: un frame transparente donde colocar widgets
    """
    
    # Obtener dimensiones
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    
    if ancho <= 1:
        ancho = 700
    if alto <= 1:
        alto = 550
    
    # Crear y dibujar canvas gradiente
    canvas = tk.Canvas(ventana, width=ancho, height=alto, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Dibujar gradiente
    try:
        r1, g1, b1 = ventana.winfo_rgb(color1)
        r2, g2, b2 = ventana.winfo_rgb(color2)
        for i in range(alto):
            r = int(r1 + (r2 - r1) * i / max(1, alto)) >> 8
            g = int(g1 + (g2 - g1) * i / max(1, alto)) >> 8
            b = int(b1 + (b2 - b1) * i / max(1, alto)) >> 8
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, ancho, i, fill=color)
    except Exception as e:
        print(f"Error al dibujar gradiente: {e}")
        canvas.configure(bg=color1)
    
    # Calcular color medio (aproximación) para usar como fondo de contenedores
    try:
        rm = (r1 + r2) // 2 >> 8
        gm = (g1 + g2) // 2 >> 8
        bm = (b1 + b2) // 2 >> 8
        mid_color = f'#{rm:02x}{gm:02x}{bm:02x}'
    except Exception:
        mid_color = color1

    # Crear un frame colocado sobre el canvas (usando place)
    # No existe transparencia real para widgets en Tkinter, así que usamos
    # un color medio para que el frame armonice con el gradiente.
    frame = tk.Frame(ventana, bg=mid_color)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    return canvas, frame, mid_color
