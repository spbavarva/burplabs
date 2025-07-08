# Use a minimal base image with Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir .

# Default command (can be overridden)
ENTRYPOINT ["portswiggerlab"]
