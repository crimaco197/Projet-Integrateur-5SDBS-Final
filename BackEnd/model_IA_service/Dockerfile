# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y curl && apt-get clean
RUN apt-get update && apt-get install -y iputils-ping

# Copy only the dependencies file first (for caching)
COPY requirements.txt /app

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose the application port
EXPOSE 8004

# Command to start the FastAPI service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]