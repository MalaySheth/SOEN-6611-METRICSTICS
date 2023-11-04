import tkinter as tk
from tkinter import ttk, filedialog

from d2.metricstics.data_computation.data_processor import DataProcessor
from d2.metricstics.data_computation.data_statistics import DataStatistics


class MetricsticsCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("METRICSTICS Calculator - (Team O)")

        # Entry for data input
        self.data_entry = ttk.Entry(self.root, width=40)
        self.data_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Buttons for numeric digits (0-9)
        self.create_digit_buttons()

        # Buttons for operations
        ttk.Button(self.root, text=".", command=lambda: self.add_digit(".")).grid(row=4, column=0)
        ttk.Button(self.root, text="-", command=lambda: self.add_minus()).grid(row=4, column=2)
        ttk.Button(self.root, text="Clear", command=self.clear_entry).grid(row=1, column=4)
        ttk.Button(self.root, text="Append", command=self.add_value).grid(row=2, column=4)

        # Buttons for statistics calculations
        ttk.Button(self.root, text="Mean", command=self.calculate_mean).grid(row=5, column=0)
        ttk.Button(self.root, text="Median", command=self.calculate_median).grid(row=5, column=1)
        ttk.Button(self.root, text="Mode", command=self.calculate_mode).grid(row=5, column=2)
        ttk.Button(self.root, text="Minimum", command=self.calculate_minimum).grid(row=6, column=0)
        ttk.Button(self.root, text="Maximum", command=self.calculate_maximum).grid(row=6, column=1)
        ttk.Button(self.root, text="MAD", command=self.calculate_mad).grid(row=6, column=2)
        ttk.Button(self.root, text="Std Dev", command=self.calculate_std_dev).grid(row=7, column=1)

        # "Upload CSV" button
        ttk.Button(self.root, text="Upload CSV", command=self.upload_csv).grid(row=3, column=4)

        # Label for displaying the result
        self.result_label = ttk.Label(self.root, text="", font=('Helvetica', 16))
        self.result_label.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

        # List to store values
        self.values = []

    def create_digit_buttons(self):
        button_labels = ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0"]
        row = 1
        col = 0
        for label in button_labels:
            if label == "0":
                ttk.Button(self.root, text=label, command=lambda l=label: self.add_digit(l)).grid(row=row,
                                                                                                  column=col + 1)
            else:
                ttk.Button(self.root, text=label, command=lambda l=label: self.add_digit(l)).grid(row=row, column=col)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def add_digit(self, digit):
        current_data = self.data_entry.get()
        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(0, current_data + digit)

    def add_value(self):
        value = self.data_entry.get()
        if value:
            try:
                num = float(value)
                self.values.append(num)
                self.data_entry.delete(0, tk.END)
                self.result_label.config(text="Last data appended: " + str(num))
            except ValueError:
                self.result_label.config(text="Invalid input. Please enter a valid number.")
                self.data_entry.delete(0, tk.END)

    def add_minus(self):
        current_data = self.data_entry.get()
        if not current_data or current_data == "-":
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, "-")
        elif current_data == "-":
            self.data_entry.delete(0, tk.END)
        else:
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, "-" + current_data)

    def clear_entry(self):
        self.data_entry.delete(0, tk.END)

    def calculate_mean(self):
        statistics = DataStatistics(self.values)
        mean_value = statistics.mean()
        self.result_label.config(text=f"Mean (μ): {mean_value:.2f}")

    def calculate_median(self):
        statistics = DataStatistics(self.values)
        median_value = statistics.calculate_median()
        self.result_label.config(text=f"Median: {median_value:.2f}")

    def calculate_mode(self):
        statistics = DataStatistics(self.values)
        mode_values = statistics.mode()
        self.result_label.config(text=f"Mode: {', '.join(map(str, mode_values))}")

    def calculate_minimum(self):
        statistics = DataStatistics(self.values)
        minimum_value = statistics.minimum()
        self.result_label.config(text=f"Minimum: {minimum_value:.2f}")

    def calculate_maximum(self):
        statistics = DataStatistics(self.values)
        maximum_value = statistics.maximum()
        self.result_label.config(text=f"Maximum: {maximum_value:.2f}")

    def calculate_mad(self):
        statistics = DataStatistics(self.values)
        mad_value = statistics.mean_absolute_deviation()
        self.result_label.config(text=f"MAD: {mad_value:.2f}")

    def calculate_std_dev(self):
        statistics = DataStatistics(self.values)
        std_dev = statistics.standard_deviation()
        self.result_label.config(text=f"Std Dev: {std_dev:.2f}")

    def upload_csv(self):
        # Open a file dialog to select a CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            # Read data from the selected CSV file using DataProcessor
            data_processor = DataProcessor()
            data_from_csv = data_processor.load_data_from_csv(file_path)

            # Clear the existing values and update the data_entry with the data from CSV
            self.values = data_from_csv
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, ", ".join(map(str, data_from_csv)))


if __name__ == "__main__":
    root = tk.Tk()
    app = MetricsticsCalculator(root)
    root.mainloop()
