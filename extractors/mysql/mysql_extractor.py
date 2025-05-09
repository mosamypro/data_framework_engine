"""
MySQL Extractor

This module provides functionality to extract data and metadata from MySQL databases.
"""

# Disable Pylint import errors for database drivers
# These are installed in the Docker containers but may not be available in the development environment
# pylint: disable=import-error
import mysql.connector
# pylint: enable=import-error
from extractors.abstractextractor import BaseExtractor

class MySQLExtractor(BaseExtractor):
    """
    MySQL specific implementation of the BaseExtractor.
    
    Provides methods to connect to a MySQL database, extract metadata,
    read data, and close the connection.
    """
    
    def __init__(self, host, port, database, user, password):
        """
        Initialize the MySQL extractor with connection parameters.
        
        Args:
            host (str): Database host address
            port (int): Database port
            database (str): Database name
            user (str): Database username
            password (str): Database password
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """
        Establish a connection to the MySQL database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL database: {err}")
            return False
            
    def extract_metadata(self):
        """
        Extract metadata from the MySQL database.
        
        Returns:
            dict: Dictionary containing database metadata
        """
        if not self.connection or not self.cursor:
            raise ConnectionError("Not connected to database. Call connect() first.")
            
        metadata = {
            "tables": [],
            "database_name": self.database
        }
        
        # Get list of tables
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        
        for table in tables:
            table_name = list(table.values())[0]
            table_info = {"name": table_name, "columns": []}
            
            # Get column information
            self.cursor.execute(f"DESCRIBE {table_name}")
            columns = self.cursor.fetchall()
            
            for column in columns:
                table_info["columns"].append({
                    "name": column["Field"],
                    "type": column["Type"],
                    "nullable": column["Null"] == "YES",
                    "key": column["Key"],
                    "default": column["Default"],
                    "extra": column["Extra"]
                })
                
            metadata["tables"].append(table_info)
            
        return metadata
        
    def read_data(self, query):
        """
        Execute a query and return the results.
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            list: List of dictionaries containing the query results
        """
        if not self.connection or not self.cursor:
            raise ConnectionError("Not connected to database. Call connect() first.")
            
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return []
            
    def close_connection(self):
        """
        Close the database connection.
        
        Returns:
            bool: True if connection closed successfully, False otherwise
        """
        if self.cursor:
            self.cursor.close()
            
        if self.connection:
            try:
                self.connection.close()
                return True
            except mysql.connector.Error as err:
                print(f"Error closing connection: {err}")
                return False
        
        return True
