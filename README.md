Entrega 3 -DESPLIEGUE BÁSICO EN LA NUBE
MIGRACIÓN DE UNA APLICACIÓN WEB A LA NUBE PÚBLICA


Grupo 3
C. Camilo Baquero Gómez, Julian Torres, Franklin A. Pinto Carreño.
Desarrollo de Aplicaciones Cloud
Universidad de los Andes, Bogotá, Colombia
c.baquero@uniandes.edu.co, jy.torres@uniandes.edu.co, f.pintoc@uniandes.edu.co
Fecha de presentación: Marzo 5 de 2023

LINK APLICACIÓN WEB: http://comprimemelo.com:5000/
LINK DOCUMENTACION: https://docs.google.com/document/d/1TNBdU14JB5dwhn43IzIQIR3D6lsVBCWaGhuNs4VEAAs/edit
Video:
Arquitectura de la aplicación

La aplicación web de compresión de archivos se encuentra implementada bajo el modelo vista controlador. El modelo implementa un conjunto de métodos para crear, modificar, eliminar, consultar, comprimir y descomprimir archivos y tiene acceso directo al motor de persistencia.
La vista está implementada en formato html para los formularios y páginas de presentación en capa web, y para las api rest, se utiliza el formato json, para capturar y responder las peticiones web. El controlador es el intermediario entre el modelo y la vista para interpretar las peticiones y entregar una respuesta a cada petición web realizada por un usuario.

Diagrama de arquitectura


Figura 1. Diagrama de arquitectura aplicación de compresión de archivos

Para el despliegue de la aplicación Flask en ambiente productivo es indispensable usar el servidor HTTP WSGI llamado Gunicorn, el cual nos provee una mejor alternativa cuando se trata de escalar la aplicación.

Diagrama de despliegue





Arquitectura Cloud  GCP 




La aplicación está corriendo en el dominio www.comprimemelo.com:5000 , desarrollada en Flask la cual está dividida en 3 VM de Compute Engine de la siguiente manera: Worker, Web Server y Files Storage. La aplicación Flask (VM Compute Engine Web Server) interactúa con la base de datos Mysql Cloud SQL, el Worker procesa las colas de los archivos y el Compute Engine (File Store) guarda los archivos. 

Despliegue del componente web, el worker, y el sistema de almacenamiento de archivos en tres instancias de cómputo diferentes (máquinas virtuales)


Worker-Comprimemelo

Web-Comprimemelo

Storage-Comprimemelo

Configurar el servicio Cloud SQL para almacenar la base de datos de la aplicación Web




Configurar el servicio de VPC, con al menos una subred y las reglas de firewall mínimas para exponer de forma segura su aplicación.




ANÁLISIS DE CAPACIDAD

Prueba escenario 1.   Listar todas las tareas de conversión de un usuario

El servicio entrega el identificador de la tarea, el nombre y la extensión del archivo original, a qué extensión desea convertir y si está disponible o no. El usuario debe proveer el token de autenticación para realizar dicha operación.


Se ejecuta el plan de pruebas desde JMETER



Con 100,500 y 1000  peticiones en concurrencia no falló ninguna petición mientras que al usar 2000 comenzó a presentar fallos por timeout. Sin embargo, a nivel funcional se afirma que está dentro de los límites, dado que el requerimiento menciona que debe soportar 1000 peticiones concurrentes para este servicio.

Prueba escenario 2. Crear una cuenta de usuario en la aplicación

Para crear una cuenta se deben especificar los campos: usuario, correo electrónico y contraseña. El correo electrónico debe ser único en la plataforma dado que este se usa para la autenticación de los usuarios en la aplicación.

Para crear una cuenta de usuario es posible hacerlo a través de un formulario web ó consumiendo la api rest a través de un cliente http, ejemplo postman..

El siguiente endpoint con método post, permite crear una cuenta de usuario: http://comprimemelo.com:5000/api/auth/signup



o ingresando a la aplicación web en la siguiente url: http://comprimemelo.com:5000/api/auth/signup
presentará el siguiente formulario para el respectivo diligenciamiento de datos









Se ejecuta el plan de pruebas desde JMETER


Para este escenario se identifica que al ejecutar 300 peticiones concurrentes el sistema comienza a responder con timeout, esto posiblemente se debe es por las validaciones de existencia del usuario, creación del mismo y envío de correo simultáneo. Según los requerimientos del usuario se especifica que con 200 peticiones el sistema responde adecuadamente.

Prueba escenario 3. Iniciar sesión en la aplicación web

El usuario provee el correo electrónico/usuario y la contraseña con la que creó la cuenta de usuario en la aplicación. La aplicación retorna un token de sesión si el usuario se autenticó de forma correcta, de lo contrario indica un error de autenticación y no permite utilizar los recursos de la aplicación.

Para iniciar sesión en la aplicación se debe autenticarse ingresando las credenciales de usuario a través de la siguiente url http://comprimemelo.com:5000/api/auth/login
Para obtener el token de autenticación de usuario a través de la api rest debe usar el siguiente endpoint con metodo POST: http://comprimemelo.com:5000/api/auth/login



Se ejecuta el plan de pruebas desde JMETER



En esta prueba de concurrencia con 500 hilos comienza a presentarse timeout, hasta 350 peticiones concurrentes soporta sin presentar errores internos de servidor, sin embargo con las 350 peticiones se puede afirmar que cumple con los requerimientos del usuario. 

Prueba escenario 4.   Listar todas las tareas de conversión de un usuario.
Para obtener la información de una tarea de conversión específica. El usuario debe proveer el token de autenticación para realizar dicha operación.







5. Bibliografía


https://docs.celeryq.dev/en/stable/
https://flask.palletsprojects.com/en/2.2.x/
https://flask-jwt-extended.readthedocs.io/en/stable/






Instalar Python - https://www.python.org/  - instalar pip -> se selecciona en la instalación de python.
Python 3.8.3
pip 20.3.3

# Opcional - Descargar SQL-LITE - https://www.sqlite.org/index.html

# Instalar node - https://nodejs.org/es/
node v14.15.1
npm 6.14.11

# node-modules - carpeta static
cd app/static
npm init
npm install sweetalert2

# Instalar el ambiente virtual
cd ../../
pip install virtualenv==20.2.2
virtualenv venv

# Activar el entorno virtual en Windows
cd venv/Scripts
activate

# Agregar dependencias al archivo de requerimientos y ejecutar comandos - archivo en la raíz del proyecto 
cd ../../
pip install -r requirements.txt

# Correr al app en desarrollo
set FLASK_APP=main.py
set FLASK_DEBUG=1
set FLASK_ENV=development
flask run

# Usuario Base
    - app/migrate.py
    username: fpintoc
    pwd: mono2023
    
# NOTA (OPCIONAL) Reinicar (Base de datos) y configuración (user Default) 
    - Configurar usuario por defecto en app/migrate.py
ip:port/database

# Comandos requeridos para correr la apliación en producción


set FLASK_ENV=development
set FLASK_DEBUG=0
set FLASK_APP=main.py

flask --app main --debug run --host=0.0.0.0 --port 8000


nohup python3 server.py &


# Directorio de instalación archivos despligue app
 cd /var/www/html/events
 
# librerias instaladas en ambiente de producción
bcrypt==4.0.1
click==8.1.3
colorama==0.4.6
dnspython==2.3.0
dominate==2.7.0
email-validator==1.3.1
Flask==2.2.2
Flask-Bcrypt==1.0.1
Flask-Bootstrap==3.3.7.1
Flask-FontAwesome==0.1.5
Flask-Login==0.6.2
Flask-SQLAlchemy==3.0.2
Flask-Testing==0.8.1
Flask-WTF==1.1.1
greenlet==2.0.2
idna==3.4
itsdangerous==2.0.1
Jinja2==3.0.3
MarkupSafe==2.1.2
marshmallow==3.19.0
marshmallow-sqlalchemy==0.28.1
packaging==23.0
SQLAlchemy==2.0.0
typing_extensions==4.4.0
visitor==0.1.3
Werkzeug==2.2.2
WTForms==2.3.3
 
