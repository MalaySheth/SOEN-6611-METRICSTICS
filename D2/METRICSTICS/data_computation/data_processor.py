import csv


class DataProcessor:
    def __init__(self, data=None):
        self.data = data if data is not None else []

    def load_data_from_csv(self, file_path):
        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                data_from_csv = [float(row[0]) for row in csv_reader if row]

                # Update the internal data with the loaded data
                self.data = data_from_csv

                return data_from_csv
        except (FileNotFoundError, ValueError, IndexError, Exception):
            return None
