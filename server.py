from flask import Flask, render_template, request, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import shutil
from main import translate_doc_docx_pdf, translate_txt, LANGUAGES
file = None
isTranlated = False
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'upload_files'

class UploadFileForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField("Перевести файл")
    download = SubmitField("Скачать файл")
    back = SubmitField("Вернуться")
def get_key(value):
    for k, v in LANGUAGES.items():
        if v == value:
            return k


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    global isTranlated
    global file
    form = UploadFileForm()
    if form.validate_on_submit():
        src_lang, dest_lang = 'auto', 'en'
        if request.form.get('inp_src') not in ('Автоопределение', ''):
            src_lang = get_key(request.form.get('inp_src'))
        if request.form.get('inp_dest') != '':
            dest_lang = get_key(request.form.get('inp_dest'))
        if not file:
            file = form.file.data
        if file and isTranlated:
            if form.download.data:
                return send_file('translated_upload_files/' + file.filename, as_attachment=True)
            if form.back.data:
                shutil.rmtree('translated_upload_files')
                file = None
                isTranlated = False
                return render_template('index.html', form=form, langs=list(LANGUAGES.values()), file=isTranlated)
        elif file:
            os.mkdir('upload_files')
            os.mkdir('translated_upload_files')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            if file.filename.lower().endswith('.docx') or file.filename.lower().endswith('.doc')\
                    or file.filename.lower().endswith('.pdf'):
                translate_doc_docx_pdf('upload_files/' + file.filename, dest_lang, src_lang)
            elif file.filename.lower().endswith('.txt'):
                translate_txt('upload_files/' + file.filename, dest_lang, src_lang)
            isTranlated = True
            return render_template('index.html', form=form, langs=list(LANGUAGES.values()), file=isTranlated)
        else:
            isTranlated = False
    file = None
    isTranlated = False
    return render_template('index.html', form=form, langs=list(LANGUAGES.values()), file=isTranlated)


if __name__ == '__main__':
    app.run(debug=True)
