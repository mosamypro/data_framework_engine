"""
Example Usage of Extractors

This script demonstrates how to use the extractor modules to connect to
different database systems and extract data and metadata.
"""

# Import the BaseExtractor class


# Import the MySQLExtractor class
from extractors.mysql.mysql_extractor import MySQLExtractor

# Alternatively, you could import everything from extractors
# from extractors import abstractextractor, mysql
# Then use: mysql.mysql_extractor.MySQLExtractor

def main():
    """
    Example of using the MySQL extractor.
    """
    # Example connection parameters (replace with actual values when using)
    mysql_params = {
        "host": "localhost",
        "port": 3306,
        "database": "example_db",
        "user": "user",
        "password": "password"
    }
    
    # Create an instance of the MySQL extractor
    mysql_extractor = MySQLExtractor(**mysql_params)
    
    # Connect to the database
    if mysql_extractor.connect():
        print("Connected to MySQL database successfully")
        
        # Extract metadata
        metadata = mysql_extractor.extract_metadata()
        print(f"Database: {metadata['database_name']}")
        print(f"Tables found: {len(metadata['tables'])}")
        
        for table in metadata['tables']:
            print(f"\nTable: {table['name']}")
            print("Columns:")
            for column in table['columns']:
                print(f"  - {column['name']} ({column['type']})")
        
        # Example query
        query = "SELECT * FROM example_table LIMIT 5"
        results = mysql_extractor.read_data(query)
        
        print("\nQuery Results:")
        for row in results:
            print(row)
        
        # Close the connection
        mysql_extractor.close_connection()
        print("\nConnection closed")
    else:
        print("Failed to connect to MySQL database")

if __name__ == "__main__":
    main()
