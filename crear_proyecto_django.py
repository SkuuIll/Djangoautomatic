import os
import subprocess
import sys
import platform

# --- Funciones de Utilidad ---

def run_command(command, cwd=None, capture=True):
    """Ejecuta un comando en la terminal y muestra la salida."""
    print(f"\n> Ejecutando: {' '.join(command)}")
    try:
        # Usamos shell=True en Windows para que encuentre los ejecutables del venv y comandos como 'start'
        use_shell = platform.system() == "Windows"
        if capture:
            # Captura la salida para comandos internos como 'pip freeze' o 'migrate'
            subprocess.run(command, check=True, cwd=cwd, shell=use_shell, capture_output=True, text=True, encoding='utf-8')
        else:
            # No captura la salida para comandos que abren nuevas ventanas
            subprocess.run(command, check=True, cwd=cwd, shell=use_shell)
        print("... Comando ejecutado exitosamente.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"*** Error al ejecutar el comando: {e}")
        # A veces el error no está en stderr, así que mostramos ambos
        if e.stdout:
            print(f"*** Salida estándar:\n{e.stdout}")
        if e.stderr:
            print(f"*** Salida del error:\n{e.stderr}")
        return False
    except FileNotFoundError as e:
        print(f"*** Error: Comando no encontrado. Asegúrate de que está en tu PATH. {e}")
        return False


def create_file(path, content=""):
    """Crea un archivo en la ruta especificada con contenido opcional."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"-> Archivo creado: {os.path.basename(path)}")
    except IOError as e:
        print(f"*** Error al crear el archivo {path}: {e}")

def modify_file(path, find_str, replace_str):
    """Busca una cadena en un archivo y la reemplaza por otra."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        content = content.replace(find_str, replace_str)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"-> Archivo modificado: {os.path.basename(path)}")
    except IOError as e:
        print(f"*** Error al modificar el archivo {path}: {e}")


# --- Lógica Principal del Script ---

def main():
    """Función principal que orquesta la creación del proyecto Django."""
    print("--- INICIANDO AUTOMATIZACIÓN DE PROYECTO DJANGO ---")

    # 1. Obtener el nombre del proyecto
    project_name = input("Por favor, introduce el nombre de tu proyecto (ej: mi_blog): ")
    if not project_name or ' ' in project_name:
        print("El nombre del proyecto no puede estar vacío o contener espacios.")
        return

    project_root = os.path.join(os.getcwd(), project_name)
    if os.path.exists(project_root):
        print(f"El directorio '{project_name}' ya existe. Por favor, elige otro nombre o elimina la carpeta existente.")
        return

    os.makedirs(project_root)
    print(f"\nCreado directorio raíz del proyecto: {project_root}")

    # Determinar los nombres de los ejecutables del entorno virtual según el SO
    if platform.system() == "Windows":
        python_executable = os.path.join(project_root, "entorno", "Scripts", "python.exe")
        pip_executable = os.path.join(project_root, "entorno", "Scripts", "pip.exe")
        django_admin_executable = os.path.join(project_root, "entorno", "Scripts", "django-admin.exe")
    else: # Linux/macOS
        python_executable = os.path.join(project_root, "entorno", "bin", "python")
        pip_executable = os.path.join(project_root, "entorno", "bin", "pip")
        django_admin_executable = os.path.join(project_root, "entorno", "bin", "django-admin")

    # 2. Crear entorno virtual
    if not run_command([sys.executable, "-m", "venv", "entorno"], cwd=project_root):
        return

    # 3. Instalar dependencias
    dependencies = ["django", "pillow"]
    if not run_command([pip_executable, "install"] + dependencies, cwd=project_root):
        return

    # 4. Crear proyecto Django
    if not run_command([django_admin_executable, "startproject", project_name, "."], cwd=project_root):
        return

    # 5. Crear estructura de carpetas adicional
    print("\nCreando estructura de carpetas adicional...")
    extra_dirs = ["apps", "static", "media", "templates"]
    for dirname in extra_dirs:
        os.makedirs(os.path.join(project_root, dirname))
        print(f"-> Directorio creado: {dirname}")

    # 6. Reestructurar la configuración
    print("\nReestructurando la configuración para entornos (local/prod)...")
    config_dir = os.path.join(project_root, project_name, "configuraciones")
    original_settings_path = os.path.join(project_root, project_name, "settings.py")
    new_settings_path = os.path.join(config_dir, "settings.py")
    
    os.makedirs(config_dir)
    os.rename(original_settings_path, new_settings_path)
    print(f"-> Movido 'settings.py' a '{os.path.join(project_name, 'configuraciones')}'")

    create_file(os.path.join(config_dir, "local.py"), "from .settings import *\n")
    create_file(os.path.join(config_dir, "prod.py"), "from .settings import *\n\nDEBUG = False\n")

    # 7. Modificar archivos de configuración
    print("\nModificando archivos de configuración...")
    manage_py_path = os.path.join(project_root, "manage.py")
    find_manage = f"os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')"
    replace_manage = f"os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.configuraciones.local')"
    modify_file(manage_py_path, find_manage, replace_manage)

    settings_path = new_settings_path
    with open(settings_path, 'r', encoding='utf-8') as f:
        content_lines = f.readlines()

    new_content_lines = []
    # Asegurarse de que 'os' está importado
    has_os_import = any("import os" in line for line in content_lines)
    
    # Reemplazar Path por os si es necesario
    if not has_os_import:
        for i, line in enumerate(content_lines):
            if "from pathlib import Path" in line:
                content_lines[i] = "import os\n"
                break
    
    for line in content_lines:
        # Reemplazar BASE_DIR
        if line.strip().startswith("BASE_DIR"):
            # Usamos una definición de BASE_DIR que funciona con la estructura de carpetas movida
            new_content_lines.append(f"BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n")
        # Modificar DIRS dentro de TEMPLATES
        elif "'DIRS': []," in line:
            new_content_lines.append("        'DIRS': [os.path.join(BASE_DIR, 'templates')],\n")
        # CORRECCIÓN: Modificar la ruta de la base de datos
        elif "'NAME': BASE_DIR / 'db.sqlite3'," in line:
            new_content_lines.append("        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),\n")
        # Reemplazar LANGUAGE_CODE
        elif line.strip().startswith("LANGUAGE_CODE"):
            new_content_lines.append("LANGUAGE_CODE = 'es-ar'\n")
        # Reemplazar TIME_ZONE
        elif line.strip().startswith("TIME_ZONE"):
            new_content_lines.append("TIME_ZONE = 'America/Argentina/Buenos_Aires'\n")
        else:
            new_content_lines.append(line)
            
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.writelines(new_content_lines)
        f.write("\n# --- Configuraciones Adicionales del Script ---\n")
        f.write("STATIC_URL = '/static/'\n")
        f.write("STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]\n")
        f.write("MEDIA_URL = '/media/'\n")
        f.write("MEDIA_ROOT = os.path.join(BASE_DIR, 'media')\n")
    
    print("-> Archivo 'settings.py' actualizado con las nuevas rutas y configuraciones.")

    # 8. Crear requirements.txt
    print("\nGenerando archivo requirements.txt...")
    with open(os.path.join(project_root, "requirements.txt"), "w") as f:
        subprocess.run([pip_executable, "freeze"], stdout=f, check=True, cwd=project_root, shell=(platform.system() == "Windows"))

    # --- INICIO DE LA NUEVA SECCIÓN: Migraciones y Auto-inicio ---
    print("\n--- Realizando configuraciones finales ---")

    # 9. Realizar migraciones iniciales
    if not run_command([python_executable, "manage.py", "migrate"], cwd=project_root):
        print("\n*** No se pudieron aplicar las migraciones. Por favor, ejecútalas manualmente.")
        input("\nPresiona Enter para salir...")
        return

    # 10. Iniciar el servidor de desarrollo en una nueva terminal
    print("\nIniciando el servidor de desarrollo en una nueva terminal...")
    print("NOTA: Aún necesitas crear un superusuario manualmente.")
    print("      Para ello, abre otra terminal, activa el entorno y ejecuta: python manage.py createsuperuser")

    start_server_command = []
    if platform.system() == "Windows":
        # CORRECCIÓN: Se simplifica el comando para mayor compatibilidad con Windows.
        # Se crea un archivo .bat temporal para ejecutar los comandos en secuencia.
        bat_path = os.path.join(project_root, "start_server.bat")
        with open(bat_path, "w") as bat_file:
            bat_file.write("@echo off\n")
            bat_file.write(f"cd /d \"{project_root}\"\n")
            bat_file.write("echo Activando entorno y ejecutando servidor...\n")
            bat_file.write(".\\entorno\\Scripts\\activate && python manage.py runserver\n")
        start_server_command = ["start", "cmd", "/c", bat_path]

    elif platform.system() == "Darwin": # macOS
        activate_cmd = f"cd \\\"{project_root}\\\"; source entorno/bin/activate; python manage.py runserver"
        start_server_command = ["osascript", "-e", f'tell app "Terminal" to do script "{activate_cmd}"']
    else: # Linux (asumiendo gnome-terminal)
        activate_cmd = f"bash -c 'source entorno/bin/activate; python manage.py runserver; exec bash'"
        # Usamos -- para separar las opciones de gnome-terminal del comando a ejecutar
        start_server_command = ["gnome-terminal", f"--working-directory={project_root}", "--", "bash", "-c", activate_cmd]

    if start_server_command:
        run_command(start_server_command, capture=False)
    else:
        print("\nNo se pudo determinar el comando para iniciar el servidor en tu sistema operativo.")
        print("Por favor, inicia el servidor manualmente ejecutando: python manage.py runserver")

    # --- Finalización ---
    print("\n--- ¡PROYECTO DJANGO CREADO Y EN EJECUCIÓN! ---")
    print(f"Tu proyecto '{project_name}' está listo en la carpeta '{project_root}'")
    print("El servidor de desarrollo debería estar ejecutándose en una nueva ventana.")
    print("----------------------------------------------------")
    input("\nPresiona Enter para cerrar este script...")


if __name__ == "__main__":
    main()
