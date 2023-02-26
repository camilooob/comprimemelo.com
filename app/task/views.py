import io
from flask import render_template as render, flash, redirect, request, url_for
from flask_login import login_required, current_user
from . import eventos
from app.services import register_file, download_file, download_file_pdf
from .form import DeleteCategoryForm, RegisterCategoryForm, IdeaForm, DeleteIdeaForm, PublicIdeaForm
from app.utils import get_dict_from_wftform
from zipfile import ZipFile
from io import BytesIO, StringIO
from pathlib import Path
import zipfile
import os.path
import time  
import datetime
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity

def contextHome():
    username = current_user.id
    
    idea_form = IdeaForm()
    
    context = {
        'username': username,
        'eventos': '',
        'idea_form': idea_form,
        'delete_form': DeleteIdeaForm(),
        'public_idea_form': PublicIdeaForm(),
        'modal': {
            'insert': False,
            'update': False,
            'upload':False
        },
    }

    return context

@eventos.route('/task', methods=['GET', 'POST'])
@login_required
def task():

    flash(f"register_file registrada exitosamente.{id}", category="success")


    return render('/eventos/home.html',**context)