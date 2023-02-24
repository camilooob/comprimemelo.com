from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, HiddenField, BooleanField, SelectField,DateField
from wtforms.validators import DataRequired, Length
from wtforms import validators

class DeleteCategoryForm(FlaskForm):
    """ Form eliminar categorias. """
    submit = SubmitField("Eliminar")

class RegisterCategoryForm(FlaskForm):
    """ Form para registrar categoria. """
    name = StringField("Categoria", validators=[DataRequired(), Length(min=2, max=15)])

    submit = SubmitField("Registrar")

class IdeaForm(FlaskForm):
    """ Form de Eventos. """
    id = HiddenField()
    title = StringField("Nombre", validators=[DataRequired(), Length(min=5, max=50)])
    description = StringField("Dirección", validators=[DataRequired(), Length(min=10, max=250)])
    site = StringField("Lugar", validators=[DataRequired(), Length(min=10, max=100)])
    startDate=DateField("Fecha Inicio", format='%m/%d/%Y', validators=(validators.Optional(),))
    endDate=DateField("Fecha Fin", format='%m/%d/%Y', validators=(validators.Optional(),))
    is_public = BooleanField("Pública")
    modality = BooleanField("Presencial")
    category_id = SelectField("Categoria", validators=[DataRequired()])

    submit = SubmitField("Enviar")


class DeleteIdeaForm(FlaskForm):
    """ Form para eliminar Evento. """
    submit = SubmitField("")


class PublicIdeaForm(FlaskForm):
    """ Form para cambiar el estado de un evento. """
    submit = SubmitField("")