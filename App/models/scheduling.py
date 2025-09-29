from App.database import db

class Scheduling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)

    staff = db.relationship('Staff', backref=db.backref('schedules', lazy=True))
    shift = db.relationship('Shift', backref=db.backref('schedules', lazy=True))

    def __init__(self, staff_id, shift_id):
        self.staff_id = staff_id
        self.shift_id = shift_id

    def assign_shift(self, staff_id, shift_id):
        existing_schedule = Scheduling.query.filter_by(staff_id=staff_id, shift_id=shift_id).first()
        if existing_schedule:
            raise ValueError("This staff member is already assigned to this shift.")
        new_schedule = Scheduling(staff_id, shift_id)
        db.session.add(new_schedule)
        db.session.commit()

    def view_shift_reports(self, staff_id):
        schedules = Scheduling.query.filter_by(staff_id=staff_id).all()
        return schedules
    
    def view_combined_roster(self):
        rosters = Scheduling.query.all()
        return rosters