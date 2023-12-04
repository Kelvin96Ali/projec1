# Project 1

## README - Configuración de PostgreSQL, Python, Flask y Google Books API

Este repositorio contiene los pasos necesarios para configurar PostgreSQL, Python, Flask y utilizar la API de Google Books para tu proyecto. A continuación, se detallan los pasos a seguir:

### Configuración de PostgreSQL con Render

1. **Registro en Render**: Accede a [Render](https://render.com/) y crea una cuenta si aún no la tienes.
2. **Dashboard en Render**: Dirígete al "Dashboard" una vez que hayas iniciado sesión en Render.
3. **Creación de la base de datos**: Haz clic en "New PostgreSQL" y proporciona un nombre para tu base de datos.
4. **Crear la base de datos**: Haz clic en "Create Database" para generar tu base de datos.
5. **Conexión a la base de datos**: En la sección de "connect", encuentra la cadena de conexión en la pestaña "External Database". Copia el "External Database URL" para acceder a tu base de datos.

### Conexión a la base de datos

- Para conectarte a tu base de datos alojada en Render, puedes utilizar herramientas como BeekeeperStudio. Ingresa la URL de conexión proporcionada por Render.

- Alternativamente, si decides instalar PostgreSQL localmente, puedes usar el comando PSQL en la línea de comandos, utilizando el enlace provisto en las credenciales de Render.

### Configuración de Python y Flask

1. **Instalación de Python**: Asegúrate de tener instalada una versión de Python igual o superior a la 3.6 (se recomienda la versión 3.9).
2. **Instalación de pip**: Verifica si pip está instalado ejecutando `pip` en una ventana de terminal. Si no está instalado, asegúrate de instalarlo antes de continuar.
3. **Ejecución de la aplicación Flask**:
   - Descarga el directorio de distribución del proyecto desde [este enlace](https://cdn.cs50.net/web/2020/x/projects/1/project1.zip) y descomprímelo.
   - Navega al directorio del proyecto en una ventana de terminal.
   - Ejecuta `pip3 install -r requirements.txt` para asegurarte de tener los paquetes necesarios instalados, como Flask y SQLAlchemy.
   - Asigna el valor `application.py` a la variable de entorno `FLASK_APP`. En Mac o Linux, usa `export FLASK_APP=application.py`; en Windows, usa `set FLASK_APP=application.py`.
   - Opcionalmente, puedes asignar `1` a la variable de entorno `FLASK_DEBUG` para activar el depurador de Flask y habilitar la recarga automática de la aplicación al guardar cambios en archivos.
   - Asigna la URI de tu base de datos a la variable de entorno `DATABASE_URL`, que puedes obtener desde la página de credenciales en Render.
   - Ejecuta `flask run` para iniciar tu aplicación Flask. Al acceder al URL proporcionado por Flask, deberías ver el texto "Project 1: TODO".

