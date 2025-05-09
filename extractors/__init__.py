"""
Extractors Package

This package provides database extractors for various database systems.
Each extractor implements the BaseExtractor interface defined in the
abstractextractor module.
"""

# Import subpackages to make them available when importing the extractors package
from . import abstractextractor
from . import mysql

__all__ = ['abstractextractor', 'mysql']
