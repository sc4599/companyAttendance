from manager import app
from forms import FileUploadForm
from flask import render_template,request,flash
import os


@app.route('/upload', methods='POST')
def upload_file():
    form = FileUploadForm()
    if form.validate_on_submit():
        filename = form.excel_file.data.filename
        print filename


@app.route("/", methods=("GET", "POST",))
def index():
    form = FileUploadForm()

    filedata = []

    if form.validate_on_submit():
        print 'form.validate !!!'
        for upload in form.uploads.entries:
            filedata.append(upload)
        print len(filedata)

    for file1 in filedata:
        print file1.data.filename

    return render_template("index.html", form=form, filedata=filedata)


@app.route("/kaoqin", methods=("GET", "POST",))
def kaoqin():
    print 'this is index ()'
    form = FileUploadForm()
    filedata = []
    if form.validate_on_submit():
        for upload in form.uploads.entries:
            filedata.append(upload)
    return render_template("download.html", form=form)


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route("/upload", methods=("GET", "POST",))
def upload():
    f = request.files.get('upload')
    if f and allowed_file(f.filename):
        try:
            f.save(os.path.join(app.root_path, "static/uploads", f.filename))
            print 'upload succeed'
        except:
            print 'upload error'
        # with open('excel/%s'%f.filename,mode='r') as f:
        return render_template("download.html", filename=f.filename)
    else:
        flash('please take file input !')
        return render_template('download.html')