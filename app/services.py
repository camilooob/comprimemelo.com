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
        filenameOriginal =file_data['filenameOriginal'],
        filenameCompress =file_data['filenameCompress'],
        formatOriginal =file_data['formatOriginal'],
        formatCompress =file_data['formatCompress'],
        mimeTypeOriginal =file_data['mimeTypeOriginal'],
        mimeTypeCompress =file_data['mimeTypeCompress'],
        path=file_data['path'],
        pathOriginal=file_data['pathOriginal'],
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
    return send_file(BytesIO(upload.data),  mimetype=upload.mimeTypeCompress, download_name=upload.filenameCompress )

def download_file(upload_id):

    upload = Upload.query.filter_by(id=upload_id).first()
    print(upload.path)
    with open(upload.path, 'rb') as obFile:
    
        my_local_data = obFile.read()

    return send_file(BytesIO(my_local_data),  mimetype=upload.mimeTypeCompress, download_name=upload.filenameCompress )
    


def download_file_original(filename):
    print(filename)
    upload = Upload.query.filter_by(pathOriginal=filename).first()
    print(upload.pathOriginal)
    with open(upload.pathOriginal, 'rb') as obFile:
    
        my_local_data = obFile.read()

    return send_file(BytesIO(my_local_data),  mimetype=upload.mimeTypeOriginal, download_name=upload.filenameOriginal )


