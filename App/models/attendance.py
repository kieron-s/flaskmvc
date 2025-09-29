from App.database import db
from .user import User 

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)
    clock_in = db.Column(db.DateTime)
    clock_out = db.Column(db.DateTime)

    staff = db.relationship('User', backref=db.backref('attendances', lazy=True))
    shift = db.relationship('Shift', backref=db.backref('attendances', lazy=True))

    def __init__(self, staff_id, shift_id, clock_in=None, clock_out=None):
        self.staff_id = staff_id
        self.shift_id = shift_id
        self.clock_in = clock_in
        self.clock_out = clock_out
        
    @staticmethod
    def staff_checkin(staff_id, shift_id):
        from App.models import Shift
        from datetime import datetime
        staff = db.session.get(User, staff_id)
        shift = db.session.get(Shift, shift_id)
        if not staff or not shift:
            return "Invalid staff or shift."
        attendance_record = Attendance.query.filter_by(staff_id=staff_id, shift_id=shift_id, clock_out=None).first()
        if attendance_record:
            return "Already checked in and not checked out."
        new_attend = Attendance(staff_id=staff_id, shift_id=shift_id, clock_in=datetime.now())
        db.session.add(new_attend)
        message = f"{staff.username} checked in to shift on {shift.day} from {shift.start_time} to {shift.end_time}."
        db.session.commit()
        return message

    @staticmethod
    def staff_checkout(staff_id, shift_id):
        from App.models import Shift
        from datetime import datetime
        staff = db.session.get(User, staff_id)
        shift = db.session.get(Shift, shift_id)
        if not staff or not shift:
            return "Invalid staff or shift."
        attendance_record = Attendance.query.filter_by(staff_id=staff_id, shift_id=shift_id, clock_out=None).first()
        if not attendance_record:
            return "No check-in found for this shift."
        attendance_record.clock_out = datetime.now()
        message = f"{staff.username} checked out of their shift on {shift.day} from {shift.start_time} to {shift.end_time}."
        db.session.commit()
        return message