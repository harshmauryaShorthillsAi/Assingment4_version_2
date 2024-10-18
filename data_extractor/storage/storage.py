

# storage.py

import sqlite3
from abc import ABC, abstractmethod
import os

class Storage(ABC):
    def __init__(self, db_name='assignment4.db'):
        self.db_name = db_name
        
        # Check if the database file exists
        if not os.path.exists(self.db_name):
            # Create a new database file if it doesn't exist
            open(self.db_name, 'w').close()  # Creates an empty file

        # Establish a connection to SQLite
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    @abstractmethod
    def store(self):
        """Store the extracted data."""
        pass
    
    @abstractmethod
    def close(self):
        """Close the connection to the storage."""
        pass
