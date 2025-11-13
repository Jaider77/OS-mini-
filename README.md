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
- Refresca la vista actual
- Doble clic para entrar en carpetas

#### 2. **Gestión de Procesos**
- Lista todos los procesos activos del sistema
- Muestra PID, nombre y usuario de cada proceso
- Finaliza procesos seleccionados
- Contador de procesos activos
- Advertencias de seguridad

#### 3. **Shell Educativa**
- Terminal de comandos básicos
- Comandos permitidos: `ls`, `dir`, `pwd`, `echo`, `clear`
- Historial de comandos (navega con flechas ↑↓)
- Interfaz estilo terminal con fondo oscuro
- Mensajes de ayuda y error informativos

#### 4. **Información del Sistema**
- Información del usuario actual
- Detalles del sistema operativo
- Información del procesador (núcleos, frecuencia, uso)
- Uso de memoria RAM con barras de progreso visuales
- Espacio en disco de todas las particiones
- Información de interfaces de red
- Tiempo de actividad del sistema

## 🚀 Requisitos

### Dependencias de Python

```bash
pip install pillow psutil
```

- **Python**: 3.6 o superior
- **tkinter**: Incluido en la mayoría de instalaciones de Python
- **Pillow (PIL)**: Para manejo de imágenes
- **psutil**: Para información de procesos y sistema

## 📦 Estructura del Proyecto

```
mini_sistema_operativo/
│
├── main.py                      # Archivo principal de la aplicación
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias del proyecto
│
├── modulos/                     # Paquete de módulos
│   ├── __init__.py             # Inicializador del paquete
│   ├── mod_explorador.py       # Módulo explorador de archivos
│   ├── mod_procesos.py         # Módulo gestión de procesos
│   ├── mod_shell.py            # Módulo shell educativa
│   └── mod_info.py             # Módulo información del sistema
│
└── imagenes/                    # Recursos gráficos
    ├── explorador.png          # Icono del explorador
    ├── procesos.png            # Icono de procesos
    ├── shell.png               # Icono de la shell
    └── info.png                # Icono de información
```

## 🎮 Uso

### Instalación

1. **Clona o descarga el proyecto**:
   ```bash
   git clone <url-del-repositorio>
   cd mini_sistema_operativo
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación**:
   ```bash
   python main.py
   ```

### Navegación

1. **Pantalla Principal**: Selecciona el módulo que deseas usar haciendo clic en su botón
2. **Dentro de cada módulo**: Usa los controles específicos de cada funcionalidad
3. **Retroceder**: Haz clic en el botón "⬅️ Retroceder" para volver al menú principal

## 🛠️ Modificaciones y Personalización

### Cambiar las Imágenes de los Botones

1. Reemplaza los archivos PNG en la carpeta `imagenes/`
2. Mantén los mismos nombres de archivo
3. Tamaño recomendado: 256x256 píxeles
4. Formato: PNG con fondo transparente o blanco

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

