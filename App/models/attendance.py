from App.database import db
from .staff import Staff

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)
    clock_in = db.Column(db.DateTime)
    clock_out = db.Column(db.DateTime)


    staff = db.relationship('Staff', backref=db.backref('attendances', lazy=True))
    shift = db.relationship('Shift', backref=db.backref('attendances', lazy=True))

    def __init__(self, staff_id, shift_id, clock_in=None, clock_out=None):
        self.staff_id = staff_id
        self.shift_id = shift_id
        self.clock_in = clock_in
        self.clock_out = clock_out
        
    def check_in(self, staff_id, clock_in_time):
        attendance_record = Attendance.query.filter_by(staff_id=staff_id, clock_out=None).first()
        if attendance_record:
            raise ValueError("Staff member has already checked in and not checked out yet.")
        self.clock_in = clock_in_time
        db.session.add(self)
        db.session.commit()

    def check_out(self, staff_id, clock_out_time):
        attendance_record = Attendance.query.filter_by(staff_id=staff_id, clock_out=None).first()
        if not attendance_record:
            raise ValueError("No active check-in record found for this staff member.")
        attendance_record.clock_out = clock_out_time
        db.session.commit()