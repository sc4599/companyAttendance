from readxml import db


class detail_attendance(db.Model):
    __tablename__ = 'detail_attendance'
    id = db.Column(primary_key=True)
    name = db.Column(db.String(64), unique=True)
    department = db.Column(db.String(128), unique=True)
    month_attendance = db.Column(db.DateTime)
    ban_ci = db.Column(db.String(64))
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
    bing_jia = db.Column(db.Integer(64))
    bu_ka = db.Column(db.Integer(64))
    gong_chu = db.Column(db.Integer(64))
    hun_jia = db.Column(db.Integer(64))
    nian_jia = db.Column(db.Integer(64))
    pei_chan_jia = db.Column(db.Integer(64))
    shi_jia = db.Column(db.Integer(64))
    tiao_xiu = db.Column(db.Integer(64))
    late_count = db.Column(db.Integer(64))
    backup = db.Column(db.Integer(64))

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