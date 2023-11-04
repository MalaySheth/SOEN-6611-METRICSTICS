class CustomMathUtils:
    @staticmethod
    def custom_max(data):
        if not data:
            return None
        max_value = data[0]
        for value in data:
            if value > max_value:
                max_value = value
        return max_value

    @staticmethod
    def custom_min(data):
        if not data:
            return None
        min_value = data[0]
        for value in data:
            if value < min_value:
                min_value = value
        return min_value

    @staticmethod
    def custom_sum(data):
        total = 0
        for value in data:
            total += value
        return total

    @staticmethod
    def custom_abs(value):
        if value < 0:
            return -value
        return value
