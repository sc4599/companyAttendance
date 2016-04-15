# coding:utf-8
from app import create_app
from app.attendance.forms import FileUploadForm
from flask import render_template, request, flash
import app.attendance.readexcel as excel
import os
import datetime

app = create_app()


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


@app.route("/download", methods=("GET", "POST",))
def download():
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
    form = FileUploadForm()

    if f:
        if not allowed_file(f.filename):
            flash('please make sure file type (only .xls) !')
            return render_template('upload.html', form=form)
        f.save(os.path.join(app.root_path, "static/uploads", f.filename))
        # 将 excel数据存入数据库
        excel.get_excel_data_to_mysql("%s/static/uploads/%s" % (app.root_path, f.filename))
        # 清空user2
        excel.clear_user2()
        # 将数据写入 user2
        excel.from_detail_to_user2()
        # 将user2 数据生成CVS
        excel.output_cvs('%s/static/generate/' % app.root_path, str(datetime.date.today()))
        print 'upload succeed'
        # with open('excel/%s'%f.filename,mode='r') as f:
        return render_template("download.html", filename = str(datetime.date.today()))
    else:
        flash('please take file input !')
        return render_template('upload.html', form=form)


@app.route("/test", methods=("GET",))
def test():
    return render_template("base.html")


@app.route("/createdb")
def create_db():
    excel.db.create_all()
    return 'yes'


@app.route("/createUser2")
def create_user2():
    excel.generate_users()
    return 'yes'


if __name__ == "__main__":
    app.run('0.0.0.0')
