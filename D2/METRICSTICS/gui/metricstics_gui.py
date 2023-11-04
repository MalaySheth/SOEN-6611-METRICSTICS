import tkinter as tk
from statistics import mean, median, mode
from tkinter import ttk

from data_computation.data_analyzer import DataAnalyzer
from data_computation.data_statistics import DataStatistics


class MetricsticsCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("METRICSTICS Calculator")

        # Entry for data input
        self.data_entry = ttk.Entry(self.root, width=40)
        self.data_entry.grid(row=0, column=0, columnspan=3)

        # Plus button for adding values
        self.plus_button = ttk.Button(self.root, text="Plus", command=self.add_value)
        self.plus_button.grid(row=0, column=3)

        # Buttons for different calculations
        self.mean_button = ttk.Button(self.root, text="Mean", command=self.calculate_mean)
        self.mean_button.grid(row=1, column=0)
        self.median_button = ttk.Button(self.root, text="Median", command=self.calculate_median)
        self.median_button.grid(row=1, column=1)
        self.mode_button = ttk.Button(self.root, text="Mode", command=self.calculate_mode)
        self.mode_button.grid(row=1, column=2)
        self.min_button = ttk.Button(self.root, text="Minimum", command=self.calculate_minimum)
        self.min_button.grid(row=1, column=3)
        self.max_button = ttk.Button(self.root, text="Maximum", command=self.calculate_maximum)
        self.max_button.grid(row=2, column=0)
        self.mad_button = ttk.Button(self.root, text="MAD", command=self.calculate_mad)
        self.mad_button.grid(row=2, column=1)
        self.std_dev_button = ttk.Button(self.root, text="Std Dev", command=self.calculate_std_dev)
        self.std_dev_button.grid(row=2, column=2)

        # Label for displaying the result
        self.result_label = ttk.Label(self.root, text="")
        self.result_label.grid(row=3, column=0, columnspan=4)

        # List to store values
        self.values = []

        # Button to calculate and display all metrics
        self.calculate_all_button = ttk.Button(self.root, text="Calculate All Metrics",
                                               command=self.calculate_all_metrics)
        self.calculate_all_button.grid(row=3, column=3)

    def add_value(self):
        value = self.data_entry.get()
        if value:
            self.values.append(float(value))
            self.data_entry.delete(0, tk.END)

    def calculate_mean(self):
        mean_value = mean(self.values)
        self.result_label.config(text=f"Mean (μ): {mean_value:.2f}")

    def calculate_median(self):
        median_value = median(self.values)
        self.result_label.config(text=f"Median: {median_value:.2f}")

    def calculate_mode(self):
        mode_values = mode(self.values)
        self.result_label.config(text=f"Mode: {', '.join(map(str, mode_values))}")

    def calculate_minimum(self):
        minimum_value = min(self.values)
        self.result_label.config(text=f"Minimum: {minimum_value:.2f}")

    def calculate_maximum(self):
        maximum_value = max(self.values)
        self.result_label.config(text=f"Maximum: {maximum_value:.2f}")

    def calculate_mad(self):
        statistics = DataStatistics(self.values)
        mad_value = statistics.mean_absolute_deviation()
        self.result_label.config(text=f"MAD: {mad_value:.2f}")

    def calculate_std_dev(self):
        analyzer = DataAnalyzer(self.values)
        std_dev = analyzer.standard_deviation()
        self.result_label.config(text=f"Std Dev: {std_dev:.2f}")

    def calculate_all_metrics(self):
        mean_value = mean(self.values)
        median_value = median(self.values)
        mode_values = mode(self.values)

        # Check if mode_values is a float (single mode)
        if isinstance(mode_values, float):
            mode_text = f"Mode: {mode_values:.2f}"
        else:
            # If there are multiple modes, join them
            mode_text = f"Mode: {', '.join(map(lambda x: f'{x:.2f}', mode_values))}"

        minimum_value = min(self.values)
        maximum_value = max(self.values)
        statistics = DataStatistics(self.values)
        mad_value = statistics.mean_absolute_deviation()
        analyzer = DataAnalyzer(self.values)
        std_dev = analyzer.standard_deviation()

        result_text = (
            f"Mean (μ): {mean_value:.2f}\n"
            f"Median: {median_value:.2f}\n"
            f"{mode_text}\n"
            f"Minimum: {minimum_value:.2f}\n"
            f"Maximum: {maximum_value:.2f}\n"
            f"MAD: {mad_value:.2f}\n"
            f"Std Dev: {std_dev:.2f}"
        )

        self.result_label.config(text=result_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = MetricsticsCalculator(root)
    root.mainloop()
