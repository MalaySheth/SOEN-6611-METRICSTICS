import json
import tkinter
import tkinter as tk
import tkinter.simpledialog
from tkinter import ttk, filedialog, messagebox

from PIL import Image, ImageTk

from D2.METRICSTICS.data_computation.data_processor import DataProcessor
from D2.METRICSTICS.data_computation.data_statistics import DataStatistics
from D2.METRICSTICS.user_management.user_manager import UserManager
from D2.METRICSTICS.utils.util_functions import CustomMathUtils


class MetricsticsCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("METRICSTICS Calculator - (Team O)")
        self.root.geometry('800x600')  # Set initial size of the window

        # Load the background image with PIL
        self.original_image = Image.open("TLMS_20220906_1200x628.png")
        self.background_image = ImageTk.PhotoImage(self.original_image)

        # Create a label with the image
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind the resize event to an event handler
        self.root.bind('<Configure>', self.resize_background)

        # Create a main frame that will contain everything except the background
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Username label at the top
        self.username_label = ttk.Label(self.main_frame, text="Logged in as: Guest", font=('Helvetica', 13))
        self.username_label.grid(row=0, column=4, columnspan=4, padx=10, pady=10)

        # Entry for data input
        self.data_entry = ttk.Entry(self.main_frame, width=40)
        self.data_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Buttons for numeric digits (0-9)
        self.create_digit_buttons()

        # Buttons for operations
        ttk.Button(self.main_frame, text=".", command=lambda: self.add_digit(".")).grid(row=5, column=0)
        ttk.Button(self.main_frame, text="-", command=lambda: self.add_minus()).grid(row=5, column=2)
        ttk.Button(self.main_frame, text="Clear", command=self.clear_entry).grid(row=2, column=4)
        ttk.Button(self.main_frame, text="Append", command=self.add_value).grid(row=3, column=4)

        # Buttons for statistics calculations
        ttk.Button(self.main_frame, text="Mean", command=self.calculate_mean).grid(row=6, column=0)
        ttk.Button(self.main_frame, text="Median", command=self.calculate_median).grid(row=6, column=1)
        ttk.Button(self.main_frame, text="Mode", command=self.calculate_mode).grid(row=6, column=2)
        ttk.Button(self.main_frame, text="Minimum", command=self.calculate_minimum).grid(row=7, column=0)
        ttk.Button(self.main_frame, text="Maximum", command=self.calculate_maximum).grid(row=7, column=1)
        ttk.Button(self.main_frame, text="MAD", command=self.calculate_mad).grid(row=7, column=2)
        ttk.Button(self.main_frame, text="Std Dev", command=self.calculate_std_dev).grid(row=8, column=1)

        # "Upload CSV" button
        ttk.Button(self.main_frame, text="Upload CSV", command=self.upload_csv).grid(row=4, column=4)

        # "Save Dataset" button
        ttk.Button(self.main_frame, text="Save Dataset", command=self.save_dataset).grid(row=5, column=4)

        # "Reset Dataset" button
        ttk.Button(self.main_frame, text="Reset Dataset", command=self.reset_dataset).grid(row=6, column=4)

        # "Show History" button
        ttk.Button(self.main_frame, text="Show History", command=self.show_history).grid(row=7, column=4)

        ttk.Button(self.main_frame, text="Signup", command=self.show_signup_window).grid(row=9, column=4)

        # "Login" button
        ttk.Button(self.main_frame, text="Login", command=self.show_login_window).grid(row=10, column=4)

        # logout button
        ttk.Button(self.main_frame, text="Logout", command=self.logout).grid(row=11, column=4)

        # Label for displaying the result
        self.result_label = ttk.Label(self.main_frame, text="", font=('Helvetica', 16))
        self.result_label.grid(row=12, column=0, columnspan=4, padx=10, pady=10)

        # List to store values
        self.values = []
        # Variable to store the logged-in username
        self.logged_in_username = None
        # Variable to store the logged-in userid
        self.logged_in_userid = None
        # Variable to store the login window
        self.login_window = None

    def resize_background(self, event):
        # Resize the background image to the size of the window
        new_size = (event.width, event.height)
        resized_image = self.original_image.resize(new_size, Image.Resampling.LANCZOS)
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.background_label.config(image=self.background_image)
        self.background_label.image = self.background_image  # Keep a reference

    def create_digit_buttons(self):
        button_labels = ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0"]
        row = 2
        col = 0
        for label in button_labels:
            button = ttk.Button(self.main_frame, text=label, command=lambda l=label: self.add_digit(l))
            if label == "0":
                # Place the "0" button in the center of the 4th row
                button.grid(row=row + 2, column=1, pady=5, padx=5)
            else:
                button.grid(row=row, column=col, pady=5, padx=5)
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
        if not self.values:
            self.result_label.config(text="Dataset is empty. Please add values before calculating the mean.")
            return
        statistics = DataStatistics(self.values)
        mean_value = statistics.mean()
        self.result_label.config(text=f"Mean (μ): {mean_value:.2f}")

    def calculate_median(self):
        if not self.values:
            self.result_label.config(text="Dataset is empty. Please add values before calculating the median.")
            return
        statistics = DataStatistics(self.values)
        median_value = statistics.calculate_median()
        self.result_label.config(text=f"Median: {median_value:.2f}")

    def calculate_mode(self):
        if not self.values:
            self.result_label.config(text="Dataset is empty. Please add values before calculating the mode.")
            return
        statistics = DataStatistics(self.values)
        mode_values = statistics.mode()

        if CustomMathUtils.custom_count(mode_values) <= 10:
            mode_str = ', '.join(map(str, mode_values))
        else:
            mode_str = f"{len(mode_values)} mode values found."

        self.result_label.config(text=f"Mode: {mode_str}")

    def calculate_minimum(self):
        if not self.values:
            self.result_label.config(text="Dataset is empty. Please add values before calculating the minimum.")
            return
        statistics = DataStatistics(self.values)
        minimum_value = statistics.minimum()
        self.result_label.config(text=f"Minimum: {minimum_value:.2f}")

    def calculate_maximum(self):
        if not self.values:
            self.result_label.config(text="Dataset is empty. Please add values before calculating the maximum.")
            return
        statistics = DataStatistics(self.values)
        maximum_value = statistics.maximum()
        self.result_label.config(text=f"Maximum: {maximum_value:.2f}")

    def calculate_mad(self):
        if not self.values:
            self.result_label.config(text="Dataset is empty. Please add values before calculating the MAD.")
            return
        statistics = DataStatistics(self.values)
        mad_value = statistics.mean_absolute_deviation()
        self.result_label.config(text=f"MAD: {mad_value:.2f}")

    def calculate_std_dev(self):
        if not self.values:
            self.result_label.config(text="Dataset is empty. Please add values before calculating the std dev.")
            return
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
        if self.logged_in_username:
            messagebox.showinfo("Already Logged In", "Please logout before logging in with another account.")
            return

        # Create a new window for login
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")
        self.login_window.geometry('500x300')  # Set initial size of the window

        # Create a main frame that will contain everything except the background
        self.login_frame = ttk.Frame(self.login_window)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Load the login image
        self.login_original_image = Image.open("login.jpg")  # Replace with your image path
        self.login_background_image = ImageTk.PhotoImage(self.login_original_image)

        # Create a label with the image
        self.login_image_label = tk.Label(self.login_window, image=self.login_background_image)
        self.login_image_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind the resize event to an event handler specifically for the signup window
        self.login_window.bind('<Configure>', self.resize_login_background)

        # Ensure the image label is at the back
        self.login_image_label.lower()

        # Entry for username
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ttk.Entry(self.login_frame, width=20)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Entry for password
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = ttk.Entry(self.login_frame, show="*", width=20)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Login button in the login window
        ttk.Button(self.login_frame, text="Login", command=lambda: self.login(self.login_frame)).grid(row=2, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=10)

    def login(self, login_window):
        # Get entered username and password
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        # Validate credentials using UserManager
        user_manager = UserManager()
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

    def resize_login_background(self, event):
        # Check if the original image has been loaded
        if hasattr(self, 'login_original_image'):
            # Resize the background image to the size of the window
            new_width, new_height = event.width, event.height
            image = self.login_original_image.resize((new_width, new_height), Image.LANCZOS)

            # Update the image of the background label
            self.login_background_image = ImageTk.PhotoImage(image)
            self.login_image_label.config(image=self.login_background_image)
            self.login_image_label.image = self.login_background_image  # Keep a reference!

    def show_signup_window(self):
        # Create a new window for signup
        self.signup_window = tk.Toplevel(self.root)
        self.signup_window.title("Signup")
        self.signup_window.geometry('500x300')  # Set initial size of the window


        # Create a main frame that will contain everything except the background
        self.signup_frame = ttk.Frame(self.signup_window)
        self.signup_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Load the signup image
        self.signup_original_image = Image.open("signup.jpg")  # Replace with your image path
        self.signup_background_image = ImageTk.PhotoImage(self.signup_original_image)

        # Create a label with the image
        self.signup_image_label = tk.Label(self.signup_window, image=self.signup_background_image)
        self.signup_image_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind the resize event to an event handler specifically for the signup window
        self.signup_window.bind('<Configure>', self.resize_signup_background)

        # Ensure the image label is at the back
        self.signup_image_label.lower()



        # Entry for new username
        ttk.Label(self.signup_frame, text="New Username:").grid(row=0, column=0, padx=10, pady=10)
        self.new_username_entry = ttk.Entry(self.signup_frame, width=20)
        self.new_username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Entry for new password
        ttk.Label(self.signup_frame, text="New Password:").grid(row=1, column=0, padx=10, pady=10)
        self.new_password_entry = ttk.Entry(self.signup_frame, show="*", width=20)
        self.new_password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Signup button in the signup window
        ttk.Button(self.signup_frame, text="Signup", command=lambda: self.signup(self.signup_frame)).grid(row=2, column=0,
                                                                                                  columnspan=2, pady=10)

    def signup(self, signup_window):
        # Get new username and password
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        if not new_username or not new_password:
            messagebox.showinfo("Cannot be Empty", "Username and password cannot be empty.")
            return

        #Technical Dept
        # Validate and create a new user using UserManager
        user_manager = UserManager()
        user_exists = user_manager.signup_user(new_username, new_password)

        if user_exists:
            messagebox.showinfo("Exists", "Username already exists. Please choose a different username.")
        else:
            # Successful signup
            messagebox.showinfo("Signup Successful", "User created successfully. You can now log in.")
            signup_window.destroy()

    def resize_signup_background(self, event):
        # Check if the original image has been loaded
        if hasattr(self, 'signup_original_image'):
            # Resize the background image to the size of the window
            new_width, new_height = event.width, event.height
            image = self.signup_original_image.resize((new_width, new_height), Image.LANCZOS)

            # Update the image of the background label
            self.signup_background_image = ImageTk.PhotoImage(image)
            self.signup_image_label.config(image=self.signup_background_image)
            self.signup_image_label.image = self.signup_background_image  # Keep a reference!

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
                    user_manager = UserManager()
                    user_manager.save_dataset(self.logged_in_userid, dataset_name, self.values)
                    self.result_label.config(text="Dataset successfully saved.")
                else:
                    self.result_label.config(text="Dataset name cannot be empty.")
            else:
                self.result_label.config(text="No data to save.")
        else:
            self.result_label.config(text="Please login before saving the dataset.")

    def reset_dataset(self):
        # Ask for confirmation
        confirmation = messagebox.askyesno("Confirmation",
                                           "Are you sure you want to empty the current dataset values?")

        if confirmation:
            # Reset the dataset
            self.values = []
            self.data_entry.delete(0, tk.END)
            self.result_label.config(text="Dataset reset successfully.")
        else:
            self.result_label.config(text="Dataset reset canceled.")

    def show_history(self):
        if self.logged_in_username:
            # Create a new window for showing history
            history_window = tk.Toplevel(self.root)
            history_window.title("Data History")

            # Get historical data from the backend using UserManagement
            user_manager = UserManager()
            historical_data = user_manager.get_user_history(self.logged_in_userid)

            selected_row = None  # Variable to store the selected row

            def on_row_select(event):
                nonlocal selected_row
                item = tree.selection()
                if item:
                    selected_row = tree.item(item, "values")

            def delete_selected_dataset():
                nonlocal selected_row
                if selected_row:
                    dataset_id = selected_row[0]
                    dataset_name = selected_row[1]

                    # Ask for confirmation
                    confirmation = messagebox.askyesno("Confirmation",
                                                       f"Are you sure you want to delete the dataset '{dataset_name}'?")

                    if confirmation:
                        # Call the delete_dataset method in UserManager to delete the dataset
                        user_manager.delete_dataset(dataset_id, self.logged_in_userid)
                        messagebox.showinfo("Dataset Deleted", "Dataset successfully deleted.")

                        # Refresh the history window after deletion
                        history_window.destroy()
                        self.show_history()
                else:
                    messagebox.showinfo("No Dataset Selected", "Please select a dataset to delete.")
                    message_label.config(text="Please select a row before clicking Delete DataSet")

            # Create a Treeview widget for displaying the table
            tree = ttk.Treeview(history_window, selectmode="browse")
            tree["columns"] = ("ID", "Dataset Name", "Actual Data")
            tree.column("#0", width=0, stretch=tk.NO)  # Hide the first column

            # Define column headings
            tree.heading("#0", text="", anchor=tk.W)
            tree.heading("ID", text="ID", anchor=tk.W)
            tree.heading("Dataset Name", text="Dataset Name", anchor=tk.W)
            tree.heading("Actual Data", text="Actual Data", anchor=tk.W)

            # Insert data into the treeview
            for idx, (id, dataset_name, data) in enumerate(historical_data, start=1):
                tree.insert("", idx, values=(id, dataset_name, data))

            # Display the treeview
            tree.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

            # Add scrollbar to the treeview
            scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=tree.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")
            tree.configure(yscrollcommand=scrollbar.set)

            # Bind the on_row_select function to the click event on rows
            tree.bind("<ButtonRelease-1>", on_row_select)

            # Create a label for displaying messages
            message_label = ttk.Label(history_window, text="")
            message_label.grid(row=len(historical_data) + 3, column=0, columnspan=2, pady=10)

            # Add a "Load DataSet" button at the bottom
            load_button = ttk.Button(history_window, text="Load DataSet",
                                     command=lambda: self.load_selected_dataset(selected_row, message_label))
            load_button.grid(row=len(historical_data) + 1, column=0, pady=10)

            # Add a "Delete DataSet" button at the bottom under the table
            delete_button = ttk.Button(history_window, text="Delete DataSet", command=delete_selected_dataset)
            delete_button.grid(row=len(historical_data) + 2, column=0, pady=10)

            # Make the window resizable
            history_window.resizable(True, True)
        else:
            self.result_label.config(text="Please login before watching the history.")

    def load_selected_dataset(self, selected_row, message_label):
        if selected_row:
            # Assuming selected_row is a tuple with (ID, Dataset Name, Actual Data)
            dataset_id, dataset_name, actual_data = selected_row

            # Clear existing values
            self.values = []

            # Check if actual_data is bytes, then decode it
            if isinstance(actual_data, bytes):
                actual_data_str = actual_data.decode('utf-8')
            else:
                actual_data_str = actual_data

            # Print actual_data_str for debugging
            # print("Actual Data String from the selected row:", actual_data_str)

            try:
                # Deserialize actual_data_str (JSON string) into a list
                self.values = json.loads(actual_data_str)
                message_label.config(text="Dataset successfully loaded.")
                self.result_label.config(text="Dataset loaded successfully.")
            except json.JSONDecodeError as e:
                print(f"Error loading dataset. JSONDecodeError: {e}")
                message_label.config(text="Error loading dataset. Please check the format of the data.")
                self.result_label.config(text="Error loading dataset. Please check the format of the data.")
        else:
            messagebox.showinfo("No Dataset Selected", "Please select a dataset to load.")
            message_label.config(text="Please select a row before clicking Load DataSet")
            self.result_label.config(text="Please select a row before clicking Load DataSet")

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
