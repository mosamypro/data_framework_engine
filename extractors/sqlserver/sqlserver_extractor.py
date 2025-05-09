# Disable Pylint import errors for database drivers
# These are installed in the Docker containers but may not be available in the development environment
# pylint: disable=import-error
import pyodbc
# pylint: enable=import-error
from extractors.abstractextractor import BaseExtractor

class SQLServerExtractor(BaseExtractor):
    """
    SQL Server specific implementation of the BaseExtractor.
    
    Provides methods to connect to a SQL Server database, extract metadata,
    read data, and close the connection.
    """
    
    def __init__(self, host, port, database, user, password):
        """
        Initialize the SQL Server extractor with connection parameters.
        
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
        Establish a connection to the SQL Server database using the configured credentials and connection parameters.
        
        Returns:
            Connection: A connection object to the SQL Server database.
            
        Raises:
            ConnectionError: If unable to connect to the database.
            ConfigurationError: If connection parameters are invalid or missing.
        """
        try:
            # Build the connection string
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.host},{self.port};"
                f"DATABASE={self.database};"
                f"UID={self.user};"
                f"PWD={self.password};"
            )
            
            # Establish the connection
            self.connection = pyodbc.connect(conn_str)
            self.cursor = self.connection.cursor()
            return self.connection
        except pyodbc.Error as e:
            error_msg = str(e)
            if "Invalid connection string attribute" in error_msg or "Data source name not found" in error_msg:
                raise ValueError(f"Configuration error: {error_msg}") from e
            else:
                raise ConnectionError(f"Failed to connect to SQL Server: {error_msg}") from e

    def extract_metadata(self):
        """
        Extract metadata from the SQL Server database.
        
        Returns:
            dict: Dictionary containing database metadata
            
        Raises:
            ConnectionError: If not connected to the database
        """
        if not self.connection or not self.cursor:
            raise ConnectionError("Not connected to database. Call connect() first.")
            
        metadata = {
            "tables": [],
            "database_name": self.database
        }
        
        # Get list of tables
        table_query = """
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG = ?
        """
        self.cursor.execute(table_query, (self.database,))
        tables = self.cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            table_info = {"name": table_name, "columns": []}
            
            # Get column information
            column_query = """
                SELECT
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT,
                    CHARACTER_MAXIMUM_LENGTH,
                    NUMERIC_PRECISION,
                    NUMERIC_SCALE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = ? AND TABLE_CATALOG = ?
                ORDER BY ORDINAL_POSITION
            """
            self.cursor.execute(column_query, (table_name, self.database))
            columns = self.cursor.fetchall()
            
            for column in columns:
                col_name, data_type, is_nullable, default_val, char_max_len, num_precision, num_scale = column
                
                # Build the full data type with precision/scale/length if applicable
                full_data_type = data_type
                if char_max_len is not None and char_max_len > 0:
                    full_data_type += f"({char_max_len})"
                elif data_type in ('decimal', 'numeric') and num_precision is not None:
                    if num_scale is not None:
                        full_data_type += f"({num_precision},{num_scale})"
                    else:
                        full_data_type += f"({num_precision})"
                
                table_info["columns"].append({
                    "name": col_name,
                    "type": full_data_type,
                    "nullable": is_nullable == "YES",
                    "default": default_val
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
            
        Raises:
            ConnectionError: If not connected to the database
        """
        if not self.connection or not self.cursor:
            raise ConnectionError("Not connected to database. Call connect() first.")
            
        try:
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            results = []
            
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
                
            return results
        except pyodbc.Error as err:
            error_msg = str(err)
            raise RuntimeError(f"Error executing query: {error_msg}") from err
                                
    def close_connection(self):
        """
        Close the database connection.
        
        Returns:
            bool: True if connection closed successfully, False otherwise
        """
        if self.cursor:
            try:
                self.cursor.close()
            except pyodbc.Error:
                pass  # Ignore errors when closing cursor
            
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.cursor = None
                return True
            except pyodbc.Error as err:
                print(f"Error closing connection: {err}")
                return False
        
        return True
