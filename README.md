Automatización de Proyectos DjangoEste repositorio contiene un script de Python diseñado para automatizar la creación y configuración inicial de un proyecto Django, siguiendo las mejores prácticas y una estructura de carpetas organizada.El objetivo principal es acelerar el arranque de nuevos proyectos, eliminando la necesidad de repetir tareas manuales y de configuración en cada ocasión.🚀 CaracterísticasEl script realiza las siguientes tareas de forma automática:Crea un directorio raíz para el nuevo proyecto.Configura un entorno virtual (venv) para aislar las dependencias.Instala las dependencias iniciales necesarias (Django y Pillow).Crea el proyecto Django y la estructura base.Organiza una estructura de carpetas adicional para apps, templates, static y media.Reestructura el archivo settings.py en una carpeta de configuraciones con archivos separados para entornos local y prod.Modifica los archivos de configuración (settings.py y manage.py) para reflejar la nueva estructura.Genera un archivo requirements.txt con todas las dependencias instaladas.Ejecuta las migraciones iniciales de la base de datos.Inicia automáticamente el servidor de desarrollo de Django en una nueva terminal.📋 RequisitosPython 3.x instalado en tu sistema.⚙️ Instalación y UsoPara utilizar este script y crear tu propio proyecto Django, sigue estos pasos:Clona o descarga este repositorio en tu máquina local.Abre una terminal o línea de comandos.Navega hasta la carpeta donde se encuentra el archivo crear_proyecto_django.py.Ejecuta el script con el siguiente comando:python crear_proyecto_django.py
Introduce el nombre de tu proyecto cuando el script te lo solicite y presiona Enter.El script se encargará del resto. Verás en la terminal todos los pasos que va realizando. Al finalizar, se abrirá una nueva ventana de terminal con el servidor de Django en funcionamiento.🛠️ Pasos Post-CreaciónUna vez que el script ha finalizado, tu proyecto Django estará creado y en ejecución. Sin embargo, aún necesitas realizar un paso manual importante:Crear un SuperusuarioPara poder acceder al panel de administración de Django (/admin), necesitas crear un superusuario.Abre una nueva terminal.Navega hasta la carpeta raíz de tu nuevo proyecto (ej: cd mi_blog).Activa el entorno virtual:En Windows: .\entorno\Scripts\activateEn macOS/Linux: source entorno/bin/activateEjecuta el comando para crear el superusuario:python manage.py createsuperuser
Sigue las instrucciones para definir tu nombre de usuario, email y contraseña.¡Listo! Ahora puedes acceder a http://127.0.0.1:8000/admin con las credenciales que acabas de crear.📂 Estructura del Proyecto GeneradoEl script creará la siguiente estructura de carpetas y archivos:mi_proyecto/
├── apps/                 # Directorio para tus aplicaciones de Django
├── media/                # Para archivos subidos por los usuarios
├── static/               # Para archivos estáticos (CSS, JS, imágenes)
├── templates/            # Para las plantillas HTML
├── mi_proyecto/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── configuraciones/  # Nueva carpeta para los settings
│       ├── __init__.py
│       ├── settings.py   # Configuración base
│       ├── local.py      # Configuración para desarrollo
│       └── prod.py       # Configuración para producción
├── entorno/              # Entorno virtual de Python
├── .gitignore
├── db.sqlite3            # Base de datos inicial
├── manage.py             # Utilidad de comandos de Django
└── requirements.txt      # Dependencias del proyecto
