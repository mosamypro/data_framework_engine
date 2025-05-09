# Dockerfile for MySQL Extractor
FROM python:3.9-slim

# Install dependencies
RUN pip install mysql-connector-python requests

# Copy the extractor script
COPY mysql_extractor.py /app/mysql_extractor.py

# Set working directory
WORKDIR /app

# Command to run the extractor
CMD ["python", "mysql_extractor.py"]