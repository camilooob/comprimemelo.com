from flask import render_template as render, flash, send_from_directory, request
from app import create_app
from app.database import Usuarios
from app.migrate import init_db
from app.services import list_public_eventos, download_file, download_file, download_file_pdf,register_file
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

@app.route('/app/v1/compress/upload',methods=['POST'])
@jwt_required()
def index4():
      url_params = request.args
  
    # Retrieve parameters which are present
      format = url_params['format']

      print(f'compressing...{format}')
      file = request.files['file']
      pathRoot=os.path.abspath(os.curdir)+"/"
      pathUpload=f"uploads/"
      pathFile=pathRoot+pathUpload+f"{file.filename}"
      file.save(pathFile);

      print('compressing...')
      nombre_archivo, extension = os.path.splitext(pathFile)
      #pathZip=pathRoot+file.filename.replace(extension,'.zip')
      pathZip=pathRoot+file.filename.replace(extension,format)
      with zipfile.ZipFile(pathZip, 'w') as zf:
          zf.write(pathFile,arcname=file.filename)
      print('...compression done!')


      file_data = {
        #'filename': file.filename.replace(extension,'.zip'),
        'filename': file.filename.replace(extension,format),
        'path': pathZip,
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

@app.route('/app/v1/compress/download/<upload_id>', methods=["GET", "POST"])
@jwt_required()
def index3(upload_id):
   
   return  download_file(upload_id)

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


@app.route('/register', methods=['POST'])
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
    

@app.route('/login', methods=['POST'])
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
    

