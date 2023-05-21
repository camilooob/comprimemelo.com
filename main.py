import threading
from flask import render_template as render, flash, send_from_directory, request
from app import *
from app.services import download_file, download_file, download_file_pdf,register_file,download_file_original
import zipfile
import os.path
import time  
import datetime
from flask import Flask, jsonify, make_response   
from werkzeug.security import generate_password_hash, check_password_hash
import uuid 
import jwt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity
from flask_mail import Mail,Message
import datetime
from functools import wraps
from app.database import *
from flask import copy_current_request_context
import os
import getpass
from celery import Celery

basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app()
mail=Mail()
jwt = JWTManager(app)
mail.init_app(app)

@app.errorhandler(404)
def not_found(error):
    """ Método para error 404. """
    return render('errors/error404.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    """ Método para error 500. """
    return render('errors/error500.html')

@app.route('/')
def index():
    return render('index.html')

@app.route('/database')
def database():
    init_db()
    return "base de datos creada correctamente. """


@app.route('/app/v1/upload', methods=['GET', 'POST'])
def upload():

    return render('upload.html')

@app.route('/app/files/compress/upload',methods=['POST'])
@jwt_required()
def index4():
    url_params = request.args

    # Retrieve parameters which are present
    format = url_params['format']

    print(f'compressing...{format}')
    file = request.files['file']
    pathRoot=os.path.abspath(os.curdir)+"/"
    pathUpload=f"sin_comprimir/"
    pathCompress=f"comprimidos/"
    pathFile=pathRoot+pathUpload+f"{file.filename}"
    file.save(pathFile);
    #guardar en servidor remoto archivo sin comprimir
    os.system('gcloud storage cp /root/comprimemelo.com/sin_comprimir gs://file_comprimemelo_bucket_storage/sin_comprimir/')
    print('compressing...')
    nombre_archivo, extension = os.path.splitext(pathFile)
    #pathZip=pathRoot+file.filename.replace(extension,'.zip')
    pathZip=pathRoot+pathCompress+file.filename.replace(extension,format)
    with zipfile.ZipFile(pathZip, 'w') as zf:
        zf.write(pathFile,arcname=file.filename)
    #guardar en servidor remoto archivo comprimido
    os.system('gcloud storage cp /root/comprimemelo.com/sin_comprimir gs://file_comprimemelo_bucket_storage/comprimidos/')
    print('...compression done!')

    file_data = {
        #'filename': file.filename.replace(extension,'.zip'),
        'filenameOriginal': file.filename,
        'filenameCompress': file.filename.replace(extension,format),
        'formatOriginal': extension,
        'formatCompress': format,
        'mimeTypeOriginal':DIC_MIME_TYPES[extension],
        'mimeTypeCompress':DIC_MIME_TYPES[format],
        'path': pathZip,
        'pathOriginal': pathFile,
        'state': 'COMPRIMIDO',
        'notified': False,
        'startDate': datetime.datetime.utcnow(),                
        'endDate': datetime.datetime.utcnow(),    
        'data': file.read(),
        'email':get_jwt_identity()
      }
    id=register_file(file_data)
      

    msg=Message('El Archivo se a comprimido satisfactoriamente', sender=app.config['MAIL_USERNAME'],recipients=[get_jwt_identity()])
    mail.send(msg)
    
    return f"{id}"

@app.route('/app/files/compress/download/<upload_id>', methods=["GET", "POST"])
@jwt_required()
def downloadFileCompress(upload_id):
   
   return  download_file(upload_id)


@app.route('/api/files/<filename>', methods=["GET", "POST"])
@jwt_required()
def downloadFileOriginal(filename):
   pathRoot=os.path.abspath(os.curdir)+"/"
   pathUpload=f"sin_comprimir/"
   pathFile=pathRoot+pathUpload+f"{filename}"
   #revisar como recuperar el archivo
   os.system('gcloud storage cp /root/comprimemelo.com/sin_comprimir gs://file_comprimemelo_bucket_storage/sin_comprimir/')

   return  download_file_original(pathFile)


@app.route("/app/auth/v1/login", methods=["GET", "POST"])
def loginAuth():

    return "token dsajfklajsdkfjaklsdjkflñaj"


@app.route("/app/v1/login", methods=["GET", "POST"])
def login():
    context = {"type": "", "mensaje": ""}
    if request.method == "POST":

        print("entreee mor ")
        username = request.form["username"]
        password = request.form["password"]
        args = {"username": username, "password": password}
        response = requests.post("http://localhost:5000/Api/Methods/Login/", json=args)
        print(response)
        if response.status_code == 200:  # and r.exists(username) == 0:
            response_api = json.loads(response.text)
            response_user = requests.post(
                "http://localhost:5000/Api/Usuario/ValidarUsuario/",
                json={"username": username},
            )
            response_user = json.loads(response_user.text)
            session["token"] = response_api["token"]
            session["rol"] = response_user["rol"]
            session["username"] = username
            return render_template("index.html", context=context)
        else:
            context["type"] = "danger"
            context["mensaje"] = "Usuario no encontrado"
            return render_template("login.html", context=context)
    return render_template("login.html", context=context)




def token_required(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):

       token = None 

       if 'x-access-tokens' in request.headers:  
          token = request.headers['x-access-tokens'] 


       if not token:  
          return jsonify({'message': 'a valid token is missing'})   


       try:  
          data = jwt.decode(token, app.config[SECRET_KEY]) 
          current_user = User.query.filter_by(public_id=data['public_id']).first()  
       except:  
          return jsonify({'message': 'token is invalid'})  


          return f(current_user, *args,  **kwargs)  
    return decorator 


@app.route('/api/auth/signup', methods=['POST'])
def register():
    print('variable PASSWORD_EMAIL_FP ')
    print(os.environ.get('PASSWORD_EMAIL_FP'))
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    if test:
        return jsonify(message='That email already exists'), 409
    else:
       
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    msg=Message('El usuario se ha creado satisfactoriamente', sender=app.config['MAIL_USERNAME'],recipients=[email])
    mail.send(msg)
    
    return jsonify(message='User created successfully'), 201
    
def send_email(user_email, username, msg):
    msg=Message(msg, sender=app.config['MAIL_USERNAME'],recipients=[user_email])

@app.route('/api/auth/login', methods=['POST'])
def loginToken():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login Successful', access_token=access_token)
    else:
        return jsonify('Bad email or Password'), 401
    
DIC_MIME_TYPES = { 
    ".aac"  :"audio/aac",
    ".abw"  :"application/x-abiword",
    ".arc"  :"application/octet-stream",
    ".avi"  :"video/x-msvideo",
    ".azw"  :"application/vnd.amazon.ebook",
    ".bin"  :"application/octet-stream",
    ".bz"   :"application/x-bzip",
    ".bz2"  :"application/x-bzip2",
    ".csh"  :"application/x-csh",
    ".css"  :"text/css",
    ".csv"  :"text/csv",
    ".doc"  :"application/msword",
    ".docx" :"application/msword",
    ".epub" :"application/epub+zip",
    ".gif"  :"image/gif",
    ".htm"  :"text/html",
    ".ico"  :"image/x-icon",
    ".ics"  :"text/calendar",
    ".jar"  :"application/java-archive",
    ".jpeg" :"image/jpeg",
    ".js"   :"application/javascript",
    ".json" :"application/json",
    ".mid"  :"audio/midi",
    ".mpeg" :"video/mpeg",
    ".mpkg" :"application/vnd.apple.installer+xml",
    ".odp"  :"application/vnd.oasis.opendocument.presentation",
    ".ods"  :"application/vnd.oasis.opendocument.spreadsheet",
    ".odt"  :"application/vnd.oasis.opendocument.text",
    ".oga"  :"audio/ogg",
    ".ogv"  :"video/ogg",
    ".ogx"  :"application/ogg",
    ".pdf"  :"application/pdf",
    ".ppt"  :"application/vnd.ms-powerpoint",
    ".rar"  :"application/x-rar-compressed",
    ".rtf"  :"application/rtf",
    ".sh"   :"application/x-sh",
    ".svg"  :"image/svg+xml",
    ".swf"  :"application/x-shockwave-flash",
    ".tar"  :"application/x-tar",
    ".tif"  :"image/tiff",
    ".ttf"  :"font/ttf",
    ".vsd"  :"application/vnd.visio",
    ".wav"  :"audio/x-wav",
    ".weba" :"audio/webm",
    ".webm" :"video/webm",
    ".webp" :"image/webp",
    ".woff" :"font/woff",
    ".woff2":"font/woff2",
    ".xhtml":"application/xhtml+xml",
    ".xls"  :"application/vnd.ms-excel",
    ".xml"  :"application/xml",
    ".xul"  :"application/vnd.mozilla.xul+xml",
    ".zip"  :"application/zip",
    ".3gp"  :"video/3gpp",
    ".3g2"  :"video/3gpp2",
    ".7z"   :"application/x-7z-compressed",
    ".tar.bz" :"application/x-gzip",
    ".tar.bz2" :"application/x-gzip",
    ".gz" :"application/x-gzip",
    ".bzip" :"application/x-bzip",
    
    }

app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'  # RabbitMQ broker URL
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # Redis backend URL

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

# Define a Celery task to list the user's tasks
@celery.task
def list_tasks(user_id):
    # Replace this with your code to fetch the user's tasks from a database or other data source
    tasks = [{'id': 1, 'description': 'Task 1'}, {'id': 2, 'description': 'Task 2'}]
    return tasks

# Define the /api/tasks endpoint
@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = 123  # Replace this with your code to fetch the user's ID from the request or session
    #task = list_tasks.delay(user_id)  # Call the Celery task asynchronously
    #result = task.get()  # Wait for the task to complete and get the result
    return jsonify('''{'tasks': {"id": "1" "original_file": "pdf", "formtar": "rar", "status": "processed"}}''')

@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    if 'fileName' not in request.files or 'newFormat' not in request.form:
        #TODO Camilo
        return {'message': 'Tarea Creada'}, 200

    file = request.files['fileName']
    new_format = request.form['newFormat']
    
    if file and allowed_file(file.filename):
        task_id = convert_format.delay(file.filename, new_format)
        
        return {'message': 'Task created', 'task_id': task_id}, 200
    else:
        return {'message': 'Invalid file format'}, 400
    
@app.route('/api/tasks/<int:id_task>', methods=['GET'])
@jwt_required()
def get_task(id_task):
    #task = get_task_info.delay(id_task)
    return jsonify('''{'tasks': {"id": "1" "original_file": "pdf", "formtar": "rar", "status": "processed"}}''')

@app.route('/api/tasks/<int:id_task>', methods=['DELETE'])
@jwt_required()
def delete_task(id_task):
    # verificar si el usuario está autorizado
    #return jsonify('''{'tasks_delete': {"id": "1" "original_file": "pdf", "formtar": "rar", "status": "processed"}}''')
    
    # enviar tarea de eliminación al worker de celery
    #task = celery.send_task('tasks.delete_task', args=[id_task])
    
    return jsonify({'message': f'Tarea  eliminada con éxito'}), 200


# tarea de eliminación de tarea
@celery.task(name='tasks.delete_task')
def delete_task(id_task):
    # implementar eliminación de tarea aquí
    pass

def eliminar_archivos(tarea):
    # eliminar los archivos originales y convertidos de la tarea
    os.remove(tarea.archivo_original)
    os.remove(tarea.archivo_convertido)

@app.route('/eliminar_archivo/<int:id_tarea>', methods=['DELETE'])
@jwt_required()
def eliminar_archivo(id_tarea, token):
    # verificar si la tarea existe y su estado es 'Disponible'
    tarea = obtener_tarea(id_tarea)
    if tarea is None or tarea.estado != 'Disponible':
        return jsonify({'error': 'La tarea no existe o su estado no es "Disponible"'})

    # eliminar los archivos originales y convertidos
    eliminar_archivos(tarea)

    # actualizar el estado de la tarea a 'Eliminado'
    tarea.estado = 'Eliminado'
    guardar_tarea(tarea)

    # devolver una respuesta exitosa
    return jsonify({'mensaje': 'Los archivos se han eliminado exitosamente'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 3080)))    