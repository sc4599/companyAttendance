# coding:utf-8


import xlrd
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config
import xlrd
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
db = SQLAlchemy(app)


class Detail_attendance(db.Model):
    __tablename__ = 'detail_attendance'
    _id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    gong_hao = db.Column(db.Integer)
    name = db.Column(db.String(64))
    department = db.Column(db.String(128))
    month_attendance = db.Column(db.DateTime)
    ban_ci = db.Column(db.String(64), default='正常班')
    attendance_record = db.Column(db.String(64))
    working_hours = db.Column(db.Integer)
    late = db.Column(db.String(64))
    leave_early = db.Column(db.String(64))
    add_working = db.Column(db.String(64))
    field_personnel = db.Column(db.String(64))
    vacation = db.Column(db.String(64))
    tiao_xiu = db.Column(db.String(64))
    absenteeisma = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r %r %r %r %r %r %r %r>' % \
               (self.department, self.id, self.name, self.month_attendance, self.late, self.absenteeisma)


class User2(db.Model):
    __tablename__ = 'User2'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    department = db.Column(db.String(128), unique=True)
    bing_jia = db.Column(db.Integer)
    bu_ka = db.Column(db.Integer)
    gong_chu = db.Column(db.Integer)
    hun_jia = db.Column(db.Integer)
    nian_jia = db.Column(db.Integer)
    pei_chan_jia = db.Column(db.Integer)
    shi_jia = db.Column(db.Integer)
    tiao_xiu = db.Column(db.Integer)
    late_count = db.Column(db.Integer)
    backup = db.Column(db.Integer)

    @property
    def is_full(self):
        if (self.bing_jia + self.bu_ka + self.gong_chu + self.gong_chu + self.hun_jia + self.nian_jia +
                self.pei_chan_jia + self.shi_jia + self.tiao_xiu + self.late_count + self.late_count) > 0:
            return False
        else:
            return True

    @property
    def full_bonus(self):
        if self.is_full:
            return 100
        else:
            return 0


xml_data = xlrd.open_workbook('excel/1-31.xls')


def create_user(user_id=None, name=None, department=None, month_attendance=None, attendance_record=None,
                working_hours=None,
                late=None, ):
    pass


def get_excel_data():
    excel_data = xlrd.open_workbook('excel/1-31.xls')  # 打开指定 excel
    excel_table = excel_data.sheets()[0]
    rows = excel_table.nrows
    print ('rows = ', rows)
    print  excel_table.row_values(4961)[0]

    key_list = ['department', 'gong_hao', 'name', 'month_attendance', 'ban_ci','attendance_record', 'working_hours',
                'late', 'leave_early', 'add_working', 'field_personnel', 'vacation', 'tiao_xiu', 'absenteeisma']
    tmp = []
    for i in range(1, rows - 1):
        # u = Detail_attendance()
        item = dict()
        for j in range(14):
            value = excel_table.cell(i,j).value
            key = key_list[j]

            if key in ['name', 'department','ban_ci','absenteeisma','working_hours',]:
                pass
            if key is 'working_hours' and value:
                try:
                    value = int(float(value)*10)
                except :
                    print 'try = ',value
            if not value:
                value = 0
            item[key] = value
        print item
        tmp.append(item)

    db.session.execute(
        Detail_attendance.__table__.insert(), tmp)
    db.session.commit()


    for i in range(1, rows - 1):
        pass


if __name__ == '__main__':
    # db.create_all()
    get_excel_data()
    pass
