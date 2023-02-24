from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext
import os
import boto3
from botocore.exceptions import ClientError
import json

# Function to create a database connection.
def get_db():

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
    if 'db' not in g:
        g.db=mysql.connector.connect(host=db_host_compri_c,user=username_c,password=password_c,database=db_name_c)
    return g.db

# Function to close an existing database connection.
def close_db(e=None):
    db=g.pop('db',None)
    if db is not None:
        db.close()

# Function to initialize the database from a script.
def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        with db.cursor() as cursor:
            cursor.execute(f.read(), multi=True)
        db.commit()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Upload(db.Model):
    __tablename__ = 'upload'
    
    id = db.Column(db.Integer, primary_key=True)
    filename_original = db.Column(db.String(200))
    filename_compress = db.Column(db.String(200))
    format_original = db.Column(db.String(10))
    format_compress = db.Column(db.String(10))
    type_original = db.Column(db.String(100))
    type_compress = db.Column(db.String(100))
    state = db.Column(db.String(50))
    path = db.Column(db.String(1000))
    path_original = db.Column(db.String(1000))
    data = db.Column(db.LargeBinary)
    start_date = db.Column(db.DateTime(100), nullable=False)
    end_date = db.Column(db.DateTime(100), nullable=False)
    notified = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('upload', lazy=True))



