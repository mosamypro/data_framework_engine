# Dockerfile for Metadata Repository
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file and metadata repository script
COPY requirements.txt metadata_repository.py ./

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port for the REST API
EXPOSE 5000

# Command to run the metadata repository
CMD ["python", "metadata_repository.py"]
