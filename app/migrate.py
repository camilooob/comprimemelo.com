from .database import *

def create_db():
    """ Método de creación de la base de datos. """
    db.drop_all()
    db.create_all()

def init_db():
    """ Método de inicialización de nuestra base de datos. """
    create_db()
    # user admin app
    admin = User(
        name="Franklin",
        lastName="Pinto",
        username="fpintoc",
        email="franklin.pinto@gmail.com",
        is_admin=True,
        cellphone="3187678086",
    )
    admin.set_password("mono2023")
    db.session.add(admin)
    db.session.commit()