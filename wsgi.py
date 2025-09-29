import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from datetime import datetime
from App.controllers import create_shift
# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("role", default="staff")
def create_user_command(username, password, role):
    create_user(username, password, role)
    print(f'{username} created!')

@user_cli.command("create-shift", help="Creates a shift")
@click.argument("day", default="Monday")
@click.argument("start_time", default="09:00")
@click.argument("end_time", default="17:00")
def create_shift_command(day, start_time, end_time):
    from App.models.shift import Shift
    shift = Shift.create_shift(day, start_time, end_time)
    print(f'Shift on {shift.day} from {shift.start_time} to {shift.end_time} created!')

@user_cli.command("print-shifts", help="Prints all shifts")
def print_shifts_command():
    from App.models import Shift
    Shift.print_all_shifts()

@user_cli.command("print-staff", help="Prints all staff users")
def print_staff_command():
    staff = db.session.scalars(db.select(User).where(User.role == 'staff')).all()
    for user in staff:
        print(f"ID: {user.id}, Username: {user.username}, Role: {user.role}")

@user_cli.command("clear-roster", help="Clears all scheduled shifts for all staff members")
def clear_schedule_command():
    db.session.execute(db.table('user_shift').delete())
    db.session.commit()
    print("Cleared all scheduled shifts for all staff members.")

@user_cli.command("schedule-staff", help="Schedules a shift to a staff member (admin only)")
@click.argument("admin_user_id", type=int)
@click.argument("user_id", type=int)
@click.argument("shift_id", type=int)
def schedule_shift_to_staff_command(admin_user_id, user_id, shift_id):
    from App.models.scheduling import Scheduling
    result = Scheduling.schedule_staff_to_shift(admin_user_id, user_id, shift_id)
    print(result)

@user_cli.command("view-combined-schedule", help="View combined schedule of all staff members")
def view_combined_schedule_command():
    from App.models.scheduling import Scheduling
    combined_schedule = Scheduling.get_combined_schedule()
    for day, shifts in combined_schedule.items():
        print(f"{day}:")
        for username, start_time, end_time in shifts:
            print(f"  {username}: {start_time} - {end_time}")
    if not combined_schedule:
        print("No shifts scheduled.")

@user_cli.command("view-shift-report", help="View shift report for all staff members (admin only)")
@click.argument("admin_user_id", type=int)
def view_shift_report_command(admin_user_id):
    admin_user = db.session.get(User, admin_user_id)
    if not admin_user or admin_user.role != 'admin':
        print("Permission denied: Only admins can view shift reports.")
        return
    from App.models.scheduling import Scheduling
    report = Scheduling.view_shift_report()
    for user_report in report:
        print(f"Shift report for {user_report['username']}:")
        if user_report["shifts"]:
            for shift in user_report["shifts"]:
                print(f"  {shift['day']}: {shift['start_time']} - {shift['end_time']}")
        else:
            print("No shifts scheduled.")

@user_cli.command("staff-checkin", help="Staff member checks in to a specific shift")
@click.argument("user_id", type=int)
@click.argument("shift_id", type=int)
def staff_checkin_command(user_id, shift_id):
    from App.models.attendance import Attendance
    result = Attendance.staff_checkin(user_id, shift_id)
    print(result)

@user_cli.command("staff-checkout", help="Staff member checks out of a specific shift")
@click.argument("user_id", type=int)
@click.argument("shift_id", type=int)
def staff_checkout_command(user_id, shift_id):
    from App.models.attendance import Attendance
    result = Attendance.staff_checkout(user_id, shift_id)
    print(result)


# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)