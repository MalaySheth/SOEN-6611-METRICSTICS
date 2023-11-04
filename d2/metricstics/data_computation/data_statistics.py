from d2.metricstics.utils.utility_functions import CustomMathUtils


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
        mean_value = self.mean()
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

    def mean(self):
        if not self.data:
            return None
        total = 0
        count = 0
        for value in self.data:
            total += value
            count += 1
        return total / count

    def standard_deviation(self):
        if not self.data:
            return None
        mean_value = self.mean()
        squared_diff = 0
        count = 0
        for value in self.data:
            squared_diff += (value - mean_value) ** 2
            count += 1
        return (squared_diff / count) ** 0.5

    def calculate_median(self):
        if not self.data:
            return None
        n = len(self.data)
        data_copy = self.data.copy()  # Create a copy of the original data to avoid altering it

        data_copy.sort()  # Sort the copied data in ascending order

        if n % 2 == 1:
            # If the number of data points is odd, return the middle value
            return data_copy[n // 2]
        else:
            # If the number of data points is even, return the average of the two middle values
            middle1 = data_copy[(n - 1) // 2]
            middle2 = data_copy[n // 2]
            return (middle1 + middle2) / 2


