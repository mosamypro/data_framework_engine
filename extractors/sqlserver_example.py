#!/usr/bin/env python3
"""
Example script demonstrating how to use the SQLServerExtractor to connect to a SQL Server database,
extract metadata, and query data.

This example connects to a SQL Server instance running in Docker, extracts metadata about the database
structure, and executes a sample query.
"""

import os
import sys
import json
from datetime import datetime

# Add the parent directory to the path so we can import the extractors package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractors.sqlserver.sqlserver_extractor import SQLServerExtractor


def main():
    """
    Main function to demonstrate SQLServerExtractor usage.
    """
    # Connection parameters
    host = "docker"  # Docker container hostname
    port = 1434  # Default SQL Server port
    database = "test"  # Example database name
    user = "sa"  # From connection.txt
    password = "sa@password2024"  # From connection.txt

    # Create an instance of the SQL Server extractor
    print(f"Connecting to SQL Server at {host}:{port}...")
    sql_server_extractor = SQLServerExtractor(
        host=host, port=port, database=database, user=user, password=password
    )

    try:
        # Connect to the database
        connection = sql_server_extractor.connect()
        print("Connected to SQL Server database successfully")

        # Extract metadata
        print("\nExtracting database metadata...")
        metadata = sql_server_extractor.extract_metadata()

        # Display database information
        print(f"Database: {metadata['database_name']}")
        print(f"Tables found: {len(metadata['tables'])}")

        # Display table and column information
        for table in metadata["tables"][:5]:  # Limit to first 5 tables for brevity
            print(f"\nTable: {table['name']}")
            print("Columns:")
            for column in table["columns"]:
                nullable = "NULL" if column["nullable"] else "NOT NULL"
                print(f"  - {column['name']} ({column['type']}) {nullable}")

        if len(metadata["tables"]) > 5:
            print(f"\n... and {len(metadata['tables']) - 5} more tables")

        # Example query - get the first 5 rows from a table
        # This assumes there's a Person.Person table in AdventureWorks
        print("\nExecuting sample query...")
        query = """
            SELECT TOP 5 *
            FROM Person.Person
        """

        try:
            results = sql_server_extractor.read_data(query)

            print(f"\nQuery Results ({len(results)} rows):")
            for row in results:
                # Print a few key columns for each row
                print(
                    f"ID: {row.get('BusinessEntityID')}, "
                    f"Name: {row.get('FirstName')} {row.get('LastName')}, "
                    f"Email: {row.get('EmailAddress', 'N/A')}"
                )
        except Exception as query_err:
            print(f"Query error: {query_err}")

            # Try an alternative query if the first one fails
            print("\nTrying alternative query...")
            alt_query = """
                SELECT TOP 5 name, create_date
                FROM sys.tables
            """
            try:
                results = sql_server_extractor.read_data(alt_query)
                print(f"\nAlternative Query Results ({len(results)} rows):")
                for row in results:
                    print(
                        f"Table: {row.get('name')}, Created: {row.get('create_date')}"
                    )
            except Exception as alt_err:
                print(f"Alternative query error: {alt_err}")

    except ConnectionError as conn_err:
        print(f"Connection error: {conn_err}")
    except ValueError as val_err:
        print(f"Configuration error: {val_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Close the connection
        if (
            hasattr(sql_server_extractor, "connection")
            and sql_server_extractor.connection
        ):
            print("\nClosing connection...")
            if sql_server_extractor.close_connection():
                print("Connection closed successfully")
            else:
                print("Failed to close connection")


if __name__ == "__main__":
    main()
