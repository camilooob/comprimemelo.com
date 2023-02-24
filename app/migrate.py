from .database import *

def create_db():
    """ Método de creación de la base de datos. """
    db.drop_all()
    db.create_all()

# Function to initialize the database from a script.
def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        with db.cursor() as cursor:
            cursor.execute(f.read(), multi=True)
        db.commit()
    db.session.commit()