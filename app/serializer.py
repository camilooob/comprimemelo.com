from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .database import *

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'is_admin')
        load_instance = True

class UploadSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: Upload
        fields = ('id', 'filename_original', 'filename_compress','format_original','format_compress','type_original','type_compress','state','path','path_original','data','start_date','end_date','notified','user_id','user')
        load_intance = True
