import datetime
from exceptions.errors import *
class Event:
    def __init__(self, title, date_time, location, organiser, groups):
        self.title = title
        self.location = location
        self.organiser = organiser
        self.groups = groups
        self.date_time = date_time
        self.attendees = []
        self.is_cancelled = False

    def add_attendee(self, student):
        if student.group not in self.groups:
            raise GroupNotInvitedError(
                f"Группа {student.group.name} не приглашена"
            )
        if student not in self.attendees:
            self.attendees.append(student)
    def cancel(self):
        self.is_cancelled = True

    def remove_student(self, student):
        if student in self.attendees:
            self.attendees.remove(student)

    def reschedule(self, new_date_time):
        self.date_time = new_date_time