# Mini Sistema Operativo Educativo

Este proyecto es una aplicación de escritorio que simula algunas funcionalidades básicas de un sistema operativo, diseñada con fines educativos utilizando Python y Tkinter.

## Características Principales

### 1. Explorador de Archivos
- Navegación por el sistema de archivos
- Vista de carpetas y archivos
- Funcionalidad de subir nivel
- Actualización en tiempo real del contenido
- Manejo de errores de permisos

### 2. Gestor de Procesos
- Lista de procesos activos en el sistema
- Visualización de PID y nombre de procesos
- Capacidad para finalizar procesos por PID
- Actualización de la lista de procesos

### 3. Shell Educativa
- Interfaz de línea de comandos simplificada
- Comandos básicos permitidos:
  - `ls` - Listar contenido del directorio
  - `dir` - Listar contenido del directorio (Windows)
  - `pwd` - Mostrar directorio actual
  - `echo` - Mostrar texto
- Salida formateada de comandos

### 4. Información del Sistema
- Datos del usuario actual
- Información del sistema operativo
- Detalles del hardware
- Información de espacio en disco
  - Espacio total
  - Espacio usado
  - Espacio disponible
  - Porcentaje de uso

## Requisitos del Sistema

- Python 3.x
- Bibliotecas requeridas:
  - tkinter (incluido en Python)
  - psutil
  - platform
  - getpass
  - os

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/Jaider77/OS-mini-.git
```

2. Instala las dependencias necesarias:
```bash
pip install psutil
```

3. Ejecuta la aplicación:
```bash
python main.py
```

## Estructura del Proyecto

```
os_mini/
├── main.py              # Punto de entrada de la aplicación
├── modulos/
│   ├── __init__.py
│   ├── mod_explorador.py    # Módulo del explorador de archivos
│   ├── mod_info.py          # Módulo de información del sistema
│   ├── mod_procesos.py      # Módulo de gestión de procesos
│   └── mod_shell.py         # Módulo de shell educativa
└── README.md
```

## Uso

1. Ejecuta `main.py`
2. La ventana principal mostrará cuatro botones para acceder a los diferentes módulos
3. Cada módulo se abrirá en una ventana independiente
4. Puedes tener múltiples módulos abiertos simultáneamente

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría realizar.

## Autor
Jaider Asprilla 

- Jaider77 (GitHub)