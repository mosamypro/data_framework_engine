# Dockerfile for Controller Container
FROM python:3.9-slim

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r /app/requirements.txt

# Copy the controller script
COPY controller.py /app/controller.py

# Set working directory
WORKDIR /app

# Command to run the controller
CMD ["python", "controller.py"]
