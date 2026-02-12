from infrastructure.activity_type import ActivityType
class CapacityCalculator:
    @staticmethod
    def calculate(activity_type, groups=None, subgroup=None):
        if activity_type == ActivityType.LECTURE:
            return sum(len(group.students) for group in groups)
        elif activity_type == ActivityType.PRACTICAL:
            return len(groups[0].students) if groups else 0
        elif activity_type == ActivityType.LAB:
            return len(subgroup.students) if subgroup else 0
        return 0