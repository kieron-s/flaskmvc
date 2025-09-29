from .user import create_user
from .user import create_shift
from App.database import db
from App.models.scheduling import Scheduling


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', 'admin')
    create_user('alice', 'alicepass', 'staff')
    create_user('eve', 'evepass', 'staff')
    create_user('john', 'johnpass', 'staff')
    create_user('mary', 'marypass', 'staff')
    create_shift('Monday', '09:00', '17:00')
    create_shift('Tuesday', '10:00', '18:00')
    create_shift('Wednesday', '08:00', '16:00')
    create_shift('Thursday', '11:00', '19:00')
    Scheduling.schedule_staff_to_shift(1, 2, 1)
    Scheduling.schedule_staff_to_shift(1, 3, 2)