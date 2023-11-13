import json

import mysql.connector
from mysql.connector import Error


class UserManagement:
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                port=3306,
                database='metricstics_db',
                user='root',
                password='root'
            )
            if connection.is_connected():
                print('Connected to MySQL database')
                return connection
        except Error as e:
            print(f'Error: {e}')
            return None

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print('Connection closed')

    def register_user(self, username, password_hash):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                           (username, password_hash))
            self.connection.commit()
            print('User registered successfully')
        except Error as e:
            print(f'Error: {e}')

    def authenticate_user(self, username, password_hash):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE BINARY username=%s AND BINARY password_hash=%s",
                           (username, password_hash))
            user = cursor.fetchone()
            if user:
                print('Authentication successful')
                return user
            else:
                print('Authentication failed')
                return False
        except Error as e:
            print(f'Error: {e}')
            return False

    def signup_user(self, username, password):
        try:
            cursor = self.connection.cursor()

            # Check if the username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                print("Username already exists. Please choose a different username.")
                return True
            elif not username or not password:
                print("Username and password cannot be empty.")
                return False
            else:
                # Create a new user entry
                cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                               (username, password))
                self.connection.commit()
                print("Signup successful. You can now log in.")
                return False

        except Error as e:
            print(f'Error: {e}')
            return False

    def save_dataset(self, user_id, dataset_name, data):
        try:
            # Convert the list to a JSON string
            data_str = json.dumps(data)

            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO datasets (user_id, dataset_name, data) VALUES (%s, %s, %s)",
                           (user_id, dataset_name, data_str))
            self.connection.commit()
            print('Dataset saved successfully')
        except Error as e:
            print(f'Error: {e}')

    def get_user_history(self, user_id):
        try:
            cursor = self.connection.cursor()

            # Assuming there's a 'datasets' table with columns 'user_id', 'dataset_name', and 'data'
            cursor.execute("SELECT id, dataset_name, data FROM datasets WHERE user_id = %s", (user_id,))
            historical_data = cursor.fetchall()

            return historical_data

        except Error as e:
            print(f'Error: {e}')
            return []
