from flask import render_template as render, flash, send_from_directory, request
from app import create_app
from app.database import Usuarios
from app.migrate import init_db
from app.services import list_public_eventos, download_file, download_file, download_file_pdf,register_file,download_file_original
import zipfile
import os.path
import time  
import datetime
from flask import Flask, jsonify, make_response   
from werkzeug.security import generate_password_hash, check_password_hash
import uuid 
import jwt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import datetime
from functools import wraps
from app.database import *

basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app()

jwt = JWTManager(app)

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
    context = {
        'public_eventos': list_public_eventos()
    }
    return render('index.html', **context)

@app.template_filter()
def visibility_public_or_private(visibility):
    """ Filtro de visibilidad de eventos. """
    return 'Pública'  if visibility == True else 'Privada'

@app.route('/profile/picture/<path:filename>')
def picture_profile(filename):
    base_url = 'uploads/profile_pictures'
    if filename == 'none':
        filename = 'user_default.JPG'
        
    return send_from_directory(base_url, filename)

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

      print('compressing...')
      nombre_archivo, extension = os.path.splitext(pathFile)
      #pathZip=pathRoot+file.filename.replace(extension,'.zip')
      pathZip=pathRoot+pathCompress+file.filename.replace(extension,format)
      with zipfile.ZipFile(pathZip, 'w') as zf:
          zf.write(pathFile,arcname=file.filename)
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
        'username':'fpintoc'
      }
      id=register_file(file_data)
   
      #return f"Archivo guardado correctamente. {id}"
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
          current_user = Users.query.filter_by(public_id=data['public_id']).first()  
       except:  
          return jsonify({'message': 'token is invalid'})  


          return f(current_user, *args,  **kwargs)  
    return decorator 


@app.route('/api/auth/signup', methods=['POST'])
def register():
    email = request.form['email']
    test = Usuarios.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = Usuarios(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully'), 201
    

@app.route('/api/auth/login', methods=['POST'])
def loginToken():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = Usuarios.query.filter_by(email=email, password=password).first()
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