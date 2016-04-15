# coding=utf-8
from app.attendance.readexcel import db



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
