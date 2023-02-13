from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .database import *

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: User
        fields = ('id', 'name', 'lastName', 'username', 'email', 'password', 'is_admin', 'cellphone', 'avatar',)
        load_instance = True

class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model: Category
        fields = ('id', 'name',)
        load_intance = True

class eventoschema(SQLAlchemyAutoSchema):
    class Meta:
        model: Idea
        fields = ('id', 'title', 'description','site','startDate','endDate', 'is_public', 'modality','category_id', 'category', 'user_id', 'user', )
        include_relationships = True
        load_instance = True