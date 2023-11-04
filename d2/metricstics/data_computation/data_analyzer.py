class DataAnalyzer:
    def __init__(self, data):
        self.data = data

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
