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
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
        return '<User %r %r %r %r %r %r >' % \
               (self.department, self._id, self.name, self.month_attendance, self.late, self.absenteeisma)


class User2(db.Model):
    __tablename__ = 'User2'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gong_hao = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(64), unique=True)
    department = db.Column(db.String(128))
    bing_jia = db.Column(db.Integer, default=0)
    bu_ka = db.Column(db.Integer, default=0)
    gong_chu = db.Column(db.Integer, default=0)
    hun_jia = db.Column(db.Integer, default=0)
    nian_jia = db.Column(db.Integer, default=0)
    pei_chan_jia = db.Column(db.Integer, default=0)
    shi_jia = db.Column(db.Integer, default=0)
    tiao_xiu = db.Column(db.Integer, default=0)
    false_late = db.Column(db.Integer, default=0)
    real_late = db.Column(db.Integer, default=0)
    backup = db.Column(db.Integer, default=0)

    @property
    def is_full(self):
        if (self.bing_jia + self.bu_ka + self.gong_chu + self.gong_chu + self.hun_jia + self.nian_jia +
                self.pei_chan_jia + self.shi_jia + self.tiao_xiu + self.false_late + self.real_late) > 0:
            return False
        else:
            return True

    @property
    def full_bonus(self):
        if self.is_full:
            return 100
        else:
            return 0

    @property
    def late_counts(self):
        return self.real_late + self.false_late


xml_data = xlrd.open_workbook('excel/1-31.xls')


def create_user(user_id=None, name=None, department=None, month_attendance=None, attendance_record=None,
                working_hours=None,
                late=None, ):
    pass


def get_excel_data_to_mysql(path):
    excel_data = xlrd.open_workbook(path)  # 打开指定 excel
    excel_table = excel_data.sheets()[0]
    rows = excel_table.nrows
    print ('rows = ', rows)
    print excel_table.row_values(4961)[0]

    key_list = ['department', 'gong_hao', 'name', 'month_attendance', 'ban_ci', 'attendance_record', 'working_hours',
                'late', 'leave_early', 'add_working', 'field_personnel', 'vacation', 'tiao_xiu', 'absenteeisma']
    tmp = []  # 用于保存所有
    for i in range(1, rows - 1):
        # u = Detail_attendance()
        item = dict()
        for j in range(14):
            value = excel_table.cell(i, j).value
            key = key_list[j]

            if key in ['name', 'department', 'ban_ci', 'absenteeisma', 'working_hours', ]:
                pass
            if key is 'working_hours' and value:
                try:
                    value = int(float(value) * 10)
                except:
                    print 'try = ', value
            if not value:
                value = 0
            item[key] = value
        print item
        tmp.append(item)
    # 批量执行插入动作
    db.session.execute(Detail_attendance.__table__.insert(), tmp)
    db.session.commit()


def from_detail_to_user2():
    d = db.session.query(Detail_attendance)
    is_change = False

    users = User2.query.filter().all()
    userdict = dict()
    for u in users:
        userdict[u.gong_hao] = u

    for detail_a in list(d):
        u = userdict.get(detail_a.gong_hao)
        if is_sun_or_saturdays(detail_a.month_attendance):
            continue

            # 判断是否补卡
            # print detail_a.vacation
            # print type(detail_a.vacation)
        if u'补'.endswith(detail_a.vacation[0]):
            # print u.name, 'bu_ka', detail_a.month_attendance
            last_count = u.bu_ka
            u.bu_ka = last_count + 1
            is_change = True

        # 计算病假时间
        if u'病'.endswith(detail_a.vacation[0]):
            bing_jia_time = int(
                float(detail_a.vacation[detail_a.vacation.find('(') + 1:detail_a.vacation.find(')')]) * 10)
            # print u.name, 'bing_jia', detail_a.month_attendance, 'time=',bing_jia_time
            last_bing_jia_time = u.bing_jia
            u.bing_jia = last_bing_jia_time + bing_jia_time
            is_change = True

        # 计算婚假时间
        if u'婚'.endswith(detail_a.vacation[0]):
            hun_jia_time = int(
                float(detail_a.vacation[detail_a.vacation.find('(') + 1:detail_a.vacation.find(')')]) * 10)
            print u.name, 'hun_jia', detail_a.month_attendance, 'time=', hun_jia_time
            last_hun_jia_time = u.hun_jia
            u.hun_jia = last_hun_jia_time + hun_jia_time
            is_change = True

        # 计算年假时间
        if u'婚'.endswith(detail_a.vacation[0]):
            nian_jia_time = int(
                float(detail_a.vacation[detail_a.vacation.find('(') + 1:detail_a.vacation.find(')')]) * 10)
            print u.name, 'nian_jia', detail_a.month_attendance, 'time=', nian_jia_time
            last_nian_jia_time = u.nian_jia
            u.nian_jia = last_nian_jia_time + nian_jia_time
            is_change = True

        # 计算事假时间
        if u'事'.endswith(detail_a.vacation[0]):
            shi_jia_time = int(
                float(detail_a.vacation[detail_a.vacation.find('(') + 1:detail_a.vacation.find(')')]) * 10)
            print u.name, 'nian_jia', detail_a.month_attendance, 'time=', shi_jia_time
            last_shi_jia_time = u.shi_jia
            u.shi_jia = last_shi_jia_time + shi_jia_time
            is_change = True

        # 计算调休时间
        if u'调'.endswith(detail_a.vacation[0]):
            tiao_xiu_time = int(
                float(detail_a.vacation[detail_a.vacation.find('(') + 1:detail_a.vacation.find(')')]) * 10)
            print u.name, 'nian_jia', detail_a.month_attendance, 'time=', tiao_xiu_time
            last_tiao_xiu_time = u.tiao_xiu
            u.tiao_xiu = last_tiao_xiu_time + tiao_xiu_time
            is_change = True

        attendance_record = detail_a.attendance_record.split(' ')
        if len(attendance_record) is 2:
            # 上下班全部打卡的
            morning = attendance_record[0].split("-")[0]
            afternoon = attendance_record[1].split("-")[1]
            # 迟到判定 (减工时)
            if is_false_late(str_to_datetime(morning)):
                # print u.name, 'false_late', morning
                last_count = u.false_late
                if detail_a.vacation != '0':
                    # print u.name, 'false_late', morning, detail_a.vacation
                    last_count = u.false_late - 1
                u.false_late = last_count + 1
                is_change = True
            if is_real_late(str_to_datetime(morning)):
                # print u.name, 'real_late', morning, detail_a.month_attendance
                last_count = u.real_late
                if detail_a.vacation != '0':
                    # print u.name, 'real_late', morning, detail_a.vacation
                    last_count = u.real_late - 1
                u.real_late = last_count + 1
                is_change = True

            # 早退判定 (减工时)
            if is_leave_early(str_to_datetime(afternoon)):
                pass

        if attendance_record[0].split('-')[0].startswith("xx"):
            # 早上忘记刷卡的
            continue
        else:
            # 下班忘记刷卡的
            pass

        if is_change:
            db.session.add(u)
            is_change = False

    db.session.commit()


def clear_user2():
    db.session.query(User2).filter().update(
        {User2.false_late: 0, User2.real_late: 0, User2.bu_ka: 0, User2.bing_jia: 0, User2.hun_jia: 0,
         User2.nian_jia: 0, User2.shi_jia: 0, User2.tiao_xiu: 0})
    db.session.commit()


def generate_users():
    d = db.session.query(Detail_attendance)
    print list(d)
    tmp = []  # 用于保存所有用户
    filter_id = []
    for detail_a in list(d):
        item = dict()
        if detail_a.gong_hao in filter_id:
            continue
        else:
            filter_id.append(detail_a.gong_hao)
        item['gong_hao'] = detail_a.gong_hao
        item['name'] = detail_a.name
        item['department'] = detail_a.department
        tmp.append(item)
        print item
    db.session.execute(User2.__table__.insert(), tmp)
    db.session.commit()


def is_sun_or_saturdays(month_attendance):
    if not isinstance(month_attendance, datetime.datetime):
        return False
    if month_attendance.weekday() is 6 or month_attendance.weekday() is 5:
        return True
    else:
        return False


def is_false_late(minutes):
    if minutes > 9 * 60 and minutes <= 9 * 60 + 10:
        return True
    else:
        return False


def is_real_late(minutes):
    if minutes > 9 * 60 + 10:
        return True
    else:
        return False


def is_leave_early(minutes):
    if minutes < 18 * 60 + 30:
        return True
    else:
        return False


def str_to_datetime(str_datetime):
    if str_datetime.startswith(u'次日'):
        str_datetime = str_datetime[2:]
    hour = int(str_datetime.split(':')[0])
    minute = int(str_datetime.split(':')[1])
    return hour * 60 + minute


def test_is_real():
    details = Detail_attendance.query.filter(Detail_attendance.gong_hao == 835).all()
    for itme in details:
        if is_sun_or_saturdays(itme.month_attendance):
            continue
        testtime = itme.attendance_record.split(" ")[0].split('-')[0]
        print testtime
        print is_false_late(str_to_datetime(testtime))
        print is_real_late(str_to_datetime(testtime))


def output_cvs():
    users = list(db.session.query(User2))
    key_list = ','.join([u'姓名', u'设备工号', u'十分钟内迟到', u'十分钟后迟到', u'病假', u'补卡', u'公出', u'婚假', u'年假', u'产假',
                u'陪产假', u'流产假', u'事假', u'调休', u'是否全勤'])
    tmp = [key_list]
    for u in users:
        tmp_user = [u.name, str(u.gong_hao), str(u.false_late), str(u.real_late), str(float(u.bing_jia)/10),
                    str(u.bu_ka), '', str(float(u.hun_jia)/10), str(float(u.nian_jia)/10), '',
                    '', '', str(float(u.shi_jia)/10), str(float(u.tiao_xiu)/10), u'是' if u.is_full else u'否']
        tmp.append(','.join(tmp_user))
    with open('test_cvs.csv', mode='w') as f:
        f.write('\n'.join(tmp).encode('gb18030'))


if __name__ == '__main__':
    # db.create_all()
    # get_excel_data_to_mysql('excel/1-31.xls')
    # generate_users()  # generate  user  information
    # from_detail_to_user2()
    # clear_user2()
    # details = Detail_attendance.query.filter(Detail_attendance.name == u'陈强胜').all()
    # for item in details:
    #     if u'0' == item.vacation:
    #         continue
    #     print item.vacation[0]
    #     print item.vacation[item.vacation.find('(')+1:item.vacation.find(')')]

    # test_is_real()
    output_cvs()
    pass
