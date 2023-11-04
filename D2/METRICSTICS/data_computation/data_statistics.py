from data_analyzer import DataAnalyzer
from utils.utility_functions import CustomMathUtils


class DataStatistics:
    def __init__(self, data):
        self.data = data

    def maximum(self):
        if not self.data:
            return None
        # Use the custom utility function for maximum
        return CustomMathUtils.custom_max(self.data)

    def minimum(self):
        if not self.data:
            return None
        # Use the custom utility function for minimum
        return CustomMathUtils.custom_min(self.data)

    def count(self):
        if not self.data:
            return None
        # Use the custom utility function for counting
        return len(self.data)

    def total(self):
        if not self.data:
            return None
        # Use the custom utility function for sum
        return CustomMathUtils.custom_sum(self.data)

    def mean_absolute_deviation(self):
        if not self.data:
            return None
        analyzer = DataAnalyzer(self.data)
        mean_value = analyzer.mean()
        absolute_deviations = [CustomMathUtils.custom_abs(value - mean_value) for value in self.data]
        return sum(absolute_deviations) / len(self.data)

    def mode(self):
        if not self.data:
            return None

        # Count the occurrences of each value using a dictionary
        value_counts = {}
        for value in self.data:
            if value in value_counts:
                value_counts[value] += 1
            else:
                value_counts[value] = 1

        # Find the mode(s) with the highest count
        max_count = max(value_counts.values())
        mode_values = [value for value, count in value_counts.items() if count == max_count]

        return mode_values
