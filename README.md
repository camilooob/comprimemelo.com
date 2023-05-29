ENTREGA 5 - DESPLIEGUE EN PAAS
MIGRACIÓN DE UNA APLICACIÓN WEB A UN PLATAFORMA COMO
SERVICIO EN LA NUBE PÚBLICA 

Grupo 3
C. Camilo Baquero Gómez, Julian Torres, Franklin A. Pinto Carreño.
Desarrollo de Aplicaciones Cloud
Universidad de los Andes, Bogotá, Colombia
c.baquero@uniandes.edu.co, jy.torres@uniandes.edu.co, f.pintoc@uniandes.edu.co
Fecha de presentación: MAYO 28 de 2023

LINK APLICACIÓN WEB: https://crunbuid-webappcomprimemelo-imm52zicba-uc.a.run.app
LINK componentes backend: https://cloud-run-backoffice-comprimemelo-imm52zicba-uc.a.run.app/api
Github frontend: https://github.com/camilooob/comprimemelo.com
Github Backend: https://github.com/JulianTorrest/Comprimemelo-Backoffice
Video: https://www.youtube.com/watch?v=TGW-4ybs7Eg


La aplicación web de compresión de archivos se encuentra implementada bajo el modelo desacoplamiento utilizando una instancia web que se encarga de desplegar el front en un compute engine, y procesar los archivos de compresión en un Worker comunicado mediante una cola de Pubsub, el front y un worker que procesa la compresión de archivos. 

Cuando el server web  o worker supera un uso de cpu en un 60% se activa la regla de autoscaling y despliega un nodo adicional y lo agrega al Balanceador de Carga. El modelo implementa un conjunto de métodos para crear, modificar, eliminar, consultar, comprimir y descomprimir archivos y tiene acceso directo al motor de persistencia.

La vista está implementada en formato html para los formularios y páginas de presentación en capa web, y para las api rest, se utiliza el formato json, para capturar y responder las peticiones web. El controlador es el intermediario entre el modelo y la vista para interpretar las peticiones y entregar una respuesta a cada petición web realizada por un usuario.




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
 
