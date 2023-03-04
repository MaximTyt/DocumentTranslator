from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from main import read_doc_and_docx, LANGUAGES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'upload_files'

class UploadFileForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField("Upload File")

def get_key(value):
    for k,v in LANGUAGES.items():
        if v == value:
            return k


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        src_lang, dest_lang = 'auto', 'en'
        if request.form.get('inp_src') not in ('Автоопределение', ''):
            src_lang = get_key(request.form.get('inp_src'))
        if request.form.get('inp_dest') != '':
            dest_lang = get_key(request.form.get('inp_dest'))
        file = form.file.data
        if file:
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                   file.filename))
            if file.filename.lower().endswith('.docx') or file.filename.lower().endswith('.doc'):
                read_doc_and_docx('upload_files/' + file.filename, dest_lang, src_lang)

            return "Файл был переведён успешно!"
    return render_template('index.html', form=form, langs=list(LANGUAGES.values()))


if __name__ == '__main__':
    app.run(debug=True)
