# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
# Copy the application code to the working directory
COPY . .

# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "80"]