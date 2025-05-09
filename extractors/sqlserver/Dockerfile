# Dockerfile for SQL Server Extractor
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y unixodbc-dev
RUN pip install pyodbc requests

# Copy the extractor script
COPY sqlserver_extractor.py /app/sqlserver_extractor.py

# Set working directory
WORKDIR /app

# Command to run the extractor
CMD ["python", "sqlserver_extractor.py"]