

class CalorieTracker:
    def __init__(self, daily_goal):
        self.daily_goal = daily_goal
        self.calories_consumed = 0

    def add_calories(self, calories):
        """
        Add consumed calories to the tracker.
        """
        self.calories_consumed += calories

    def get_calories_consumed(self):
        """
        Get the total calories consumed.
        """
        return self.calories_consumed

    def compare_to_goal(self):
        """
        Compare total calories consumed to the daily goal.
        Returns:
            -1 if below the goal
            0 if equal to the goal
            1 if above the goal
        """
        if self.calories_consumed < self.daily_goal:
            return -1
        elif self.calories_consumed == self.daily_goal:
            return 0
        else:
            return 1
