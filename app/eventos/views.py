import io
from flask import render_template as render, flash, redirect, request, url_for
from flask_login import login_required, current_user
from . import eventos
from app.services import get_Category_by_id, delete_category, create_category, list_categories, list_eventos_by_username, create_idea, delete_idea_db, update_state_idea_db, update_idea_db, get_idea_by_id, register_file, download_file, download_file_pdf
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
def contextHome():
    username = current_user.id
    categories = [(c["id"], c["name"]) for c in list_categories() ]
    idea_form = IdeaForm()
    idea_form.category_id.choices = [("", "--seleccione categoria --") ] + categories
    context = {
        'username': username,
        'eventos': list_eventos_by_username(username),
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

@eventos.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    categories = list_categories()
    register_form = RegisterCategoryForm()
    context = {
        'register_form': register_form,
        'delete_form': DeleteCategoryForm(),
        'categories': categories
    }

    if register_form.validate_on_submit():
        create_category(register_form.name.data)
        flash("Categoria registrada exitosamente.", category="success")

        return redirect(url_for('eventos.categories'))        

    return render('eventos/categories.html', **context)

@eventos.route('/category/delete/<category_id>', methods=['POST'])
@login_required
def delete_category_view(category_id):
    delete_category(category_id)
    flash("Categoria eliminada", category="success")   

    return redirect(url_for('eventos.categories')) 


@eventos.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    """ Método para retornar al home de la aplicación. """
    context = contextHome()
    idea_form = context["idea_form"]
    if idea_form.validate_on_submit():
        form_dict = get_dict_from_wftform(idea_form)
        form_dict['username'] = context['username']
        if idea_form.id.data == "":
            create_idea(form_dict)
            flash("eventos creada.", category="success")
            return redirect(url_for('eventos.home'))
        else:
            update_idea_db(form_dict)
            flash("Idea actualizada correctamente !!", category="success")
            return redirect(url_for("eventos.home"))
        
    return render('eventos/home.html', **context)

@eventos.route('/insert')
@login_required
def inserteventos_view():
    context = contextHome()
    context["modal"] = {
        "insert": True,
        "udpate": False
    }

    return render('eventos/home.html', **context)


@eventos.route('/compressFile')
@login_required
def compressFile_view():
    context = contextHome()
    context["modal"] = {
        "insert": False,
        "udpate": False,
        "upload": True
    }
    return render('eventos/home.html', **context)

@eventos.route('/comprimir')
@login_required
def comprimir():
    
    return render('/eventos/homeUpload.html')

@eventos.route('/compress', methods=['GET', 'POST'])
#@login_required
def compress():
    
    file = request.files['file']
    format=request.form.get('format')
    
    print(f'format...{format}')

    pathRoot=os.path.abspath(os.curdir)+"/"
    pathUpload=f"uploads/"
    pathFile=pathRoot+pathUpload+f"{file.filename}"
    file.save(pathFile);
    
    print('compressing...')
    nombre_archivo, extension = os.path.splitext(pathFile)
    pathZip=pathRoot+file.filename.replace(extension,format)
    with zipfile.ZipFile(pathZip, 'w') as zf:
     zf.write(pathFile,arcname=file.filename)
    print('...compression done!')


    file_data = {
                'filename': file.filename.replace(extension,format),
                'path': pathZip,
                'state': 'COMPRIMIDO',
                'notified': False,
                'startDate': datetime.datetime.utcnow(),                
                'endDate': datetime.datetime.utcnow(),    
                'data': file.read(),
                'username':'fpintoc'
            }
    id=register_file(file_data)

    flash(f"register_file registrada exitosamente.{id}", category="success")

    context = contextHome()
    context["modal"] = {
        "insert": False,
        "udpate": False,
        "upload": True
    }

    return render('/eventos/home.html',**context)

def _walk(path: Path) -> []:
    all_files = []
    for x in path.iterdir():
        if x.is_dir():
            all_files.extend(_walk(x))
        else:
            all_files.append(x)
    return all_files


def zip_files(path: Path, archive_name: str):
    all_files = _walk(path)
    with zipfile.ZipFile(f'{archive_name}', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in all_files:
            zipf.write(f)
        zipf.close()

@eventos.route('/download/<upload_id>')
#@login_required
def download():
    print('leyendo archivo...')
    download_file_pdf(4)
    
    flash("register_file descargado exitosamente.", category="success")

    

    return render('index.html')


@eventos.route('/delete_idea/<idea_id>', methods=['POST'])
@login_required
def delete_idea(idea_id):
    delete_idea_db(idea_id)
    flash("Idea eliminada exitosamente", category="success")
    
    return redirect(url_for("eventos.home"))

@eventos.route('/public_idea/<idea_id>/<int:is_public>', methods=['POST'])
@login_required
def public_idea(idea_id, is_public):
    update_state_idea_db(idea_id, is_public)
    flash("Idea actualizada exitosamente !!", category="success")

    return redirect(url_for("eventos.home"))

@eventos.route('/update_idea/<idea_id>', methods=['POST'])
@login_required
def update_idea(idea_id):
    context = contextHome()
    idea_form = context["idea_form"]

    idea = get_idea_by_id(idea_id)
    idea_form.id.data = idea.id
    idea_form.title.data = idea.title
    idea_form.description.data = idea.description
    idea_form.site.data = idea.site
    idea_form.startDate.data = idea.startDate
    idea_form.endDate.data = idea.endDate
    idea_form.is_public.data = idea.is_public
    idea_form.modality.data = idea.modality
    idea_form.category_id.data = idea.category_id

    context["idea_form"] = idea_form
    context["modal"] = {
        'insert': False,
        'update': True
    }

    return render('eventos/home.html', **context)
