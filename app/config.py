import os
import boto3
from botocore.exceptions import ClientError
import json


class Config:

    secret_name = "rds!cluster-6b7d7cb4-5a52-4fff-9ee4-5c1bf54c7919"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    dic_secret = json.loads(secret)
    secret_name = "secret_comprimelo"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret_comprimelo = get_secret_value_response['SecretString']
    dic_secret_comprimelo = json.loads(secret_comprimelo)
    username_c = str(dic_secret['username'])
    password_c = str(dic_secret['password'])
    db_host_compri_c = str(dic_secret_comprimelo['db_host_compri'])
    db_name_c = str(dic_secret_comprimelo['db_name'])
    db_port_c = int(dic_secret_comprimelo['db_port'])
    jwt_secret_c = str(dic_secret_comprimelo['jwt_secret'])
    mail_server_c = str(dic_secret_comprimelo['mail_server'])
    mail_port_c = int(dic_secret_comprimelo['mail_port'])
    mail_username_c = str(dic_secret_comprimelo['mail_username'])
    mail_password_c = str(dic_secret_comprimelo['mail_password'])

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
    
