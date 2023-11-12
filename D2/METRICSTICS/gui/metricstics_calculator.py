import tkinter
import tkinter as tk
import tkinter.simpledialog
from tkinter import ttk, filedialog, messagebox

from D2.METRICSTICS.data_computation.data_processor import DataProcessor
from D2.METRICSTICS.data_computation.data_statistics import DataStatistics
from D2.METRICSTICS.user_management.user_manager import UserManagement


class MetricsticsCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("METRICSTICS Calculator - (Team O)")

        # Username label at the top
        self.username_label = ttk.Label(self.root, text="Logged in as: Guest", font=('Helvetica', 12))
        self.username_label.grid(row=0, column=4, columnspan=4, padx=10, pady=10)

        # Entry for data input
        self.data_entry = ttk.Entry(self.root, width=40)
        self.data_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Buttons for numeric digits (0-9)
        self.create_digit_buttons()

        # Buttons for operations
        ttk.Button(self.root, text=".", command=lambda: self.add_digit(".")).grid(row=5, column=0)
        ttk.Button(self.root, text="-", command=lambda: self.add_minus()).grid(row=5, column=2)
        ttk.Button(self.root, text="Clear", command=self.clear_entry).grid(row=2, column=4)
        ttk.Button(self.root, text="Append", command=self.add_value).grid(row=3, column=4)

        # Buttons for statistics calculations
        ttk.Button(self.root, text="Mean", command=self.calculate_mean).grid(row=6, column=0)
        ttk.Button(self.root, text="Median", command=self.calculate_median).grid(row=6, column=1)
        ttk.Button(self.root, text="Mode", command=self.calculate_mode).grid(row=6, column=2)
        ttk.Button(self.root, text="Minimum", command=self.calculate_minimum).grid(row=7, column=0)
        ttk.Button(self.root, text="Maximum", command=self.calculate_maximum).grid(row=7, column=1)
        ttk.Button(self.root, text="MAD", command=self.calculate_mad).grid(row=7, column=2)
        ttk.Button(self.root, text="Std Dev", command=self.calculate_std_dev).grid(row=8, column=1)

        # "Upload CSV" button
        ttk.Button(self.root, text="Upload CSV", command=self.upload_csv).grid(row=4, column=4)

        # "Save Dataset" button
        ttk.Button(self.root, text="Save Dataset", command=self.save_dataset).grid(row=5, column=4)

        # "Show History" button
        ttk.Button(self.root, text="Show History", command=self.show_history).grid(row=6, column=4)

        # "Login" button
        ttk.Button(self.root, text="Login", command=self.show_login_window).grid(row=8, column=4)

        # logout button
        ttk.Button(self.root, text="Logout", command=self.logout).grid(row=9, column=4)

        # Label for displaying the result
        self.result_label = ttk.Label(self.root, text="", font=('Helvetica', 16))
        self.result_label.grid(row=9, column=0, columnspan=4, padx=10, pady=10)

        # List to store values
        self.values = []
        # Variable to store the logged-in username
        self.logged_in_username = None
        # Variable to store the logged-in userid
        self.logged_in_userid = None
        # Variable to store the login window
        self.login_window = None

    def create_digit_buttons(self):
        button_labels = ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0"]
        row = 2
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

        if len(mode_values) <= 10:
            mode_str = ', '.join(map(str, mode_values))
        else:
            mode_str = f"{len(mode_values)} mode values found."

        self.result_label.config(text=f"Mode: {mode_str}")

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
            data_processor = DataProcessor()
            data_from_csv = data_processor.load_data_from_csv(file_path)

            # Clear the existing values and update the data_entry with the data from CSV
            self.values = data_from_csv
            self.data_entry.delete(0, tk.END)
            self.result_label.config(text="Data successfully loaded from csv")

    def show_login_window(self):
        # Create a new window for login
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")

        # Entry for username
        ttk.Label(self.login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ttk.Entry(self.login_window, width=20)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Entry for password
        ttk.Label(self.login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = ttk.Entry(self.login_window, show="*", width=20)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Login button in the login window
        ttk.Button(self.login_window, text="Login", command=lambda: self.login(self.login_window)).grid(row=2, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=10)

    def login(self, login_window):
        # Get entered username and password
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        # Validate credentials using UserManager
        user_manager = UserManagement()
        user = user_manager.authenticate_user(entered_username, entered_password)
        if user:
            # Successful login
            self.logged_in_username = entered_username
            self.logged_in_userid = user[0]
            self.username_label.config(text=f"Logged in as: {self.logged_in_username}")
            messagebox.showinfo("Login Successful", "Welcome, " + entered_username + "!")

            # Close the login window
            login_window.destroy()
        else:
            # Failed login
            messagebox.showerror("Login Failed", "Invalid username or password")

    def save_dataset(self):
        # Check if a user is logged in
        if self.logged_in_username:
            # Check if there is data to save
            if self.values:
                # Prompt user for dataset name
                dataset_name = tkinter.simpledialog.askstring("Input", "Enter the name of the dataset:")

                # Check if the user provided a name
                if dataset_name:
                    # Save the dataset using the DataSaver
                    user_manager = UserManagement()
                    user_manager.save_dataset(self.logged_in_userid, dataset_name, self.values)
                    self.result_label.config(text="Dataset successfully saved.")
                else:
                    self.result_label.config(text="Dataset name cannot be empty.")
            else:
                self.result_label.config(text="No data to save.")
        else:
            self.result_label.config(text="Please login before saving the dataset.")

    def show_history(self):
        if self.logged_in_username:
            # Create a new window for showing history
            history_window = tk.Toplevel(self.root)
            history_window.title("Data History")

            # Get historical data from the backend using UserManagement
            user_manager = UserManagement()
            historical_data = user_manager.get_user_history(self.logged_in_userid)

            # Create a Treeview widget for displaying the table
            tree = ttk.Treeview(history_window)
            tree["columns"] = ("Dataset Name", "Actual Data")
            tree.column("#0", width=0, stretch=tk.NO)  # Hide the first column

            # Define column headings
            tree.heading("#0", text="", anchor=tk.W)
            tree.heading("Dataset Name", text="Dataset Name", anchor=tk.W)
            tree.heading("Actual Data", text="Actual Data", anchor=tk.W)

            # Insert data into the treeview
            for idx, (dataset_name, data) in enumerate(historical_data, start=1):
                tree.insert("", idx, values=(dataset_name, data))

            # Display the treeview
            tree.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

            # Add scrollbar to the treeview
            scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=tree.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")
            tree.configure(yscrollcommand=scrollbar.set)

            # Adjust column widths
            for col in ("Dataset Name", "Actual Data"):
                tree.column(col, width=150, anchor=tk.W)

            # Make the window resizable
            history_window.resizable(True, True)
        else:
            self.result_label.config(text="Please login before watching the history.")

    def logout(self):
        # Reset logged-in variables
        self.logged_in_username = None
        self.logged_in_userid = None

        # Update username label
        self.username_label.config(text="Logged in as: Guest")

        # Clear values and result label
        self.values = []
        self.data_entry.delete(0, tk.END)
        self.result_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = MetricsticsCalculator(root)
    root.mainloop()
