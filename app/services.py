from .database import *
from .serializer import *
from .utils import remove_pictute_profile
from flask import Flask, render_template, request, send_file
from io import BytesIO

def get_user_by_username(username):
    """ Método para retornar el usuario a partir del username. """
    return User.query.filter_by(username=username).first()

def register_user(user_data):
    """ Método para registrar un usuario nuevo en la base de datos. """
    user = User(
        name=user_data['name'],
        lastName=user_data['lastName'],
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'],
        cellphone=user_data['cellphone'],
    )
    user.set_password(user_data['password'])

    db.session.add(user)
    db.session.commit()

def register_file(file_data):
    """ Método para registrar un archivo nuevo en la base de datos. """
    user = get_user_by_username(
        file_data['username']
    )

    upload = Upload(
        filename =file_data['filename'],
        path=file_data['path'],
        state=file_data['state'],
        data=file_data['data'],
        startDate=file_data['startDate'],
        endDate=file_data['endDate'],
        notified=file_data['notified'],
        user=user
    )
    db.session.add(upload)
    db.session.commit()
    
    return upload.id

def download_file_pdf(upload_id):
    #upload = Upload.query.get(1)
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data),  mimetype="application/pdf", download_name=upload.filename )

def download_file(upload_id):

    upload = Upload.query.filter_by(id=upload_id).first()
    print(upload.path)
    with open(upload.path, 'rb') as obFile:
    
        my_local_data = obFile.read()

    return send_file(BytesIO(my_local_data),  mimetype="application/zip", download_name=upload.filename )
    


def get_Category_by_id(category_id):
    """ Método para busar categoria por id. """
    return Category.query.get(category_id)

def delete_category(category_id):
    category = get_Category_by_id(category_id)

    db.session.delete(category)
    db.session.commit()

def create_category(name):
    """ Método para crear una categoría. """
    category = Category(name=name)

    db.session.add(category)
    db.session.commit()

def list_categories():
    """ Método para obtener el listado de categorias. """
    schema = CategorySchema()
    data = Category.query.all()
    categories = [schema.dump(c) for c in data]

    return categories

def get_idea_by_id(idea_id):
    """ Método para obtener evento por id. """
    return Idea.query.get(idea_id)

def create_idea(idea_data):
    """ Método para crear un evento en la db. """
    user = get_user_by_username(
        idea_data['username']
    )

    category = get_Category_by_id(
        idea_data['category_id']
    )

    idea = Idea(
        title=idea_data["title"],
        description=idea_data["description"],
        site=idea_data["site"],
        startDate=idea_data["startDate"],
        endDate=idea_data["endDate"],
        is_public=idea_data["is_public"],
        modality=idea_data["modality"],
        category=category,
        user=user,
    )

    db.session.add(idea)
    db.session.commit()

def list_eventos_by_username(username):
    """ Método para listar evento por nombre de usuario. """
    user = get_user_by_username(username)
    schema = eventoschema()
    data = Idea.query.filter_by(user=user)
    eventos = [schema.dump(i) for i in data]
    
    return eventos


def delete_idea_db(idea_id):
    """ Método para eliminar un evento. """
    idea = get_idea_by_id(idea_id)

    db.session.delete(idea)
    db.session.commit()

def update_state_idea_db(idea_id, state):
    """ Método apta cambiar el estado de un evento. """
    idea = get_idea_by_id(idea_id)
    idea.is_public = not bool(state)

    db.session.commit()

def update_idea_db(idea_data):
    """ Método para actualizar un evento. """
    category = get_Category_by_id(
    idea_data['category_id']
    )
    idea = get_idea_by_id(idea_data['id'])

    idea.title = idea_data["title"]    
    idea.description = idea_data["description"]
    idea.site = idea_data["site"]
    idea.startDate = idea_data["startDate"]
    idea.endDate = idea_data["endDate"]
    idea.is_public = idea_data["is_public"]
    idea.modality = idea_data["modality"]
    idea.category = category

    db.session.commit()

def update_profile_picture(username, picture_name_new):
    """ Método para actualizar la foto de perfil del usuario. """
    user = get_user_by_username(
        username
    )
    if user.avatar is not None:
        remove_pictute_profile(user.avatar)
    
    user.avatar = picture_name_new

    db.session.commit()


def list_public_eventos():
    """ Método para obtener listado de eventos, """
    data = Idea.query.filter_by(is_public=True).order_by(Idea.startDate)
    schema = eventoschema()
    public_eventos = [schema.dump(i) for i in data]

    return public_eventos