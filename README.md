# Mini Sistema Operativo v2

## 📋 Descripción

**Mini Sistema Operativo** es una aplicación de escritorio desarrollada en Python con Tkinter que simula las funcionalidades básicas de un sistema operativo. Esta versión 2.0 incluye mejoras significativas en la interfaz de usuario y funcionalidades adicionales.

## ✨ Características Principales

### 🖼️ Interfaz Mejorada
- **Botones con Imágenes**: La pantalla principal ahora utiliza botones visuales con iconos personalizados
- **Diseño Moderno**: Interfaz limpia y profesional con colores y tipografías mejoradas
- **Botones de Retroceso**: Todos los módulos incluyen un botón para volver al menú principal

### 📂 Módulos Disponibles

#### 1. **Explorador de Archivos**
- Navega por el sistema de archivos
- Visualiza carpetas y archivos
- Sube niveles en la jerarquía de directorios
 
Este proyecto es una aplicación de escritorio que simula funciones básicas de un "mini" sistema operativo mediante una interfaz gráfica creada con `tkinter`.

**Objetivo:** servir como práctica educativa para entender conceptos básicos de sistemas: explorador de archivos, gestión de procesos, shell limitada e información del sistema.

---

**Metadatos del paquete**

- Versión: `2.0` (definida en `modulos/__init__.py`)
- Autor: `jaider`

---

## Resumen de funcionalidades

- **Explorador de archivos** (`modulos/mod_explorador.py`)
   - Navegación por carpetas
   - Subir nivel y refrescar vista
   - Manejo de directorios vacíos y errores de permisos

- **Gestor de procesos** (`modulos/mod_procesos.py`)
   - Lista procesos activos (PID y nombre)
   - Finalizar procesos por PID (usa `psutil`)

- **Shell educativa** (`modulos/mod_shell.py`)
   - Ejecuta comandos permitidos: `ls`, `dir`, `pwd`, `echo`
   - Muestra salida y errores formateados

- **Información del sistema** (`modulos/mod_info.py`)
   - Usuario actual, datos del SO y uso de disco (usa `psutil`)

- **Estilos** (`modulos/estilo.py`)
   - Utilitarios para gradientes y frames de contenido

---

## Requisitos

- Python 3.8 o superior
- Dependencias Python (instalar mediante `pip`):
   - `psutil`

`tkinter` viene normalmente incluido en instalaciones estándar de Python en Windows; en algunas distribuciones Linux puede requerir paquetes adicionales (p. ej. `python3-tk`).

## Instalación y ejecución

1. Clona el repositorio y entra en la carpeta:

```powershell
git clone https://github.com/Jaider77/OS-mini-.git
cd "os_mini"
```

2. (Opcional, recomendado) crea y activa un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instala la dependencia necesaria:

```powershell
pip install psutil
```

4. Ejecuta la aplicación:

```powershell
python main.py
```

La ventana principal mostrará botones para abrir cada módulo en ventanas separadas.

---

## Notas de seguridad y limitaciones

- **Finalizar procesos:** terminar procesos puede requerir privilegios elevados y puede interrumpir servicios importantes. Usa la funcionalidad con precaución.
- **Shell educativa:** solo se permiten unos pocos comandos por diseño; la ejecución se realiza con `subprocess` y `shell=True` para simplicidad, así que evita introducir comandos no controlados.
- **Acceso a archivos:** el explorador no implementa operaciones destructivas (borrar/copiar/mover) — solo navegación — por seguridad y simplicidad.

## Estructura del proyecto

```
`main.py`                 # Punto de entrada de la app
`modulos/`                # Paquete con los módulos
   ├─ `__init__.py`        # Metadatos (versión / autor)
   ├─ `mod_explorador.py`  # Explorador de archivos
   ├─ `mod_procesos.py`    # Gestor de procesos (usa psutil)
   ├─ `mod_shell.py`       # Shell educativa
   ├─ `mod_info.py`        # Información del sistema (usa psutil)
   └─ `estilo.py`          # Utilidades de UI / gradientes
``


## Contribuciones

Abierto a PRs e issues. Describe cambios, pruebas realizadas y justificación.

## Licencia

Por defecto sugerida: MIT. Añade un archivo `LICENSE` si aún no existe.

---

Si quieres, puedo generar ya un `requirements.txt`, añadir confirmaciones antes de terminar procesos o crear un pequeño script de comprobación de dependencias. Dime qué prefieres y lo hago.

### Agregar Nuevos Comandos a la Shell

Edita el archivo `modulos/mod_shell.py`:

```python
# Línea 67: Agrega tu comando a la lista
COMANDOS_VALIDOS = ['ls', 'dir', 'pwd', 'echo', 'cd', 'clear', 'tu_comando']
```

### Personalizar Colores y Estilos

Los colores principales se definen en cada módulo. Busca las secciones de configuración:

```python
# Ejemplo en main.py
root.configure(bg='#f0f0f0')  # Color de fondo
```

### Agregar Nuevos Módulos

1. Crea un nuevo archivo en `modulos/mod_nuevo.py`
2. Define la función principal: `def abrir_nuevo(ventana_padre):`
3. Importa el módulo en `main.py`
4. Agrega el botón en la lista de módulos

## 📝 Notas Importantes

### Seguridad
- La shell educativa solo permite comandos básicos por seguridad
- Finalizar procesos del sistema puede causar inestabilidad
- Algunos directorios pueden requerir permisos de administrador

### Compatibilidad
- **Windows**: Totalmente compatible
- **Linux**: Totalmente compatible
- **macOS**: Compatible (algunos comandos pueden variar)

### Permisos
- Para finalizar procesos del sistema, puede requerir permisos de administrador
- Algunos directorios pueden no ser accesibles sin permisos elevados

## 🐛 Solución de Problemas

### Error: "No module named 'PIL'"
```bash
pip install pillow
```

### Error: "No module named 'psutil'"
```bash
pip install psutil
```

### Las imágenes no se cargan
- Verifica que la carpeta `imagenes/` esté en el mismo directorio que `main.py`
- Asegúrate de que los archivos PNG existan y no estén corruptos

### Error de permisos al finalizar procesos
- Ejecuta la aplicación como administrador (Windows) o con `sudo` (Linux/macOS)

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal.

## 👨‍💻 Autor

## jaider asprilla 

## 🔄 Historial de Versiones

### v2.0 (2025)
- ✅ Botones con imágenes en la pantalla principal
- ✅ Botones de retroceso en todos los módulos
- ✅ Interfaz mejorada con diseño moderno
- ✅ Código completamente documentado y comentado
- ✅ Información extendida del sistema
- ✅ Historial de comandos en la shell
- ✅ Barras de progreso visuales

### v1.0 (Original)
- Funcionalidades básicas de los 4 módulos
- Interfaz simple con botones de texto

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Haz un fork del proyecto
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

