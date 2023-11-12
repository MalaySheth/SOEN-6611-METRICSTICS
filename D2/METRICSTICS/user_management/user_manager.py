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
            cursor.execute("SELECT * FROM users WHERE username=%s AND password_hash=%s",
                           (username, password_hash))
            user = cursor.fetchone()
            if user:
                print('Authentication successful')
                return True
            else:
                print('Authentication failed')
                return False
        except Error as e:
            print(f'Error: {e}')
            return False

    def save_dataset(self, user_id, dataset_name, data):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO datasets (user_id, dataset_name, data) VALUES (%s, %s, %s)",
                           (user_id, dataset_name, data))
            self.connection.commit()
            print('Dataset saved successfully')
        except Error as e:
            print(f'Error: {e}')
