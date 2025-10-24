from infrastructure.schedule import Schedule
import datetime 
from exceptions.errors import *
class Semester:
    def __init__(self,name,start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.schedule = Schedule()
    def is_active(self, date_time):
        if isinstance(date_time, datetime.datetime):
            d = date_time.date()
        else:
            d = date_time
        return self.start_date <= d <= self.end_date
    def add_schedule_entry(self, name, activity_type, date_time, duration, location, teacher, course, groups=None, subgroup=None):
        if not self.is_active(date_time.date()):
            raise DateOutOfSemesterError(
                f"Дата {date_time.date()} вне периода семестра {self.name}"
            )
        self.schedule.add_entry(name, activity_type, date_time, duration, location, teacher, course, groups, subgroup)