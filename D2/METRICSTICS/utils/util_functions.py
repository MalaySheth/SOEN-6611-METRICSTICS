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

    @staticmethod
    def custom_sort(data):
        if not data:
            return None
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data

    @staticmethod
    def custom_count(data):
        if not data:
            return None
        count = 0
        for _ in data:
            count += 1
        return count

    @staticmethod
    def custom_copy(data):
        """
        Create a copy of the original data to avoid altering it.

        Parameters:
        - data: The original data to be copied.

        Returns:
        - A copy of the original data.
        """
        if data is None:
            return None

        # Custom implementation of copying the data
        return data[:]
