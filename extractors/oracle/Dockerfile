# Dockerfile for Oracle Extractor
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y libaio1
RUN pip install cx_Oracle requests

# Copy the extractor script
COPY oracle_extractor.py /app/oracle_extractor.py

# Set working directory
WORKDIR /app

# Command to run the extractor
CMD ["python", "oracle_extractor.py"]