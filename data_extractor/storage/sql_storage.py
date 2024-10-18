







# sql_storage.py

import sqlite3  # Make sure to import sqlite3 here
from data_extractor.storage.storage import Storage

class SQLStorage(Storage):
    def __init__(self, connection_string):
        super().__init__()  # Call parent constructor
        self.connection_string = connection_string
        self.conn = sqlite3.connect(connection_string)  # Connect to the provided database string
        self.cursor = self.conn.cursor()

    def store(self, table_name, data):
        """Stores data in a SQL database."""
        self.table_name = table_name.replace(" ", "_").replace("-", "_")

        # Create the table if it doesn't exist
        escaped_table_name = f'"{self.table_name}"'

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {escaped_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )""")

        # Insert the data into the table
        self.cursor.execute(f"INSERT INTO {escaped_table_name} (data) VALUES (?)", (str(data),))

        # Commit the changes
        self.conn.commit()

    def close(self):
        """Closes the connection to the database."""
        self.conn.close()







