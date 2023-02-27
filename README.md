Aplicación de Eventos Entrega 1 - comprimemelo.com - Cristhiam Camilo Baquero Gomez - c.baquero@uniandes.edu.co - Julian Torres - jy.torres@uniandes.edu.co - Franklin Augusto Pinto Carreño -f.pintoc@uniandes.edu.co - 201011075


#VIDEO EXPLICACIÓN: https://youtu.be/xY8I-C4ZGRo
 #Documento de arquitectura de la aplicación: file llamado "Guia Uso - Arquitectura-conclusiones y consideraciones.pdf"

# Instalar Python - https://www.python.org/  - instalar pip -> se selecciona en la instalación de python.
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
 
