from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """
    Abstract base class for all database extractors.
    Defines the common interface that all specific database extractors must implement.
    """
    @abstractmethod
    def connect(self):
        """
        Establish a connection to the database.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def extract_metadata(self):
        """
        Extract metadata from the database.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def read_data(self, query):
        """
        Execute a query and return the results.
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            Results of the query execution
        """
        pass

    @abstractmethod
    def close_connection(self):
        """
        Close the database connection.
        Must be implemented by subclasses.
        """
        pass
