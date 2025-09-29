from App.database import db
from datetime import datetime


class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __init__(self, day, start_time, end_time):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

    @staticmethod
    def create_shift(day, start_time_str, end_time_str):
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()
        shift = Shift(day=day, start_time=start_time, end_time=end_time)
        db.session.add(shift)
        db.session.commit()
        return shift
    
    @staticmethod
    def print_all_shifts():
        shifts = db.session.scalars(db.select(Shift)).all()
        for shift in shifts:
            print(f"ID: {shift.id}, Day: {shift.day}, Start: {shift.start_time}, End: {shift.end_time}")