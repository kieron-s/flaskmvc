from App.database import db
from .user import User
from .shift import Shift

class Scheduling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)

    staff = db.relationship('User', backref=db.backref('schedules', lazy=True))  
    shift = db.relationship('Shift', backref=db.backref('schedules', lazy=True))

    def __init__(self, staff_id, shift_id):
        self.staff_id = staff_id
        self.shift_id = shift_id

    @staticmethod
    def schedule_staff_to_shift(admin_user_id, user_id, shift_id):
        admin_user = db.session.get(User, admin_user_id)
        if not admin_user or admin_user.role != 'admin':
            return "Permission denied: Only admins can schedule shifts."
        user = db.session.get(User, user_id)
        shift = db.session.get(Shift, shift_id)
        if user and shift and user.role == 'staff':
            if not hasattr(user, 'shifts'):
                user.shifts = []
            user.shifts.append(shift)
            message = f"Scheduled Shift ID {shift_id} ({shift.day} {shift.start_time}) to User ID {user_id} ({user.username})"
            db.session.commit()
            return message
        else:
            return "Invalid user or shift, or user is not staff."

    @staticmethod
    def view_shift_report():
        from App.models.user import User
        staff_users = db.session.scalars(db.select(User).filter_by(role='staff')).all()
        report = []
        for user in staff_users:
            user_report = {"username": user.username, "shifts": []}
            if hasattr(user, 'shifts') and user.shifts:
                for shift in user.shifts:
                    user_report["shifts"].append({
                        "day": shift.day,
                        "start_time": shift.start_time,
                        "end_time": shift.end_time
                    })
            report.append(user_report)
        return report
    
    @staticmethod
    def get_combined_schedule():
        from App.models.user import User
        staff_users = db.session.scalars(db.select(User).filter_by(role='staff')).all()
        combined_schedule = {}
        for user in staff_users:
            if hasattr(user, 'shifts'):
                for shift in user.shifts:
                    if shift.day not in combined_schedule:
                        combined_schedule[shift.day] = []
                    combined_schedule[shift.day].append((user.username, shift.start_time, shift.end_time))
        return combined_schedule