import os
import boto3
from botocore.exceptions import ClientError


def get_secret():

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
    print(secret)

    # Your code goes here.

class Config:
    """ Clase de configuración de flask. """
    SECRET_KEY = 'eventos secreatas de youtube'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../eventos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY= 'UatnOQmYhlfQNaINx5OX'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'franklin.pinto@gmail.com'
    MAIL_PASSWORD = 'jzlgabmqeyxvwyas'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    
get_secret()