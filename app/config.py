import os
import json
from google.cloud import storage
from google.cloud import bigquery
from google.cloud import secretmanager

def read_secret():
    # Access the secret version.
    project_id = "datacompressionprojectfjc"

    # ID of the secret to create.
    secret_name = "secretos_comprimemelo"
    resource_name = f"projects/208785026947/secrets/secretos_comprimemelo/versions/1"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": resource_name})

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    secret_comprimelo = response.payload.data.decode("UTF-8")
    #print("Plaintext: {}".format(secret_mysql))
    ##ssh variables
    secret_comprimelo_dic = json.loads(secret_comprimelo)
    #print(secret_comprimelo_dic)
    return secret_comprimelo_dic

class Config:
    
    secret_comprimelo = read_secret()
    username_c = str(secret_comprimelo['username'])
    password_c = str(secret_comprimelo['password'])
    db_host_compri_c = str(secret_comprimelo['db_host_compri'])
    db_name_c = str(secret_comprimelo['db_name'])
    db_port_c = int(secret_comprimelo['db_port'])
    jwt_secret_c = str(secret_comprimelo['jwt_secret'])
    mail_server_c = str(secret_comprimelo['mail_server'])
    mail_port_c = int(secret_comprimelo['mail_port'])
    mail_username_c = str(secret_comprimelo['mail_username'])
    mail_password_c = str(secret_comprimelo['mail_password'])

    # Your code goes here.


    """ Clase de configuración de flask. """
    mysql_connect = 'mysql://{}:{}@{}/{}'.format(username_c,password_c,db_host_compri_c,db_name_c)
    SECRET_KEY = 'eventos secreatas de youtube'
    SQLALCHEMY_DATABASE_URI = mysql_connect
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY= jwt_secret_c
    MAIL_SERVER= mail_server_c
    MAIL_PORT = mail_port_c
    MAIL_USERNAME = mail_username_c
    MAIL_PASSWORD = mail_password_c
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    