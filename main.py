from flask import render_template as render, flash, send_from_directory, request
from app import create_app
from app.migrate import init_db
from app.services import list_public_eventos, download_file, download_file, download_file_pdf,register_file
import zipfile
import os.path
import time  
import datetime

app = create_app()

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

@app.route('/app/v1/upload',methods=['POST'])
def index4():
      url_params = request.args
  
    # Retrieve parameters which are present
      format = url_params['format']

      print(f'compressing...{format}')
      file = request.files['file']
      pathRoot=f"C:/Users/Franklin pinto/Documents/Uniandes/semestre 2/Desarrollo aplicaciones cloud/comprimemelo.com/"
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

@app.route('/app/v1/download/<upload_id>', methods=["GET", "POST"])
def index3(upload_id):
   
   return  download_file(upload_id)

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



