from flask import render_template as render, flash, send_from_directory
from app import create_app
from app.migrate import init_db
from app.services import list_public_eventos

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


@app.route('/app/v1/users')
def user_actions():
    print("estoy aca")
    return "funcionado..."

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