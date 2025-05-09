# Dockerfile for CDC Stream Processor
FROM python:3.9-slim

# Install dependencies
RUN pip install kafka-python requests

# Copy the CDC stream processor script
COPY cdc_stream_processor.py /app/cdc_stream_processor.py

# Set working directory
WORKDIR /app

# Command to run the CDC stream processor
CMD ["python", "cdc_stream_processor.py"]