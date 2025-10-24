import datetime
class ConflictChecker:
    @staticmethod
    def is_conflicted(entries, location, date_time, duration):
        new_end = date_time + datetime.timedelta(minutes=duration)
        for entry in entries:
            if entry["location"] == location:
                existing_end = entry["date_time"] + datetime.timedelta(minutes=entry["duration"])
                if (date_time < existing_end) and (new_end > entry["date_time"]):
                    return True
        return False